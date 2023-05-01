from typing import Dict, NamedTuple, List, Optional
from BaseClasses import Item, ItemClassification

BASE_ITEM_ID = 4000


class LandstalkerItem(Item):
    game: str = "Landstalker"
    price_in_shops: int


class LandstalkerItemData(NamedTuple):
    id: int
    classification: ItemClassification
    price_in_shops: int
    quantity: int


item_table: Dict[str, LandstalkerItemData] = {
    "EkeEke":               LandstalkerItemData(0,  ItemClassification.useful,      20,     0),  # Variable amount
    "Magic Sword":          LandstalkerItemData(1,  ItemClassification.useful,      300,    1),
    "Sword of Ice":         LandstalkerItemData(2,  ItemClassification.useful,      300,    1),
    "Thunder Sword":        LandstalkerItemData(3,  ItemClassification.useful,      500,    1),
    "Sword of Gaia":        LandstalkerItemData(4,  ItemClassification.progression, 300,    1),
    "Fireproof":            LandstalkerItemData(5,  ItemClassification.progression, 150,    1),
    "Iron Boots":           LandstalkerItemData(6,  ItemClassification.progression, 150,    1),
    "Healing Boots":        LandstalkerItemData(7,  ItemClassification.useful,      300,    1),
    "Snow Spikes":          LandstalkerItemData(8,  ItemClassification.progression, 400,    1),
    "Steel Breast":         LandstalkerItemData(9,  ItemClassification.useful,      200,    1),
    "Chrome Breast":        LandstalkerItemData(10, ItemClassification.useful,      350,    1),
    "Shell Breast":         LandstalkerItemData(11, ItemClassification.useful,      500,    1),
    "Hyper Breast":         LandstalkerItemData(12, ItemClassification.useful,      700,    1),
    "Mars Stone":           LandstalkerItemData(13, ItemClassification.useful,      150,    1),
    "Moon Stone":           LandstalkerItemData(14, ItemClassification.useful,      150,    1),
    "Saturn Stone":         LandstalkerItemData(15, ItemClassification.useful,      200,    1),
    "Venus Stone":          LandstalkerItemData(16, ItemClassification.useful,      300,    1),
    # Awakening Book: 17
    "Detox Grass":          LandstalkerItemData(18, ItemClassification.filler,      25,     9),
    "Statue of Gaia":       LandstalkerItemData(19, ItemClassification.filler,      75,     12),
    "Golden Statue":        LandstalkerItemData(20, ItemClassification.filler,      150,    10),
    "Mind Repair":          LandstalkerItemData(21, ItemClassification.filler,      25,     7),
    "Casino Ticket":        LandstalkerItemData(22, ItemClassification.progression, 50,     1),
    "Axe Magic":            LandstalkerItemData(23, ItemClassification.progression, 400,    1),
    "Blue Ribbon":          LandstalkerItemData(24, ItemClassification.filler,      50,     1),
    "Buyer Card":           LandstalkerItemData(25, ItemClassification.progression, 150,    1),
    "Lantern":              LandstalkerItemData(26, ItemClassification.progression, 200,    1),
    "Garlic":               LandstalkerItemData(27, ItemClassification.progression, 150,    2),
    "Anti Paralyze":        LandstalkerItemData(28, ItemClassification.filler,      20,     7),
    "Statue of Jypta":      LandstalkerItemData(29, ItemClassification.useful,      250,    1),
    "Sun Stone":            LandstalkerItemData(30, ItemClassification.progression, 300,    1),
    "Armlet":               LandstalkerItemData(31, ItemClassification.progression, 300,    1),
    "Einstein Whistle":     LandstalkerItemData(32, ItemClassification.progression, 200,    1),
    "Blue Jewel":           LandstalkerItemData(33, ItemClassification.progression, 500,    0),  # Detox Book in base game
    "Yellow Jewel":         LandstalkerItemData(34, ItemClassification.progression, 500,    0),  # AntiCurse Book in base game
    # Record Book: 35
    # Spell Book: 36
    # Hotel Register: 37
    # Island Map: 38
    "Lithograph":           LandstalkerItemData(39, ItemClassification.progression, 250,    1),
    "Red Jewel":            LandstalkerItemData(40, ItemClassification.progression, 500,    0),
    "Pawn Ticket":          LandstalkerItemData(41, ItemClassification.useful,      200,    4),
    "Purple Jewel":         LandstalkerItemData(42, ItemClassification.progression, 500,    0),
    "Gola's Eye":           LandstalkerItemData(43, ItemClassification.progression, 400,    1),
    "Death Statue":         LandstalkerItemData(44, ItemClassification.filler,      150,    1),
    "Dahl":                 LandstalkerItemData(45, ItemClassification.useful,      100,    18),
    "Restoration":          LandstalkerItemData(46, ItemClassification.filler,      40,     9),
    "Logs":                 LandstalkerItemData(47, ItemClassification.progression, 100,    2),
    "Oracle Stone":         LandstalkerItemData(48, ItemClassification.progression, 250,    1),
    "Idol Stone":           LandstalkerItemData(49, ItemClassification.progression, 200,    1),
    "Key":                  LandstalkerItemData(50, ItemClassification.progression, 150,    1),
    "Safety Pass":          LandstalkerItemData(51, ItemClassification.progression, 250,    1),
    "Green Jewel":          LandstalkerItemData(52, ItemClassification.progression, 500,    0),  # No52 in base game
    "Bell":                 LandstalkerItemData(53, ItemClassification.useful,      200,    1),
    "Short Cake":           LandstalkerItemData(54, ItemClassification.useful,      250,    1),
    "Gola's Nail":          LandstalkerItemData(55, ItemClassification.progression, 800,    1),
    "Gola's Horn":          LandstalkerItemData(56, ItemClassification.progression, 800,    1),
    "Gola's Fang":          LandstalkerItemData(57, ItemClassification.progression, 800,    1),
    # Broad Sword: 58
    # Leather Breast: 59
    # Leather Boots: 60
    # No Ring: 61
    "Life Stock":           LandstalkerItemData(62, ItemClassification.useful,      250,    0),  # Variable amount
    "No Item":              LandstalkerItemData(63, ItemClassification.filler,      0,      0),
    "1 Gold":               LandstalkerItemData(64, ItemClassification.filler,      0,      1),
    "20 Golds":             LandstalkerItemData(65, ItemClassification.filler,      0,      15),
    "50 Golds":             LandstalkerItemData(66, ItemClassification.useful,      0,      7),
    "100 Golds":            LandstalkerItemData(67, ItemClassification.useful,      0,      5),
    "200 Golds":            LandstalkerItemData(68, ItemClassification.useful,      0,      2),

    "Progressive Armor":    LandstalkerItemData(69, ItemClassification.useful,      250,    0)
}


def get_weighted_filler_item_names():
    weighted_item_names: List[str] = []
    for name, data in item_table.items():
        if data.classification == ItemClassification.filler:
            weighted_item_names += [name for _ in range(0, data.quantity)]
    return weighted_item_names


def build_item_name_to_id_table():
    item_name_to_id_table = {}
    for name, data in item_table.items():
        item_name_to_id_table[name] = data.id + BASE_ITEM_ID
    return item_name_to_id_table
