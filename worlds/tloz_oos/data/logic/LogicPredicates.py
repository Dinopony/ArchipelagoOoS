from BaseClasses import CollectionState
from Options import Accessibility
from worlds.tloz_oos.data.Constants import DUNGEON_NAMES, SEASON_ITEMS, ESSENCES, JEWELS


# Items predicates ############################################################

def oos_has_sword(state: CollectionState, player: int, accept_biggoron: bool = True):
    return any([
        state.has("Progressive Sword", player),
        accept_biggoron and state.has("Biggoron's Sword", player)
    ])


def oos_has_noble_sword(state: CollectionState, player: int):
    return state.has("Progressive Sword", player, 2)


def oos_has_shield(state: CollectionState, player: int):
    return state.has("Progressive Shield", player)


def oos_has_fools_ore(state: CollectionState, player: int):
    return state.has("Fool's Ore", player)


def oos_has_feather(state: CollectionState, player: int):
    return state.has("Progressive Feather", player)


def oos_has_cape(state: CollectionState, player: int):
    return state.has("Progressive Feather", player, 2)


def oos_has_satchel(state: CollectionState, player: int, level: int = 1):
    return state.has("Seed Satchel", player, level)


def oos_has_slingshot(state: CollectionState, player: int):
    return state.has("Progressive Slingshot", player)


def oos_has_hyper_slingshot(state: CollectionState, player: int):
    return state.has("Progressive Slingshot", player, 2)


def oos_has_boomerang(state: CollectionState, player: int):
    return state.has("Progressive Boomerang", player)


def oos_has_magic_boomerang(state: CollectionState, player: int):
    return state.has("Progressive Boomerang", player, 2)


def oos_has_bracelet(state: CollectionState, player: int):
    return state.has("Power Bracelet", player)


def oos_has_shovel(state: CollectionState, player: int):
    return state.has("Shovel", player)


def oos_has_flippers(state: CollectionState, player: int):
    return state.has("Flippers", player)


def oos_has_season(state: CollectionState, player: int, season: str):
    return state.has(SEASON_ITEMS[season], player)


def oos_has_summer(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS["summer"], player)


def oos_has_spring(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS["spring"], player)


def oos_has_winter(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS["winter"], player)


def oos_has_autumn(state: CollectionState, player: int):
    return state.has(SEASON_ITEMS["autumn"], player)


def oos_has_magnet_gloves(state: CollectionState, player: int):
    return state.has("Magnetic Gloves", player)


def oos_has_ember_seeds(state: CollectionState, player: int):
    return any([
        state.has("Ember Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "ember",
        (state.has("_wild_ember_seeds", player) and oos_option_medium_logic(state, player))
    ])


def oos_has_scent_seeds(state: CollectionState, player: int):
    return state.has("Scent Seeds", player) or state.multiworld.worlds[player].options.default_seed == "scent"


def oos_has_pegasus_seeds(state: CollectionState, player: int):
    return state.has("Pegasus Seeds", player) or state.multiworld.worlds[player].options.default_seed == "pegasus"


def oos_has_mystery_seeds(state: CollectionState, player: int):
    return any([
        state.has("Mystery Seeds", player),
        state.multiworld.worlds[player].options.default_seed == "mystery",
        (state.has("_wild_mystery_seeds", player) and oos_option_medium_logic(state, player))
    ])


def oos_has_gale_seeds(state: CollectionState, player: int):
    return state.has("Gale Seeds", player) or state.multiworld.worlds[player].options.default_seed == "gale"


def oos_has_small_keys(state: CollectionState, player: int, dungeon_id: int, amount: int = 1):
    return state.has(f"Small Key ({DUNGEON_NAMES[dungeon_id]})", player, amount)


def oos_has_boss_key(state: CollectionState, player: int, dungeon_id: int):
    return state.has(f"Boss Key ({DUNGEON_NAMES[dungeon_id]})", player)


# Options and generation predicates ###########################################

def oos_option_medium_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty in ["medium", "hard"]


def oos_option_hard_logic(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.logic_difficulty == "hard"


def oos_option_allow_warp_to_start(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.warp_to_start.value


def oos_option_shuffled_dungeons(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.shuffle_dungeons != "vanilla"


def oos_is_companion_ricky(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "ricky"


def oos_is_companion_moosh(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "moosh"


def oos_is_companion_dimitri(state: CollectionState, player: int):
    return state.multiworld.worlds[player].options.animal_companion == "dimitri"


def oos_get_default_season(state: CollectionState, player: int, area_name: str):
    return state.multiworld.worlds[player].default_seasons[area_name]


def oos_can_remove_season(state: CollectionState, player: int, season: str):
    # Test if player has any other season than the one we want to remove
    return any(
        [state.has(item_name, player) for season_name, item_name in SEASON_ITEMS.items() if season_name != season])


def oos_has_essences(state: CollectionState, player: int, target_count: int):
    essence_count = [state.has(essence, player) for essence in ESSENCES].count(True)
    return essence_count >= target_count


def oos_has_essences_for_maku_seed(state: CollectionState, player: int):
    return oos_has_essences(state, player, state.multiworld.worlds[player].options.required_essences.value)


def oos_has_essences_for_treehouse(state: CollectionState, player: int):
    return oos_has_essences(state, player, state.multiworld.worlds[player].options.treehouse_old_man_requirement.value)


def oos_has_required_jewels(state: CollectionState, player: int):
    target_count = state.multiworld.worlds[player].options.tarm_gate_required_jewels.value
    count = [state.has(jewel, player) for jewel in JEWELS].count(True)
    return count >= target_count


def oos_can_reach_lost_woods_pedestal(state: CollectionState, player: int):
    world = state.multiworld.worlds[player]
    return all([
        any([
            world.options.lost_woods_item_sequence == "vanilla",
            all([
                oos_can_use_ember_seeds(state, player, False),
                state.has("Phonograph", player)
            ])
        ]),
        "winter" not in world.lost_woods_item_sequence or oos_has_winter(state, player),
        "spring" not in world.lost_woods_item_sequence or oos_has_spring(state, player),
        "summer" not in world.lost_woods_item_sequence or oos_has_summer(state, player),
        "autumn" not in world.lost_woods_item_sequence or oos_has_autumn(state, player)
    ])


def oos_can_beat_required_golden_beasts(state: CollectionState, player: int):
    GOLDEN_BEAST_EVENTS = ["_beat_golden_darknut", "_beat_golden_lynel", "_beat_golden_moblin", "_beat_golden_octorok"]
    beast_count = [state.has(beast, player) for beast in GOLDEN_BEAST_EVENTS].count(True)
    return beast_count >= state.multiworld.worlds[player].options.golden_beasts_requirement.value


# Various item predicates ###########################################

def oos_has_rupees(state: CollectionState, player: int, amount: int):
    if oos_can_farm_rupees(state, player):
        return True

    rupees = state.count("Rupees (1)", player)
    rupees += state.count("Rupees (5)", player) * 5
    rupees += state.count("Rupees (10)", player) * 10
    rupees += state.count("Rupees (20)", player) * 20
    rupees += state.count("Rupees (50)", player) * 50
    rupees += state.count("Rupees (100)", player) * 100

    # Secret rooms inside D2 and D6 containing loads of rupees
    if state.has("_reached_d2_rupee_room", player):
        rupees += 150
    if state.has("_reached_d6_rupee_room", player):
        rupees += 90

    # Old men giving and taking rupees
    world = state.multiworld.worlds[player]
    for region_name, value in world.old_man_rupee_values.items():
        event_name = "rupees from " + region_name
        if state.has(event_name, player):
            rupees += value

    return rupees >= amount


def oos_can_farm_rupees(state: CollectionState, player: int):
    # Having Ember Seeds and a weapon or a shovel is enough to guarantee that we can reach
    # a significant amount of rupees
    return all([
        oos_can_use_ember_seeds(state, player, False),
        (oos_has_sword(state, player) or oos_has_shovel(state, player))
    ])


def oos_has_ore(state: CollectionState, player: int, amount: int):
    if oos_can_farm_ore(state, player):
        return True
    return False


def oos_can_farm_ore(state: CollectionState, player: int):
    return any([
        oos_has_shovel(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_magic_boomerang(state, player),
            oos_has_sword(state, player)
        ]),
        all([
            oos_option_hard_logic(state, player),
            state.has("_reached_subrosian_dance_hall", player)
        ])
    ])


def oos_can_date_rosa(state: CollectionState, player: int):
    return state.has("_reached_rosa", player) and state.has("Ribbon", player)


def oos_can_trigger_far_switch(state: CollectionState, player: int):
    return any([
        oos_has_boomerang(state, player),
        oos_has_bombs(state, player),
        oos_has_slingshot(state, player),
        all([
            oos_option_hard_logic(state, player),
            oos_has_sword(state, player, False),
            state.has("Energy Ring", player)
        ])
        # TODO: Regular beams?
    ])


def oos_has_rod(state: CollectionState, player: int):
    return any([
        oos_has_winter(state, player),
        oos_has_summer(state, player),
        oos_has_spring(state, player),
        oos_has_autumn(state, player)
    ])


def oos_has_bombs(state: CollectionState, player: int, amount: int = 1):
    if state.has("Bombs (10)", player, amount):
        return True

    return all([
        # With hard logic, player is expected to know they can get free bombs
        # from D2 moblin room even if they never had bombs before
        (amount == 1),
        oos_option_medium_logic(state, player),
        state.has("_reached_d2_bracelet_room", player),
        oos_can_harvest_regrowing_bush(state, player, False)
    ])


def oos_has_flute(state: CollectionState, player: int):
    return any([
        oos_can_summon_ricky(state, player),
        oos_can_summon_moosh(state, player),
        oos_can_summon_dimitri(state, player)
    ])


def oos_can_summon_ricky(state: CollectionState, player: int):
    return state.has("Ricky's Flute", player)


def oos_can_summon_moosh(state: CollectionState, player: int):
    return state.has("Moosh's Flute", player)


def oos_can_summon_dimitri(state: CollectionState, player: int):
    return state.has("Dimitri's Flute", player)


# Jump-related predicates ###########################################

def oos_can_jump_1_wide_liquid(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_feather(state, player),
        all([
            oos_option_medium_logic(state, player),
            can_summon_companion,
            oos_can_summon_ricky(state, player)
        ])
    ])


def oos_can_jump_2_wide_liquid(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player)
        ]),
        all([
            # Hard logic expects bomb jumps over 2-wide liquids
            oos_option_hard_logic(state, player),
            oos_has_feather(state, player),
            oos_has_bombs(state, player)
        ])
    ])


def oos_can_jump_3_wide_liquid(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_option_hard_logic(state, player),
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player),
            oos_has_bombs(state, player),
        ])
    ])


def oos_can_jump_4_wide_liquid(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        any([
            oos_can_use_pegasus_seeds(state, player),
            all([
                # Hard logic expects player to be able to cape bomb-jump above 4-wide liquids
                oos_option_hard_logic(state, player),
                oos_has_bombs(state, player)
            ])
        ])
    ])


def oos_can_jump_5_wide_liquid(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


def oos_can_jump_6_wide_liquid(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


def oos_can_jump_1_wide_pit(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_feather(state, player),
        all([
            can_summon_companion,
            any([
                oos_can_summon_moosh(state, player),
                oos_can_summon_ricky(state, player)
            ])
        ])
    ])


def oos_can_jump_2_wide_pit(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_has_feather(state, player),
            any([
                # Medium logic expects player to be able to jump above 2-wide pits without pegasus seeds
                oos_option_medium_logic(state, player),
                oos_can_use_pegasus_seeds(state, player)
            ])
        ])
    ])


def oos_can_jump_3_wide_pit(state: CollectionState, player: int):
    return any([
        oos_has_cape(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_feather(state, player),
            oos_can_use_pegasus_seeds(state, player),
        ])
    ])


def oos_can_jump_4_wide_pit(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        any([
            oos_option_medium_logic(state, player),
            oos_can_use_pegasus_seeds(state, player),
        ])
    ])


def oos_can_jump_5_wide_pit(state: CollectionState, player: int):
    return all([
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


def oos_can_jump_6_wide_pit(state: CollectionState, player: int):
    return all([
        oos_option_medium_logic(state, player),
        oos_has_cape(state, player),
        oos_can_use_pegasus_seeds(state, player),
    ])


# Seed-related predicates ###########################################

def oos_can_use_seeds(state: CollectionState, player: int):
    return oos_has_slingshot(state, player) or oos_has_satchel(state, player)


def oos_can_use_ember_seeds(state: CollectionState, player: int, accept_mystery_seeds: bool):
    return all([
        oos_can_use_seeds(state, player),
        any([
            oos_has_ember_seeds(state, player),
            all([
                # Medium logic expects the player to know they can use mystery seeds
                # to randomly get the ember effect in some cases
                accept_mystery_seeds,
                oos_option_medium_logic(state, player),
                oos_has_mystery_seeds(state, player),
            ])
        ])
    ])


def oos_can_use_scent_seeds(state: CollectionState, player: int):
    return all([
        oos_can_use_seeds(state, player),
        oos_has_scent_seeds(state, player)
    ])


def oos_can_use_pegasus_seeds(state: CollectionState, player: int):
    return all([
        # Unlike other seeds, pegasus only have an interesting effect with the satchel
        oos_has_satchel(state, player),
        oos_has_pegasus_seeds(state, player)
    ])


def oos_can_warp_using_gale_seeds(state: CollectionState, player: int):
    return all([
        oos_has_satchel(state, player),
        oos_has_gale_seeds(state, player)
    ])


def oos_can_use_gale_seeds_offensively(state: CollectionState, player: int):
    # If we don't have gale seeds or aren't at least in medium logic, don't even try
    if not oos_has_gale_seeds(state, player) or not oos_option_medium_logic(state, player):
        return False

    return any([
        oos_has_slingshot(state, player),
        all([
            oos_has_satchel(state, player),
            any([
                oos_option_hard_logic(state, player),
                oos_has_feather(state, player)
            ]),
        ])
    ])


def oos_can_warp(state: CollectionState, player: int):
    # Never expect points of no return / risky checks for casual logic
    if not oos_option_medium_logic(state, player):
        return False
    return oos_can_warp_using_gale_seeds(state, player) or oos_option_allow_warp_to_start(state, player)


def oos_can_use_mystery_seeds(state: CollectionState, player: int):
    return all([
        oos_can_use_seeds(state, player),
        oos_has_mystery_seeds(state, player)
    ])


# Break / kill predicates ###########################################

def oos_can_break_bush(state: CollectionState, player: int, can_summon_companion: bool = False):
    return any([
        oos_has_sword(state, player),
        oos_has_magic_boomerang(state, player),
        oos_has_bracelet(state, player),
        (can_summon_companion and oos_has_flute(state, player)),
        all([
            # Consumables need at least medium logic, since they need a good knowledge of the game
            # not to be frustrating
            oos_option_medium_logic(state, player),
            any([
                oos_has_bombs(state, player, 2),
                oos_can_use_ember_seeds(state, player, False),
                (oos_has_slingshot(state, player) and oos_has_gale_seeds(state, player)),
            ])
        ]),
    ])


def oos_can_harvest_regrowing_bush(state: CollectionState, player: int, allow_bombs: bool = True):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        (allow_bombs and oos_has_bombs(state, player))
    ])


def oos_can_break_mushroom(state: CollectionState, player: int, can_use_companion: bool):
    return any([
        oos_has_bracelet(state, player),
        all([
            oos_option_medium_logic(state, player),
            any([
                oos_has_magic_boomerang(state, player),
                can_use_companion and oos_can_summon_dimitri(state, player)
            ])
        ]),
    ])


def oos_can_break_pot(state: CollectionState, player: int):
    return any([
        oos_has_bracelet(state, player),
        oos_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player)
    ])


def oos_can_break_flowers(state: CollectionState, player: int, can_summon_companion: bool):
    return any([
        oos_has_sword(state, player),
        oos_has_magic_boomerang(state, player),
        (can_summon_companion and oos_has_flute(state, player)),
        all([
            # Consumables need at least medium logic, since they need a good knowledge of the game
            # not to be frustrating
            oos_option_medium_logic(state, player),
            any([
                oos_has_bombs(state, player, 2),
                oos_can_use_ember_seeds(state, player, False),
                (oos_has_slingshot(state, player) and oos_has_gale_seeds(state, player)),
            ])
        ]),
    ])


def oos_can_break_crystal(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_bombs(state, player),
        oos_has_bracelet(state, player),
        all([
            oos_option_hard_logic(state, player),
            state.has("Expert's Ring", player)
        ])
    ])


def oos_can_break_sign(state: CollectionState, player: int):
    return any([
        oos_has_noble_sword(state, player),
        state.has("Biggoron's Sword", player),
        oos_has_bracelet(state, player),
        oos_can_use_ember_seeds(state, player, False),
        oos_has_magic_boomerang(state, player)
    ])


def oos_can_harvest_tree(state: CollectionState, player: int, can_use_companion: bool):
    return all([
        oos_can_use_seeds(state, player),
        any([
            oos_has_sword(state, player),
            oos_has_fools_ore(state, player),
            oos_has_rod(state, player),
            oos_can_punch(state, player),
            all([
                can_use_companion,
                oos_option_medium_logic(state, player),
                oos_can_summon_dimitri(state, player)
            ])
        ])
    ])


def oos_can_push_enemy(state: CollectionState, player: int):
    return any([
        oos_has_rod(state, player),
        oos_has_shield(state, player)
    ])


def oos_can_kill_normal_enemy(state: CollectionState, player: int, pit_available: bool = False):
    # If a pit is avaiable nearby, it can be used to put the enemies inside using
    # items that are usually non-lethal
    if pit_available and oos_can_push_enemy(state, player):
        return True

    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_can_kill_normal_using_satchel(state, player),
        oos_can_kill_normal_using_slingshot(state, player),
        (oos_option_medium_logic(state, player) and oos_has_bombs(state, player, 4)),
        oos_can_punch(state, player)
    ])


def oos_can_kill_normal_using_satchel(state: CollectionState, player: int):
    # Expect a 50+ seed satchel to ensure we can chain dungeon rooms to some extent if that's our only kill option
    if not oos_has_satchel(state, player, 2):
        return False

    return any([
        # Casual logic => only ember
        oos_has_ember_seeds(state, player),
        all([
            # Medium logic => allow scent or gale+feather
            oos_option_medium_logic(state, player),
            any([
                oos_has_scent_seeds(state, player),
                oos_has_mystery_seeds(state, player),
                all([
                    oos_has_gale_seeds(state, player),
                    oos_has_feather(state, player)
                ])
            ])
        ]),
        all([
            # Hard logic => allow gale without feather
            oos_option_hard_logic(state, player),
            oos_has_gale_seeds(state, player)
        ])
    ])


def oos_can_kill_normal_using_slingshot(state: CollectionState, player: int):
    # Expect a 50+ seed satchel to ensure we can chain dungeon rooms to some extent if that's our only kill option
    if not oos_has_satchel(state, player, 2):
        return False

    return all([
        oos_has_slingshot(state, player),
        any([
            oos_has_ember_seeds(state, player),
            oos_has_scent_seeds(state, player),
            all([
                oos_option_medium_logic(state, player),
                any([
                    oos_has_mystery_seeds(state, player),
                    oos_has_gale_seeds(state, player),
                ])
            ])
        ])
    ])


def oos_can_kill_armored_enemy(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        all([
            oos_has_satchel(state, player, 2),  # Expect a 50+ seeds satchel to be able to chain rooms in dungeons
            oos_has_scent_seeds(state, player),
            any([
                oos_has_slingshot(state, player),
                oos_option_medium_logic(state, player)
            ])
        ]),
        oos_can_punch(state, player)
    ])


def oos_can_kill_stalfos(state: CollectionState, player: int):
    return any([
        oos_can_kill_normal_enemy(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_rod(state, player)
        ])
    ])


def oos_can_punch(state: CollectionState, player: int):
    return all([
        oos_option_hard_logic(state, player),
        any([
            state.has("Fist Ring", player),
            state.has("Expert's Ring", player)
        ])
    ])


def oos_can_trigger_lever(state: CollectionState, player: int):
    return any([
        oos_can_trigger_lever_from_minecart(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_trigger_lever_from_minecart(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_has_boomerang(state, player),
        oos_has_rod(state, player),

        # TODO: Test that to ensure our understanding is right
        oos_can_use_scent_seeds(state, player),
        oos_can_use_mystery_seeds(state, player),
        oos_has_slingshot(state, player),  # any seed works using slingshot
    ])


def oos_can_kill_d2_hardhat(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_has_boomerang(state, player),
        oos_can_push_enemy(state, player),
        all([
            oos_option_medium_logic(state, player),
            any([
                oos_has_slingshot(state, player),
                all([
                    oos_option_hard_logic(state, player),
                    oos_has_satchel(state, player),
                ])
            ]),
            any([
                oos_has_scent_seeds(state, player),
                oos_has_gale_seeds(state, player),
            ])
        ]),
        all([
            oos_option_hard_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_kill_d2_far_moblin(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        oos_can_kill_normal_using_slingshot(state, player),
        all([
            oos_has_feather(state, player),
            oos_can_push_enemy(state, player),
        ]),
        all([
            oos_option_hard_logic(state, player),
            any([
                oos_can_use_ember_seeds(state, player, False),
                oos_can_punch(state, player)
            ])
        ])
    ])


def oos_can_flip_spiked_beetle(state: CollectionState, player: int):
    return any([
        oos_has_shield(state, player),
        all([
            oos_option_medium_logic(state, player),
            oos_has_shovel(state, player)
        ])
    ])


def oos_can_kill_spiked_beetle(state: CollectionState, player: int):
    return any([
        all([  # Regular flip + kill
            oos_can_flip_spiked_beetle(state, player),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                oos_can_kill_normal_using_satchel(state, player),
                oos_can_kill_normal_using_slingshot(state, player)
            ])
        ]),
        # Instant kill using Gale Seeds
        oos_can_use_gale_seeds_offensively(state, player)
    ])


def oos_can_kill_magunesu(state: CollectionState, player: int):
    return any([
        oos_has_sword(state, player),
        oos_has_fools_ore(state, player),
        # state.has("expert's ring", player)
    ])


# Action predicates ###########################################

def oos_can_remove_snow(state: CollectionState, player: int, can_summon_companion: bool):
    return oos_has_shovel(state, player) or (can_summon_companion and oos_has_flute(state, player))


def oos_can_swim(state: CollectionState, player: int, can_summon_companion: bool):
    return oos_has_flippers(state, player) or (can_summon_companion and oos_can_summon_dimitri(state, player))


def oos_can_remove_rockslide(state: CollectionState, player: int, can_summon_companion: bool):
    return oos_has_bombs(state, player) or (can_summon_companion and oos_can_summon_ricky(state, player))


# Season in region predicates ##########################################

def oos_season_in_spool_swamp(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "SPOOL_SWAMP") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_spool_stump", player)


def oos_season_in_eyeglass_lake(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "EYEGLASS_LAKE") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_eyeglass_stump", player)


def oos_season_in_temple_remains(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "TEMPLE_REMAINS") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_remains_stump", player)


def oos_season_in_north_horon(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "NORTH_HORON") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_ghastly_stump", player)


def oos_season_in_western_coast(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "WESTERN_COAST") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_coast_stump", player)


def oos_season_in_eastern_suburbs(state: CollectionState, player: int, season: str):
    return (oos_get_default_season(state, player, "EASTERN_SUBURBS") == season
            or oos_has_season(state, player, season))


def oos_season_in_sunken_city(state: CollectionState, player: int, season: str):
    return (oos_get_default_season(state, player, "SUNKEN_CITY") == season
            or oos_has_season(state, player, season))


def oos_season_in_woods_of_winter(state: CollectionState, player: int, season: str):
    return (oos_get_default_season(state, player, "WOODS_OF_WINTER") == season
            or oos_has_season(state, player, season))


def oos_season_in_central_woods_of_winter(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "WOODS_OF_WINTER") == season:
        return True
    return oos_has_season(state, player, season) and state.has("_reached_d2_stump", player)


def oos_season_in_mt_cucco(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "SUNKEN_CITY") == season:
        return True
    return oos_has_season(state, player, season)


def oos_season_in_lost_woods(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "LOST_WOODS") == season:
        return True
    return oos_has_season(state, player, season)


def oos_season_in_tarm_ruins(state: CollectionState, player: int, season: str):
    if oos_get_default_season(state, player, "TARM_RUINS") == season:
        return True
    return oos_has_season(state, player, season)


def oos_season_in_horon_village(state: CollectionState, player: int, season: str):
    if state.multiworld.worlds[player].options.horon_village_season == "chaotic":
        return True
    if oos_get_default_season(state, player, "HORON_VILLAGE") == season:
        return True
    return oos_has_season(state, player, season)


def region_holds_small_key(state: CollectionState, player: int, region_name: str, dungeon: int):
    if state.multiworld.worlds[player].options.accessibility == Accessibility.option_locations:
        return False

    region = state.multiworld.get_region(region_name, player)
    items_in_region = [location.item for location in region.locations if location.item is not None]
    for item in items_in_region:
        if item.name == f"Small Key ({DUNGEON_NAMES[dungeon]})" and item.player == player:
            return True
    return False
