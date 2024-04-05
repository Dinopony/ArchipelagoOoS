import os
import logging

import yaml

from BaseClasses import Tutorial, Region, Location, LocationProgressType
from Fill import fill_restrictive, FillError
from Options import Accessibility
from worlds.AutoWorld import WebWorld, World
from .Data import *
from worlds.tloz_oos.data.Items import *
from .Logic import create_connections, apply_self_locking_rules
from .Options import *
from .PatcherDataWriter import write_patcherdata_file
from .data import LOCATIONS_DATA
from .data.Constants import *
from .data.Regions import REGIONS
from .Client import OracleOfSeasonsClient  # Unused, but required to register with BizHawkClient


class OracleOfSeasonsWeb(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Oracle of Seasons for Archipelago on your computer.",
        "English",
        "oos_setup_en.md",
        "oos_setup/en",
        ["Dinopony"]
    )]


class OracleOfSeasonsWorld(World):
    """
    The Legend of Zelda: Oracles of Seasons is one of the rare Capcom entries to the series.
    The seasons in the world of Holodrum have been a mess since Onox captured Din, the Oracle of Seasons.
    Gather the Essences of Nature, confront Onox and rescue Din to give nature some rest in Holodrum.
    """
    game = "The Legend of Zelda - Oracle of Seasons"
    options_dataclass = OracleOfSeasonsOptions
    options: OracleOfSeasonsOptions
    required_client_version = (0, 4, 4)
    web = OracleOfSeasonsWeb()

    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS

    pre_fill_items: List[Item]
    dungeon_items: List[Item]
    default_seasons: Dict[str, str]
    dungeon_entrances: Dict[str, str]
    portal_connections: Dict[str, str]
    lost_woods_item_sequence: List[str]
    old_man_rupee_values: Dict[str, int]
    shop_prices: Dict[str, int]
    samasa_gate_code: List[int]

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        self.pre_fill_items = []
        self.dungeon_items = []
        self.default_seasons = DEFAULT_SEASONS.copy()
        self.dungeon_entrances = DUNGEON_ENTRANCES.copy()
        self.portal_connections = PORTAL_CONNECTIONS.copy()
        self.lost_woods_item_sequence = LOST_WOODS_ITEM_SEQUENCE.copy()
        self.old_man_rupee_values = OLD_MAN_RUPEE_VALUES.copy()
        self.samasa_gate_code = SAMASA_GATE_CODE.copy()
        self.shop_prices = SHOP_PRICES_DIVIDERS.copy()

    def fill_slot_data(self) -> dict:
        # Put options that are useful to the tracker inside slot data
        options = ["goal", "death_link",
                   # Logic-impacting options
                   "logic_difficulty", "horon_village_season", "warp_to_start",
                   "shuffle_dungeons", "shuffle_portals", "lost_woods_item_sequence",
                   "duplicate_seed_tree", "default_seed",
                   # Locations
                   "shuffle_golden_ore_spots", "shuffle_old_men", "advance_shop",
                   # Requirements
                   "required_essences", "tarm_gate_required_jewels", "treehouse_old_man_requirement",
                   "sign_guy_requirement", "golden_beasts_requirement",
                   ]

        slot_data = self.options.as_dict(*options)
        slot_data["animal_companion"] = COMPANIONS[self.options.animal_companion.value]
        slot_data["default_seed"] = SEED_ITEMS[self.options.default_seed.value]

        slot_data["default_seasons_option"] = self.options.default_seasons.current_key
        slot_data["default_seasons"] = {}
        for region_name, season in self.default_seasons.items():
            slot_data["default_seasons"][REGIONS_CONVERSION_TABLE[region_name]] = season
        if self.options.horon_village_season == "vanilla":
            slot_data["default_seasons"][REGIONS_CONVERSION_TABLE["HORON_VILLAGE"]] = "chaotic"

        slot_data["dungeon_entrances"] = self.dungeon_entrances
        slot_data["portal_connections"] = self.portal_connections

        return slot_data

    def generate_early(self):
        self.restrict_non_local_items()
        self.randomize_default_seasons()
        self.randomize_old_men()

        if self.options.shuffle_dungeons == "shuffle":
            shuffled_entrances = list(self.dungeon_entrances.values())
            self.random.shuffle(shuffled_entrances)
            self.dungeon_entrances = dict(zip(self.dungeon_entrances, shuffled_entrances))

        if self.options.shuffle_portals == "shuffle":
            self.shuffle_portals()

        if self.options.lost_woods_item_sequence == "randomized":
            # Pick 4 random seasons & directions (no direction can be "right", and last one has to be "left")
            authorized_directions = [direction for direction in DIRECTIONS if direction != "right"]
            self.lost_woods_item_sequence = []
            for i in range(4):
                self.lost_woods_item_sequence.append(self.random.choice(SEASONS))
                self.lost_woods_item_sequence.append(self.random.choice(authorized_directions) if i < 3 else "left")

        if self.options.samasa_gate_code == "randomized":
            self.samasa_gate_code = []
            for i in range(self.options.samasa_gate_code_length.value):
                self.samasa_gate_code.append(self.random.randint(0, 3))

        self.randomize_shop_prices()

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it's incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity_small_keys:
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]
        if not self.options.keysanity_boss_keys:
            self.options.non_local_items.value -= self.item_name_groups["Boss Keys"]
        if not self.options.keysanity_maps_compasses:
            self.options.non_local_items.value -= self.item_name_groups["Dungeon Maps"]
            self.options.non_local_items.value -= self.item_name_groups["Compasses"]

    def randomize_default_seasons(self):
        if self.options.default_seasons == "randomized":
            for region in self.default_seasons:
                self.default_seasons[region] = self.random.choice(SEASONS)
        elif self.options.default_seasons.current_key.endswith("singularity"):
            single_season = self.options.default_seasons.current_key.replace("_singularity", "")
            if single_season == "random":
                single_season = self.random.choice(SEASONS)
            for region in self.default_seasons:
                self.default_seasons[region] = single_season

    def shuffle_portals(self):
        shuffled_portals = list(self.portal_connections.values())
        self.random.shuffle(shuffled_portals)
        self.portal_connections = dict(zip(self.portal_connections, shuffled_portals))

        # If accessibility is not locations, don't perform any check on what was randomly picked
        if self.options.accessibility != Accessibility.option_locations:
            return

        # If accessibility IS locations, we need to ensure that Temple Remains upper portal doesn't lead to the volcano
        # that can be triggered to open Temple Remains cave, since it would make it unreachable forever.
        # In that case, just swap it with a random other portal.
        if self.portal_connections["temple remains upper portal"] == "subrosia portal 6":
            other_portals = [key for key in PORTAL_CONNECTIONS.keys() if key != "temple remains upper portal"]
            portal_to_swap = self.random.choice(other_portals)
            self.portal_connections["temple remains upper portal"] = self.portal_connections[portal_to_swap]
            self.portal_connections[portal_to_swap] = "subrosia portal 6"

    def randomize_old_men(self):
        if self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_shuffled_values:
            shuffled_rupees = list(self.old_man_rupee_values.values())
            self.random.shuffle(shuffled_rupees)
            self.old_man_rupee_values = dict(zip(self.old_man_rupee_values, shuffled_rupees))
        elif self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_random_values:
            for key in self.old_man_rupee_values.keys():
                sign = self.random.choice([-1, 1])
                self.old_man_rupee_values[key] = self.random.choice(get_old_man_values_pool()) * sign
        elif self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_random_positive_values:
            for key in self.old_man_rupee_values.keys():
                self.old_man_rupee_values[key] = self.random.choice(get_old_man_values_pool())

    def randomize_shop_prices(self):
        prices_pool = get_prices_pool()
        self.random.shuffle(prices_pool)
        global_prices_factor = self.options.shop_prices_factor.value / 100.0
        for key, divider in self.shop_prices.items():
            floating_price = prices_pool.pop() * global_prices_factor / divider
            for i, value in enumerate(VALID_RUPEE_VALUES):
                if value > floating_price:
                    self.shop_prices[key] = VALID_RUPEE_VALUES[i-1]
                    break

    def location_is_active(self, location_name, location_data):
        if "conditional" not in location_data or location_data["conditional"] is False:
            return True

        region_id = location_data["region_id"]
        if region_id == "advance shop":
            return self.options.advance_shop.value
        if region_id.startswith("subrosia") and region_id.endswith("digging spot"):
            return self.options.shuffle_golden_ore_spots != "vanilla"
        if location_name in RUPEE_OLD_MAN_LOCATIONS:
            return self.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_turn_into_locations

        return False

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)
        if local:
            location.item_rule = lambda item: item.player == self.player

    def create_regions(self):
        # Create regions
        for region_name in REGIONS:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Create locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not self.location_is_active(location_name, location_data):
                continue

            is_local = "local" in location_data and location_data["local"] is True
            self.create_location(location_data['region_id'], location_name, is_local)

        self.create_events()
        self.exclude_problematic_locations()

    def create_event(self, region_name, event_item_name):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(Item(event_item_name, ItemClassification.progression, None, self.player))

    def create_events(self):
        self.create_event("subrosian smithy bell", "Pirate's Bell")
        self.create_event("maku seed", "Maku Seed")

        if self.options.goal == OracleOfSeasonsGoal.option_beat_onox:
            self.create_event("onox beaten", "_beaten_game")
        elif self.options.goal == OracleOfSeasonsGoal.option_beat_ganon:
            self.create_event("ganon beaten", "_beaten_game")

        self.create_event("spool stump", "_reached_spool_stump")
        self.create_event("temple remains lower stump", "_reached_remains_stump")
        self.create_event("temple remains upper stump", "_reached_remains_stump")
        self.create_event("d1 stump", "_reached_eyeglass_stump")
        self.create_event("d2 stump", "_reached_d2_stump")
        self.create_event("d5 stump", "_reached_eyeglass_stump")
        self.create_event("sunken city dimitri", "_saved_dimitri_in_sunken_city")
        self.create_event("ghastly stump", "_reached_ghastly_stump")
        self.create_event("coast stump", "_reached_coast_stump")
        self.create_event("subrosia market sector", "_reached_rosa")
        self.create_event("subrosian dance hall", "_reached_subrosian_dance_hall")
        self.create_event("subrosia pirates sector", "_met_pirates")
        self.create_event("tower of autumn", "_opened_tower_of_autumn")
        self.create_event("d2 moblin chest", "_reached_d2_bracelet_room")
        self.create_event("d5 drop ball", "_dropped_d5_magnet_ball")
        self.create_event("d8 SE crystal", "_dropped_d8_SE_crystal")
        self.create_event("d8 NE crystal", "_dropped_d8_NE_crystal")
        self.create_event("d2 rupee room", "_reached_d2_rupee_room")
        self.create_event("d6 rupee room", "_reached_d6_rupee_room")

        # Don't create an event for the triggerable volcano in Subrosia if portals layout make it unreachable, since
        # events are technically progression and generator doesn't like locked progression. At all.
        if self.portal_connections["temple remains upper portal"] != "subrosia portal 6":
            self.create_event("bomb temple remains", "_triggered_volcano")

        self.create_event("golden darknut", "_beat_golden_darknut")
        self.create_event("golden lynel", "_beat_golden_lynel")
        self.create_event("golden octorok", "_beat_golden_octorok")
        self.create_event("golden moblin", "_beat_golden_moblin")

        self.create_event("d4 miniboss room wild embers", "_wild_ember_seeds")
        self.create_event("d5 armos chest", "_wild_ember_seeds")
        self.create_event("d7 entrance wild embers", "_wild_ember_seeds")
        self.create_event("frypolar room wild mystery", "_wild_mystery_seeds")

        # Create event items to represent rupees obtained from Old Men, unless they are turned into locations
        if self.options.shuffle_old_men != OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
            for region_name in self.old_man_rupee_values:
                self.create_event(region_name, "rupees from " + region_name)

    def exclude_problematic_locations(self):
        locations_to_exclude = []
        # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
        # essences than this goal to hold anything of value
        if self.options.required_essences < 7:
            locations_to_exclude.append("Horon Village: Item Inside Maku Tree (7+ Essences)")
            if self.options.required_essences < 5:
                locations_to_exclude.append("Horon Village: Item Inside Maku Tree (5+ Essences)")
                if self.options.required_essences < 3:
                    locations_to_exclude.append("Horon Village: Item Inside Maku Tree (3+ Essences)")
        if self.options.required_essences < self.options.treehouse_old_man_requirement:
            locations_to_exclude.append("Holodrum Plain: Old Man in Treehouse")

        # If Temple Remains upper portal is connected to triggerable volcano portal in Subrosia, this makes a check
        # in the bombable cave of Temple Remains unreachable forever. Exclude it in such conditions.
        if self.portal_connections["temple remains upper portal"] == "subrosia portal 6":
            locations_to_exclude.append("Temple Remains: Item in Cave Behind Rockslide")

        for name in locations_to_exclude:
            self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED

    def set_rules(self):
        create_connections(self.multiworld, self.player)
        apply_self_locking_rules(self.multiworld, self.player)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("_beaten_game", self.player)

    def create_item(self, name: str) -> Item:
        ap_code = self.item_name_to_id[name]
        classification = ITEMS_DATA[name]["classification"]

        # A few items become progression only in hard logic
        progression_items_in_hard_logic = ["Expert's Ring", "Fist Ring", "Swimmer's Ring"]
        if self.options.logic_difficulty == "hard" and name in progression_items_in_hard_logic:
            classification = ItemClassification.progression

        return Item(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        item_pool_dict = {}
        for loc_name, loc_data in LOCATIONS_DATA.items():
            if "randomized" in loc_data and loc_data["randomized"] is False:
                item = self.create_item(loc_data['vanilla_item'])
                location = self.multiworld.get_location(loc_name, self.player)
                location.place_locked_item(item)
                continue
            if not self.location_is_active(loc_name, loc_data):
                continue
            if "vanilla_item" not in loc_data:
                continue

            item_name = loc_data['vanilla_item']
            if "Ring" in item_name:
                item_name = "Random Ring"

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # Perform adjustments on the item pool
        item_pool_adjustements = [
            ["Flute", COMPANIONS[self.options.animal_companion.value] + "'s Flute"],  # Put a specific flute
            ["Ricky's Gloves", "Progressive Sword"],    # Ricky's gloves are useless in current logic
            ["Gasha Seed", "Seed Satchel"],             # Add a 3rd satchel that is usually obtained in linked games (99 seeds)
            ["Gasha Seed", "Bombs (10)"],               # Add one more bomb compared to vanilla to reach 99 max bombs
            ["Gasha Seed", "Rupees (200)"],             # Too many Gasha Seeds in vanilla pool, add more rupees and ore instead
            ["Gasha Seed", "Ore Chunks (50)"],          # ^
            ["Gasha Seed", "Ore Chunks (50)"],          # ^
            ["Gasha Seed", "Ore Chunks (50)"],          # ^
        ]

        fools_ore_item = "Fool's Ore"
        if self.options.fools_ore == OracleOfSeasonsFoolsOre.option_excluded:
            fools_ore_item = "Gasha Seed"
        item_pool_adjustements.append(["Rod of Seasons", fools_ore_item]) # No lone rod of seasons supported for now

        for i, pair in enumerate(item_pool_adjustements):
            original_name = pair[0]
            replacement_name = pair[1]
            item_pool_dict[original_name] -= 1
            item_pool_dict[replacement_name] = item_pool_dict.get(replacement_name, 0) + 1

        # If Master Keys replace Small Keys, remove all Small Keys but one for every dungeon
        removed_keys = 0
        if self.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled:
            for small_key_name in ITEM_GROUPS["Small Keys"]:
                removed_keys += item_pool_dict[small_key_name] - 1
                del item_pool_dict[small_key_name]
            for small_key_name in ITEM_GROUPS["Master Keys"]:
                item_pool_dict[small_key_name] = 1
        # If Master Keys replace Boss Keys, remove Boss Keys from item pool
        if self.options.master_keys == OracleOfSeasonsMasterKeys.option_all_dungeon_keys:
            for boss_key_name in ITEM_GROUPS["Boss Keys"]:
                removed_keys += 1
                del item_pool_dict[boss_key_name]
        for i in range(removed_keys):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1

        return item_pool_dict

    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()

        # Create items following the dictionary that was previously constructed
        self.create_rings(item_pool_dict["Random Ring"])
        del item_pool_dict["Random Ring"]

        for item_name, quantity in item_pool_dict.items():
            for i in range(quantity):
                if ("Small Key" in item_name or "Master Key" in item_name) and not self.options.keysanity_small_keys:
                    self.dungeon_items.append(self.create_item(item_name))
                elif "Boss Key" in item_name and not self.options.keysanity_boss_keys:
                    self.dungeon_items.append(self.create_item(item_name))
                elif ("Compass" in item_name or "Dungeon Map" in item_name) and not self.options.keysanity_maps_compasses:
                    self.dungeon_items.append(self.create_item(item_name))
                else:
                    self.multiworld.itempool.append(self.create_item(item_name))

    def create_rings(self, amount):
        # Get a subset of as many rings as needed, with a potential filter on quality depending on chosen options
        ring_names = [name for name, idata in ITEMS_DATA.items() if "ring" in idata and idata["ring"] is True]
        if self.options.ring_quality == "only_useful":
            forbidden_classes = [ItemClassification.filler, ItemClassification.trap]
            ring_names = [name for name in ring_names if ITEMS_DATA[name]["classification"] not in forbidden_classes]

        self.random.shuffle(ring_names)
        del ring_names[amount:]
        for ring_name in ring_names:
            self.multiworld.itempool.append(self.create_item(ring_name))

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        self.pre_fill_seeds()
        self.pre_fill_dungeon_items()

    def pre_fill_dungeon_items(self):
        # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
        # of those which makes them pretty crowded.
        # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
        # To circumvent this, we perform a restricted pre-fill here, placing only those dungeon items
        # before anything else.
        collection_state = self.multiworld.get_all_state(False)

        for i in range(0, 9):
            # Build a list of locations in this dungeon
            dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                      if "dungeon" in loc and loc["dungeon"] == i]
            dungeon_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in dungeon_location_names]

            # Build a list of dungeon items that are "confined" (i.e. must be placed inside this dungeon)
            # See `create_items` to see how `self.dungeon_items` is populated depending on current options.
            confined_dungeon_items = [item for item in self.dungeon_items if item.name.endswith(f"({DUNGEON_NAMES[i]})")]
            if len(confined_dungeon_items) == 0:
                continue  # This list might be empty with some keysanity options
            for item in confined_dungeon_items:
                collection_state.remove(item)

            # Perform a prefill to place confined items inside locations of this dungeon
            for attempts_remaining in range(2, -1, -1):
                self.random.shuffle(dungeon_locations)
                try:
                    fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                                     single_player_placement=True, lock=True, allow_excluded=True)
                    break
                except FillError as exc:
                    if attempts_remaining == 0:
                        raise exc
                    logging.debug(f"Failed to shuffle dungeon items for player {self.player}. Retrying...")

    def pre_fill_seeds(self) -> None:
        # The prefill algorithm for seeds has a few constraints:
        #   - it needs to place the "default seed" into Horon Village seed tree
        #   - it needs to place a random seed on the "duplicate tree" (can be Horon's tree)
        #   - it needs to place one of each seed on the 5 remaining trees
        # This has a few implications:
        #   - if Horon is the duplicate tree, this is the simplest case: we just place a random seed in Horon's tree
        #     and scatter the 5 seed types on the 5 other trees
        #   - if Horon is NOT the duplicate tree, we need to remove Horon's seed from the pool of 5 seeds to scatter
        #     and put a random seed inside the duplicate tree. Then, we place the 4 remaining seeds on the 4 remaining
        #     trees
        TREES_TABLE = {
            OracleOfSeasonsDuplicateSeedTree.option_horon_village: "Horon Village: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_woods_of_winter: "Woods of Winter: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_north_horon: "Holodrum Plain: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_spool_swamp: "Spool Swamp: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_sunken_city: "Sunken City: Seed Tree",
            OracleOfSeasonsDuplicateSeedTree.option_tarm_ruins: "Tarm Ruins: Seed Tree",
        }
        duplicate_tree_name = TREES_TABLE[self.options.duplicate_seed_tree.value]

        def place_seed(seed_name: str, location_name: str):
            seed_item = self.create_item(seed_name)
            self.multiworld.get_location(location_name, self.player).place_locked_item(seed_item)
            self.pre_fill_items.append(seed_item)

        seeds_to_place = set([name for name in SEED_ITEMS])

        manually_placed_trees = ["Horon Village: Seed Tree", duplicate_tree_name]
        trees_to_process = [name for name in TREES_TABLE.values() if name not in manually_placed_trees]

        # Place default seed type in Horon Village tree
        place_seed(SEED_ITEMS[self.options.default_seed.value], "Horon Village: Seed Tree")

        # If duplicate tree is not Horon's, remove Horon seed from the pool of placeable seeds
        if duplicate_tree_name != "Horon Village: Seed Tree":
            seeds_to_place.remove(SEED_ITEMS[self.options.default_seed.value])
            place_seed(self.random.choice(SEED_ITEMS), duplicate_tree_name)

        # Place remaining seeds on remaining trees
        self.random.shuffle(trees_to_process)
        for seed in seeds_to_place:
            place_seed(seed, trees_to_process.pop())

    def get_filler_item_name(self) -> str:
        FILLER_ITEM_NAMES = [
            "Rupees (1)", "Rupees (5)", "Rupees (10)", "Rupees (20)", "Rupees (30)", "Rupees (50)",
            "Ore Chunks (50)", "Gasha Seed", "Potion"
        ]
        return self.random.choice(FILLER_ITEM_NAMES)

    def generate_output(self, output_directory: str):
        write_patcherdata_file(self, output_directory)

    def write_spoiler(self, spoiler_handle):
        spoiler_handle.write(f"\n\nDefault Seasons ({self.multiworld.player_name[self.player]}):\n")
        for region_name, season in self.default_seasons.items():
            spoiler_handle.write(f"\t- {REGIONS_CONVERSION_TABLE[region_name]} --> {season}\n")

        if self.options.shuffle_dungeons != "vanilla":
            spoiler_handle.write(f"\nDungeon Entrances ({self.multiworld.player_name[self.player]}):\n")
            for entrance, dungeon in self.dungeon_entrances.items():
                spoiler_handle.write(f"\t- {entrance} --> {dungeon.replace('enter ', '')}\n")

        if self.options.shuffle_portals != "vanilla":
            spoiler_handle.write(f"\nSubrosia Portals ({self.multiworld.player_name[self.player]}):\n")
            for portal_holo, portal_sub in self.portal_connections.items():
                spoiler_handle.write(f"\t- {PORTALS_CONVERSION_TABLE[portal_holo]} --> {PORTALS_CONVERSION_TABLE[portal_sub]}\n")
