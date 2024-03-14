from typing import TYPE_CHECKING, Set, Dict

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from worlds.tloz_oos import LOCATIONS_DATA, ITEMS_DATA
from .Data import build_item_id_to_name_dict, build_location_name_to_id_dict

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

ROOM_AFTER_DRAGONOX = 0x0790
ROOM_BLAINOS_GYM = 0x03B4

ROM_ADDRS = {
    "game_identifier": (0x0134, 9, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0xC2EE, 1, "System Bus"),
    "received_item_index": (0xC6A0, 2, "System Bus"),
    "received_item": (0xCBFB, 1, "System Bus"),
    "location_flags": (0xC600, 0x500, "System Bus"),

    "current_map_group": (0xCC49, 1, "System Bus"),
    "current_map_id": (0xCC4C, 1, "System Bus"),
}


class OracleOfSeasonsClient(BizHawkClient):
    game = "The Legend of Zelda - Oracle of Seasons"
    system = "GBC"
    patch_suffix = ".apseasons"
    local_checked_locations: Set[int]
    local_scouted_locations: Set[int]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = build_item_id_to_name_dict()
        self.location_name_to_id = build_location_name_to_id_dict()
        self.local_checked_locations = set()
        self.local_scouted_locations = set()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "ZELDA DIN":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101  # Remote items + starting inventory
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["slot_name"]]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
        pass

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        try:
            # Handle giving the player items
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"],  # Current state of game (is the player actually in-game?)
                RAM_ADDRS["received_item_index"],  # Number of received items
                RAM_ADDRS["received_item"],  # Received item still pending?
                RAM_ADDRS["location_flags"],  # Location flags
                RAM_ADDRS["current_map_group"],
                RAM_ADDRS["current_map_id"],  # Current map & id to check for goal completion
            ])
            if read_result is None:
                return

            # Player is not in-game, don't do anything else
            if read_result[0][0] != 2:
                return

            num_received_items = int.from_bytes(read_result[1], "little")
            received_item_is_empty = (read_result[2][0] == 0)
            flag_bytes = read_result[3]
            current_room = (read_result[4][0] << 8) | read_result[5][0]

            # Read location flags from RAM
            local_checked_locations = set(ctx.locations_checked)
            local_scouted_locations = set(ctx.locations_scouted)
            for name, location in LOCATIONS_DATA.items():
                if "local" in location and location["local"] is True:
                    continue
                if "flag_byte" not in location:
                    continue

                bytes_to_test = location["flag_byte"]
                if not hasattr(bytes_to_test, "__len__"):
                    bytes_to_test = [bytes_to_test]

                # Check all "flag_byte" to see if location has been checked
                for byte_addr in bytes_to_test:
                    byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
                    bit_mask = location["bit_mask"] if "bit_mask" in location else 0x20
                    if flag_bytes[byte_offset] & bit_mask == bit_mask:
                        location_id = self.location_name_to_id[name]
                        local_checked_locations.add(location_id)
                        break

                # Check "scouting_byte" to see if map has been visited for scoutable locations
                if "scouting_byte" in location:
                    byte_to_test = location["scouting_byte"]
                    byte_offset = byte_to_test - RAM_ADDRS["location_flags"][0]
                    bit_mask = location["scouting_mask"] if "scouting_mask" in location else 0x10
                    if flag_bytes[byte_offset] & bit_mask == bit_mask:
                        # Map has been visited, scout the location if it hasn't been already
                        location_id = self.location_name_to_id[name]
                        local_scouted_locations.add(location_id)

            # Send locations
            if self.local_checked_locations != local_checked_locations:
                self.local_checked_locations = local_checked_locations
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(self.local_checked_locations)
                }])

            # Scout locations
            if self.local_scouted_locations != local_scouted_locations:
                self.local_scouted_locations = local_scouted_locations
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": list(self.local_scouted_locations),
                    "create_as_hint": int(2)
                }])

            # Don't process received items if we are in Blaino's Gym to prevent him
            # from calling us a cheater
            if current_room == ROOM_BLAINOS_GYM:
                return

            # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
            # fill it with the next item
            if num_received_items < len(ctx.items_received) and received_item_is_empty:
                next_item_name = self.item_id_to_name[ctx.items_received[num_received_items].item]
                await bizhawk.write(ctx.bizhawk_ctx, [(0xCBFB, [
                    ITEMS_DATA[next_item_name]["id"],
                    ITEMS_DATA[next_item_name]["subid"] if "subid" in ITEMS_DATA[next_item_name] else 0
                ], "System Bus")])

            # Send game clear
            game_clear = (current_room == ROOM_AFTER_DRAGONOX)
            if not ctx.finished_game and game_clear:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass