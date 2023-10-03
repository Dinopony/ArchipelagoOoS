from BaseClasses import Tutorial, Region, Entrance, ItemClassification, Item
from worlds.AutoWorld import WebWorld, World
from .Options import metroid_prime_option_definitions
from RandovaniaLogicConverter import RandovaniaLogicConverter, RandovaniaLogicData

from .data import header as MetroidPrimeHeader
from .data import (ChozoRuins, EndGame, FrigateOrpheon, ImpactCrater, MagmoorCaverns, PhazonMines,
                   PhendranaDrifts, TallonOverworld)

BASE_LOCATION_ID = 100000000
BASE_ITEM_ID = 100000000

METROID_PRIME_REGIONS = [
    ChozoRuins.DATA, FrigateOrpheon.DATA, ImpactCrater.DATA, MagmoorCaverns.DATA, PhazonMines.DATA,
    PhendranaDrifts.DATA, TallonOverworld.DATA, EndGame.DATA
]


class MetroidPrimeWeb(WebWorld):
    theme = "grass"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Randovania on your computer.",
        "English",
        "randovania_setup_en.md",
        "randovania_setup/en",
        ["Dinopony", "JustinDM", "Toasterparty"]
    )]


class MetroidPrimeWorld(World):
    """
    Metroid Prime for the Nintendo GameCube™
    """
    game = "Metroid Prime"
    option_definitions = metroid_prime_option_definitions
    topology_present = True
    data_version = 1
    required_client_version = (0, 4, 2)
    web = MetroidPrimeWeb()

    item_name_to_id = RandovaniaLogicConverter.build_item_name_to_id_table(MetroidPrimeHeader.DATA, BASE_ITEM_ID)
    location_name_to_id = RandovaniaLogicConverter.build_location_name_to_id_table(METROID_PRIME_REGIONS,
                                                                                   BASE_LOCATION_ID)

    # TODO: Currently, Flamethrower is considered progression

    def __init__(self, multiworld: "MultiWorld", player: int):
        super().__init__(multiworld, player)

        # TODO: Temporary hack, need to handle variable missile quantity
        MetroidPrimeHeader.DATA["resource_database"]["items"]["Missile"]["long_name"] = "Missile Launcher"

        logic_data = RandovaniaLogicData(MetroidPrimeHeader.DATA, METROID_PRIME_REGIONS, BASE_LOCATION_ID, BASE_ITEM_ID)
        self.logic_converter = RandovaniaLogicConverter(self.multiworld, self.player, logic_data)

        # Add unused artifacts as starting inventory
        artifacts = [item for item in self.item_name_to_id if item.startswith("Artifact")]
        for artifact in artifacts[self.get_setting('artifact_target'):]:
            self.multiworld.start_inventory[self.player].value[artifact] = 1

        # TODO: Handle options that are not simply forwarded

    def get_setting(self, name: str):
        return getattr(self.multiworld, name)[self.player]

    def create_regions(self):
        self.logic_converter.create_regions()

        # Create the hardcoded starting "Menu" region
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        # Add a path from menu to seed's starting location
        entrance = Entrance(self.player, f"Game start", menu_region)
        menu_region.exits.append(entrance)
        entrance.connect(self.multiworld.get_region("Tallon Overworld/Landing Site/Ship", self.player))
        # TODO: Handle variable / random start location

    def create_item(self, name: str, classification: ItemClassification = ItemClassification.filler) -> Item:
        return Item(name, classification, self.item_name_to_id[name], self.player)

    def create_items(self):
        self.logic_converter.create_items()

        items_distribution = self.get_setting("item_distribution")
        for item_name, quantity in items_distribution.items():
            is_filler = (item_name.endswith("Expansion") or item_name.endswith("Tank"))
            classification = ItemClassification.filler if is_filler else ItemClassification.progression
            self.multiworld.itempool += [self.create_item(item_name, classification) for _ in range(quantity)]

        # Add the right amount of artifacts depending on settings
        artifacts = [item for item in self.item_name_to_id if item.startswith("Artifact")]
        for artifact in artifacts[:self.get_setting('artifact_target')]:
            self.multiworld.itempool += [self.create_item(artifact, ItemClassification.progression)]

        remaining_items = len(self.multiworld.get_unfilled_locations(self.player)) - len(self.multiworld.itempool)
        self.multiworld.itempool += [self.create_item("Nothing") for _ in range(remaining_items)]

    def set_rules(self):
        # Done in create_regions, is that an issue? -> can be delayed if needed
        self.logic_converter.set_rules()

    def fill_slot_data(self) -> dict:
        # Nothing required, as everything is contained inside the .rdvgame file
        return {}

    def generate_output(self, output_directory: str) -> None:
        with open(output_directory + '/graphviz.txt', 'w') as f:
            f.write('digraph {\n')
            for region in self.multiworld.regions:
                for entrance in region.entrances:
                    f.write(f'"{entrance.parent_region.name}" -> "{entrance.connected_region.name}"\n')
            f.write('}')

        # TODO: Generate .rdvgame file here
        # TODO: Convert "Nothing" to "Energy Transfer Module"
