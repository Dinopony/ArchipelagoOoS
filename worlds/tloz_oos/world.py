import os
from threading import Event
from typing import Any, ClassVar, TextIO, cast

from BaseClasses import CollectionState, Item, Location, MultiWorld
from Options import Option
from rule_builder.rules import Has
from worlds.AutoWorld import World

from .common.Util import build_item_name_to_id_dict, build_location_name_to_id_dict
from .data import ITEMS_DATA
from .data.Constants import (
    DEFAULT_SEASONS,
    DUNGEON_CONNECTIONS,
    ESSENCES,
    ITEM_GROUPS,
    LOCATION_GROUPS,
    LOST_WOODS_ITEM_SEQUENCE,
    LOST_WOODS_MAIN_SEQUENCE,
    MARKET_LOCATIONS,
    OLD_MAN_RUPEE_VALUES,
    PORTAL_CONNECTIONS,
    SAMASA_GATE_CODE,
    SEASON_NAMES,
    VANILLA_SHOP_PRICES,
)
from .data.locations import LOCATIONS_DATA
from .options import OracleOfSeasonsOptions
from .settings import OracleOfSeasonsSettings
from .web_world import OracleOfSeasonsWeb


class OracleOfSeasonsWorld(World):
    """
    The Legend of Zelda: Oracles of Seasons is one of the rare Capcom entries to the series.
    The seasons in the world of Holodrum have been a mess since Onox captured Din, the Oracle of Seasons.
    Gather the Essences of Nature, confront Onox and rescue Din to give nature some rest in Holodrum.
    """

    game = "The Legend of Zelda - Oracle of Seasons"
    options_dataclass = OracleOfSeasonsOptions
    options: OracleOfSeasonsOptions  # pyright: ignore[reportIncompatibleVariableOverride]
    web = OracleOfSeasonsWeb()
    topology_present = True

    settings: ClassVar[OracleOfSeasonsSettings]  # pyright: ignore[reportIncompatibleVariableOverride]
    settings_key = "tloz_oos_options"

    location_name_to_id = build_location_name_to_id_dict(LOCATIONS_DATA)
    item_name_to_id = build_item_name_to_id_dict(ITEMS_DATA)
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS
    origin_region_name = "impa's house"
    item_mapping: ClassVar[dict[str, str]] = {
        "Rupees (1)": "Rupees",
        "Rupees (5)": "Rupees",
        "Rupees (10)": "Rupees",
        "Rupees (20)": "Rupees",
        "Rupees (30)": "Rupees",
        "Rupees (50)": "Rupees",
        "Rupees (100)": "Rupees",
        "Rupees (200)": "Rupees",
        "_reached_d2_rupee_room": "Rupees",
        "_reached_d6_rupee_room": "Rupees",
        "rupees from old man in goron mountain": "Rupees",
        "rupees from old man near blaino": "Rupees",
        "rupees from old man near d1": "Rupees",
        "rupees from old man near western coast house": "Rupees",
        "rupees from old man in horon": "Rupees",
        "rupees from old man near d6": "Rupees",
        "rupees from old man near holly's house": "Rupees",
        "rupees from old man near mrs. ruul": "Rupees",
        "Ore Chunks (10)": "Ore Chunks",
        "Ore Chunks (25)": "Ore Chunks",
        "Ore Chunks (50)": "Ore Chunks",
        "Bombs (10)": "Bombs",
        "Bombs (20)": "Bombs",
        "Bombchus (10)": "Bombchus",
        "Bombchus (20)": "Bombchus",
    }

    @classmethod
    def version(cls) -> str:
        return cls.world_version.as_simple_string()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.pre_fill_items: list[Item] = []
        self.default_seasons: dict[str, int] = DEFAULT_SEASONS.copy()
        self.dungeon_entrances: dict[str, str] = DUNGEON_CONNECTIONS.copy()
        self.portal_connections: dict[str, str] = PORTAL_CONNECTIONS.copy()
        self.lost_woods_item_sequence: list[list] = LOST_WOODS_ITEM_SEQUENCE.copy()
        self.lost_woods_main_sequence: list[list] = LOST_WOODS_MAIN_SEQUENCE.copy()
        self.old_man_rupee_values: dict[str, int] = OLD_MAN_RUPEE_VALUES.copy()
        self.samasa_gate_code: list[int] = SAMASA_GATE_CODE.copy()
        self.shop_prices: dict[str, int] = VANILLA_SHOP_PRICES.copy()
        self.shop_order: list[list[str]] = []
        self.shop_rupee_requirements: dict[str, int] = {}
        self.essences_in_game: list[str] = ESSENCES
        self.random_rings_pool: list[str] = []
        self.remaining_progressive_gasha_seeds = 0
        self.remaining_progressive_containers = 0
        self.item_mapping_collect: dict[str, tuple[str, int]] = {}

        self.made_hints = Event()
        self.region_hints: list[tuple[str, str | int]] = []
        self.item_hints: list[Item | None] = []
        self.num_prog: int = 1 # initialized at 1 so that before pre_fill, any prog counts as all the progs

    def generate_early(self) -> None:
        from .generation.GenerateEarly import generate_early

        generate_early(self)

    def create_regions(self) -> None:
        from .generation.CreateRegions import create_regions

        create_regions(self)

    def set_rules(self) -> None:
        from .generation.logic import apply_rule_forbiddance, apply_self_locking_rules, create_connections

        create_connections(self, self.options)
        apply_self_locking_rules(self)
        apply_rule_forbiddance(self)
        self.set_completion_rule(Has("_beaten_game"))

    def create_item(self, name: str) -> Item:
        from .generation.create_items import create_item
        return create_item(self, name)

    def create_items(self) -> None:
        from .generation.create_items import create_items

        create_items(self)

    def get_pre_fill_items(self) -> list[Item]:
        return self.pre_fill_items

    @classmethod
    def stage_pre_fill(cls, multiworld: MultiWorld):
        from .generation.pre_fill_dungeon import stage_pre_fill_dungeon_items
        from .generation.pre_fill_prog_count import stage_pre_fill_check_prog

        stage_pre_fill_dungeon_items(multiworld)
        stage_pre_fill_check_prog(multiworld)


    def get_filler_item_name(self) -> str:
        filler_item_names = [
            "Rupees (1)",
            "Rupees (5)",
            "Rupees (10)",
            "Rupees (10)",
            "Rupees (20)",
            "Rupees (30)",
            "Ore Chunks (10)",
            "Ore Chunks (10)",
            "Ore Chunks (25)",
            "Random Ring",
            "Random Ring",
            "Random Ring",
            "Gasha Seed",
            "Gasha Seed",
            "Potion",
        ]

        item_name = self.random.choice(filler_item_names)
        if item_name == "Random Ring":
            return self.get_random_ring_name()
        return item_name

    def get_random_ring_name(self) -> str:
        if len(self.random_rings_pool) > 0:
            return self.random_rings_pool.pop()
        return self.get_filler_item_name()  # It might loop but not enough to really matter

    def connect_entrances(self) -> None:
        from .generation.ER import oos_randomize_entrances

        oos_randomize_entrances(self)

    # noinspection PyUnusedLocal
    @classmethod
    def stage_fill_hook(
        cls,
        multiworld: MultiWorld,
        progitempool: list[Item],
        usefulitempool: list[Item],
        filleritempool: list[Item],
        fill_locations,
    ):
        from .generation.OrderPool import order_pool

        order_pool(multiworld, progitempool)

    def pre_output(self) -> None:
        from .generation.hints import create_item_hints, create_region_hints

        if self.options.bird_hint.know_it_all():
            self.region_hints = create_region_hints(self)

        if self.options.bird_hint.owl():
            self.item_hints = create_item_hints(self)

    def generate_output(self, output_directory: str) -> None:
        from .generation.PatchWriter import oos_create_ap_procedure_patch

        patch = oos_create_ap_procedure_patch(self)
        rom_path = os.path.join(
            output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}"
        )
        patch.write(rom_path)

    def fill_slot_data(self) -> dict:
        options = cast(dict[str, type[Option[Any]]], cast(object, OracleOfSeasonsOptions.type_hints))
        slot_data = {
            "version": f"{self.version()}",
            "options": self.options.as_dict(
                *[
                    option_name
                    for option_name in options
                    if hasattr(options[option_name], "include_in_slot_data")
                ]
            ),
            # "samasa_gate_sequence": ' '.join([str(x) for x in self.samasa_gate_code]),
            "lost_woods_item_sequence": self.lost_woods_item_sequence,
            "lost_woods_main_sequence": self.lost_woods_main_sequence,
            "default_seasons": self.default_seasons,
            "old_man_rupee_values": self.old_man_rupee_values,
            "dungeon_entrances": {
                a.replace(" entrance", ""): b.replace("enter ", "") for a, b in self.dungeon_entrances.items()
            },
            "essences_in_game": self.essences_in_game,
            "subrosia_portals": self.portal_connections,
            "shop_rupee_requirements": self.shop_rupee_requirements,
            "shop_costs": self.shop_prices,
        }

        # The structure is made to make it easy to call CreateHints
        slot_data_item_hints = []
        for item_hint in self.item_hints:
            if item_hint is None:
                # Joke hint
                slot_data_item_hints.append(None)
                continue
            location = cast(Location, item_hint.location)
            slot_data_item_hints.append((location.address, location.player))
        slot_data["item_hints"] = slot_data_item_hints

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO):
        from .generation.CreateRegions import location_is_active

        spoiler_handle.write(f"\n\nDefault Seasons ({self.multiworld.player_name[self.player]}):\n")
        for region_name, season in self.default_seasons.items():
            spoiler_handle.write(f"\t- {region_name} --> {SEASON_NAMES[season]}\n")

        if self.options.shuffle_dungeons:
            spoiler_handle.write(f"\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n")
            for entrance, dungeon in self.dungeon_entrances.items():
                spoiler_handle.write(f"\t- {entrance} --> {dungeon.replace('enter ', '')}\n")

        if self.options.shuffle_portals != "vanilla":
            spoiler_handle.write(f"\nSubrosia Portals ({self.multiworld.player_name[self.player]}):\n")
            for portal_holo, portal_sub in self.portal_connections.items():
                spoiler_handle.write(f"\t- {portal_holo} --> {portal_sub}\n")

        spoiler_handle.write(f"\nShop Prices ({self.multiworld.player_name[self.player]}):\n")
        shop_codes = [code for shop in self.shop_order for code in shop]
        shop_codes.extend(MARKET_LOCATIONS)
        for shop_code in shop_codes:
            price = self.shop_prices[shop_code]
            for loc_name, loc_data in LOCATIONS_DATA.items():
                if loc_data.get("symbolic_name", None) is None or loc_data["symbolic_name"] != shop_code:
                    continue
                if location_is_active(self, loc_name, loc_data):
                    currency = "Ore Chunks" if shop_code.startswith("subrosia") else "Rupees"
                    spoiler_handle.write(f"\t- {loc_name}: {price} {currency}\n")
                break

    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if not change:
            return False

        mapping = self.item_mapping_collect.get(item.name, None)
        if mapping is not None:
            state.prog_items[self.player][mapping[0]] += mapping[1]

        state.prog_items[self.player]["progs"] += 100 # Pre-multiply by 100 to not have to do it the following line
        state.prog_items[self.player]["prog_percent"] = state.prog_items[self.player]["progs"] // self.num_prog
        return True

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        mapping = self.item_mapping_collect.get(item.name, None)
        if mapping is not None:
            state.prog_items[self.player][mapping[0]] -= mapping[1]

        state.prog_items[self.player]["progs"] -= 100 # Pre-multiply by 100 to not have to do it the following line
        state.prog_items[self.player]["prog_percent"] = state.prog_items[self.player]["progs"] // self.num_prog
        return True
