import pkgutil
from typing import Any

from settings import get_settings
from .. import patching
from ..Options import OracleOfSeasonsLinkedHerosCave
from ..common.patching.RomData import RomData
from ..common.patching.rooms.decoding import decompress_rooms
from ..common.patching.rooms.encoding import write_room_data


### How rooms work:
# Room number 0xYZZ = group Y, room ZZ
# Groups 0-3 are seasons spring to winter (usually 0ZZ)
# Group 4 is subrosia/maku/grottos (usually 1ZZ/2ZZ/3ZZ)
# Group 5-6 are the big rooms (usually 4ZZ/6ZZ and 5ZZ/7ZZ)

# Positions are assessed with YX format
# Positions in small rooms are written in decimal, as a line is 10 tiles long
# Positions in big rooms are written in hew, as a line is 16 tiles long (last tile is always 0)

def apply_room_edits(rom_data: RomData, patch_data: dict[str, Any]) -> None:
    room_data = decompress_rooms(rom_data, True)

    apply_d0_alt_entrance_edits(room_data, patch_data)
    apply_d2_alt_entrance_edits(room_data, patch_data)
    apply_samasa_dungeon_edits(room_data, patch_data)
    apply_anti_softlock_edits(room_data)
    apply_misc_edits(room_data)

    write_room_data(rom_data, room_data, True)


def apply_d0_alt_entrance_edits(room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    if not patch_data["options"]["remove_d0_alt_entrance"]:
        return
    for room_id in range(0x0d4, 0x400, 0x100):
        # Remove the grass and the soil in all seasons
        room_data[room_id][17] = 0x11
        room_data[room_id][26] = 0x11
        room_data[room_id][27] = 0x11
        room_data[room_id][28] = 0x11

        # Remove the chimney
        room_data[room_id][57] = 0xaf

    # Add stairs to the chest
    room_data[0x505][0x5a] = 0x53


def apply_d2_alt_entrance_edits(room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    for room_id in range(0x08e, 0x400, 0x100):
        # Replace the vines by stairs in all seasons
        room_data[room_id][34] = 0x36
        room_data[room_id][35] = 0xd0
        room_data[room_id][36] = 0x35
        room_data[room_id][44] = 0x51
        room_data[room_id][45] = 0xd0
        room_data[room_id][46] = 0x50
        if not patch_data["options"]["remove_d2_alt_entrance"]:
            continue

        # Remove the stairs
        room_data[room_id][12] = 0x04
        room_data[room_id - 1][18] = 0x04


def apply_samasa_dungeon_edits(room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    if not patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.samasa:
        return
    # Add the dungeon entrance
    room_data[0x1cf] = bytearray(pkgutil.get_data(patching.__name__, "rooms/samasa_dungeon.dat"))

    if patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.no_alt_entrance:
        room_data[0x1cf][28] = 0x04  # Remove the grass
        room_data[0x1cf][48] = 0xaf  # Remove the chimney
        room_data[0x62c][0x32] = 0x52  # Add stairs to the alt entrance chest


def apply_anti_softlock_edits(room_data: list[bytearray]) -> None:
    # In room 016, move the tree in front of the door left to avoid locking the player
    for room_id in range(0x016, 0x300, 0x100):
        room_data[room_id][16] = 0x70
        room_data[room_id][17] = 0x71
        room_data[room_id][18] = 0x0f
        room_data[room_id][26] = 0x80
        room_data[room_id][27] = 0x81
        room_data[room_id][28] = 0x70
    # In winter, it needs to be different
    room_data[0x316][16] = 0x65
    room_data[0x316][17] = 0x66
    room_data[0x316][18] = 0x0f
    room_data[0x316][26] = 0x55
    room_data[0x316][27] = 0x56
    room_data[0x316][28] = 0x65

    # Remove the natzu bridge lever
    room_data[0x156][66] = 0x04  # Ricky
    room_data[0x356][66] = 0x04  # Moosh

    # Shallow water to leave d4
    for room_id in range(0x01d, 0x300, 0x100):
        room_data[room_id][31] = 0xfa
        room_data[room_id][32] = 0xfa
        room_data[room_id][33] = 0xfa
        room_data[room_id][34] = 0xfa
        room_data[room_id][35] = 0xfa
        room_data[room_id][36] = 0xfa
    # Ice for winter
    room_data[0x31d][31] = 0xdc
    room_data[0x31d][32] = 0xdc
    room_data[0x31d][33] = 0xdc
    room_data[0x31d][34] = 0xdc
    room_data[0x31d][35] = 0xdc

    # Spool swamp had one to leave to east in spring, but it wasn't kept

    # Some snow piles in suburbs to WoW were removed, but this change wasn't kept

    # Remove a snow pile to prevent the statue blocking the path in winter if pushed left
    room_data[0x301][54] = 0x04

    # Remove a snow pile in front of Holly's house to avoid a needless softlock
    room_data[0x37f][56] = 0x04

    # D7 snow piles aren't removed, warp isn't far, and this impacts logic positively

    for room_id in range(0x09a, 0x400, 0x100):
        # Remove rock across pit blocking exit from D5
        room_data[room_id][14] = 0x12

        # Remove bush next to rosa portal
        room_data[room_id][34] = 0x04

    # Add rock at bottom of cliff to block ricky
    for room_id in range(0x08a, 0x400, 0x100):
        room_data[room_id][66] = 0x64

    # Add a ledge from lower portal
    for room_id in range(0x025, 0x400, 0x100):
        room_data[room_id][32] = 0x3a
        room_data[room_id][33] = 0xcf
        room_data[room_id][34] = 0x4b


def apply_misc_edits(room_data: list[bytearray]) -> None:
    # Remove access to first refill room on 4 essences
    for i in range(2, 80, 10):
        for j in range(6):
            room_data[0x41c][i + j] = 0x62 + j

    # Remove access to second refill room on 6 essences
    room_data[0x44c][3] = 0x63

    # Reveal hidden subrosia digging spots if required
    if get_settings()["tloz_oos_options"]["reveal_hidden_subrosia_digging_spots"]:
        room_data[0x406][18] = 0x2f
        room_data[0x457][38] = 0x2f
        room_data[0x447][33] = 0x2f
        room_data[0x43a][46] = 0x2f
        room_data[0x407][13] = 0x2f
        room_data[0x420][68] = 0x2f
        room_data[0x442][14] = 0x2f