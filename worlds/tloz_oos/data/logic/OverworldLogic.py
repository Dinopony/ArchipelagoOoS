from worlds.tloz_oos.data.logic.LogicPredicates import *


def make_holodrum_logic(player: int):
    return [
        ["Menu", "horon village", False, None],

        ["horon village", "mayor's gift", False, None],
        ["horon village", "vasu's gift", False, None],
        ["horon village", "mayor's house secret room", False, lambda state: oos_has_bombs(state, player)],
        ["horon village", "horon heart piece", False, lambda state: oos_can_use_ember_seeds(state, player, False)],
        ["horon village", "dr. left reward", False, lambda state: oos_can_use_ember_seeds(state, player, True)],
        ["horon village", "old man in horon", False, lambda state: oos_can_use_ember_seeds(state, player, False)],
        ["horon village", "old man trade", False, lambda state: any([
            state.has("Fish", player),
            oos_self_locking_item(state, player, "old man trade", "Fish")
        ])],
        ["horon village", "tick tock trade", False, lambda state: any([
            state.has("Wooden Bird", player),
            oos_self_locking_item(state, player, "tick tock trade", "Wooden Bird")
        ])],
        ["horon village", "maku tree", False, lambda state: oos_has_sword(state, player, False)],
        ["horon village", "horon village SE chest", False, lambda state: all([
            oos_has_bombs(state, player),
            any([
                oos_can_swim(state, player, False),
                oos_season_in_horon_village(state, player, "winter"),
                oos_can_jump_2_wide_liquid(state, player)
            ])
        ])],
        ["horon village", "horon village SW chest", False, lambda state: all([
            oos_season_in_horon_village(state, player, "autumn"),
            oos_can_break_mushroom(state, player, True)
        ])],

        ["horon village", "maple trade", False, lambda state: all([
            oos_can_meet_maple(state, player),
            any([
                state.has("Lon Lon Egg", player),
                oos_self_locking_item(state, player, "maple trade", "Lon Lon Egg")
            ])
        ])],

        ["horon village", "horon village portal", False, lambda state: any([
            oos_has_magic_boomerang(state, player),
            oos_can_jump_6_wide_pit(state, player)
        ])],
        ["horon village portal", "horon village", False, lambda state: any([
            oos_can_trigger_lever(state, player),
            oos_can_jump_6_wide_pit(state, player)
        ])],

        ["horon village", "horon village tree", False, lambda state: oos_can_harvest_tree(state, player, True)],

        ["horon village", "horon shop", False, lambda state: oos_has_rupees(state, player, 200)],
        ["horon village", "advance shop", False, lambda state: oos_has_rupees(state, player, 400)],
        ["horon village", "member's shop", False, lambda state: all([
            state.has("Member's Card", player),
            oos_has_rupees(state, player, 600)
        ])],

        # WESTERN COAST ##############################################################################################

        ["horon village", "black beast's chest", False, lambda state: all([
            all([
                oos_has_slingshot(state, player),
                oos_can_use_ember_seeds(state, player, True),
            ]),
            oos_can_use_mystery_seeds(state, player),
            oos_can_kill_armored_enemy(state, player),
        ])],

        ["horon village", "d0 entrance", True, None],

        ["western coast after ship", "coast stump", False, lambda state: all([
            oos_has_bombs(state, player),
            any([
                oos_has_feather(state, player),
                oos_option_hard_logic(state, player)
            ])
        ])],

        ["western coast after ship",  "old man near western coast house", False, lambda state: \
            oos_can_use_ember_seeds(state, player, False)],

        ["western coast after ship", "graveyard (winter)", False, lambda state: all([
            oos_can_jump_3_wide_pit(state, player),
            oos_season_in_western_coast(state, player, "winter")
        ])],

        ["western coast after ship", "graveyard (autumn)", False, lambda state: all([
            oos_can_jump_3_wide_pit(state, player),
            oos_season_in_western_coast(state, player, "autumn")
        ])],

        ["western coast after ship", "graveyard (summer or spring)", False, lambda state: any([
            oos_can_jump_3_wide_pit(state, player),
            oos_season_in_western_coast(state, player, "summer")
        ])],

        ["graveyard (winter)", "d7 entrance", False, lambda state: oos_can_remove_snow(state, player, False)],
        ["graveyard (autumn)", "d7 entrance", False, None],
        ["graveyard (summer or spring)", "d7 entrance", False, None],

        ["d7 entrance", "graveyard (winter)", False, lambda state: \
            oos_get_default_season(state, player, "WESTERN_COAST") == "winter"],
        ["d7 entrance", "graveyard (autumn)", False, lambda state: \
            oos_get_default_season(state, player, "WESTERN_COAST") == "autumn"],
        ["d7 entrance", "graveyard (summer or spring)", False, lambda state: \
            oos_get_default_season(state, player, "WESTERN_COAST") in ["summer", "spring"]],

        ["graveyard (autumn)", "graveyard heart piece", False, lambda state: oos_can_break_mushroom(state, player, False)],

        # EASTERN SUBURBS #############################################################################################

        ["horon village", "suburbs", True, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["suburbs", "windmill heart piece", False, lambda state: oos_season_in_eastern_suburbs(state, player, "winter")],
        ["suburbs", "guru-guru trade", False, lambda state: any([
            state.has("Engine Grease", player),
            oos_self_locking_item(state, player, "guru-guru trade", "Engine Grease")
        ])],

        ["suburbs", "eastern suburbs spring cave", False, lambda state: all([
            oos_has_bracelet(state, player),
            oos_season_in_eastern_suburbs(state, player, "spring"),
            any([
                oos_has_magnet_gloves(state, player),
                oos_can_jump_3_wide_pit(state, player)
            ])
        ])],

        ["eastern suburbs portal", "suburbs", False, lambda state: oos_can_break_bush(state, player, False)],
        ["suburbs", "eastern suburbs portal", False, lambda state: oos_can_break_bush(state, player, True)],

        ["suburbs", "suburbs fairy fountain", True, lambda state: any([
            oos_can_swim(state, player, True),
            oos_can_jump_1_wide_liquid(state, player, True)
        ])],
        ["suburbs", "suburbs fairy fountain (winter)", True, lambda state: any([
            oos_season_in_eastern_suburbs(state, player, "winter")
        ])],
        ["suburbs fairy fountain (winter)", "suburbs fairy fountain", False, lambda state: \
            oos_can_remove_season(state, player, "winter")],
        ["suburbs fairy fountain", "suburbs fairy fountain (winter)", False, lambda state: \
            oos_has_winter(state, player)],

        ["suburbs fairy fountain", "sunken city", False, lambda state: \
            oos_season_in_eastern_suburbs(state, player, "spring")],
        ["sunken city", "suburbs fairy fountain", False, lambda state: any([
            oos_season_in_eastern_suburbs(state, player, "spring"),
            oos_can_warp(state, player)
        ])],

        # WOODS OF WINTER / 2D SECTOR ################################################################################

        ["suburbs fairy fountain (winter)", "moblin road", False, lambda state: None],
        ["moblin road", "suburbs fairy fountain (winter)", False, lambda state: \
            oos_season_in_eastern_suburbs(state, player, "winter")],

        ["sunken city", "moblin road", False, lambda state: all([
            oos_has_flippers(state, player),
            any([
                oos_get_default_season(state, player, "SUNKEN_CITY") != "winter",
                oos_can_remove_season(state, player, "winter")
            ]),
            any([
                oos_can_warp(state, player),
                all([
                    # We need both seasons to be able to climb back up
                    oos_season_in_eastern_suburbs(state, player, "winter"),
                    oos_has_spring(state, player)
                ])
            ])
        ])],

        ["moblin road", "woods of winter, 1st cave", False, lambda state: all([
            oos_can_remove_rockslide(state, player, True),
            oos_can_break_bush(state, player, False),
            any([
                oos_get_default_season(state, player, "WOODS_OF_WINTER") != "winter",
                oos_can_remove_season(state, player, "winter")
            ])
        ])],

        ["moblin road", "woods of winter, 2nd cave", False, lambda state: any([
            oos_can_swim(state, player, False),
            oos_can_jump_3_wide_liquid(state, player)
        ])],

        ["moblin road", "holly's house", False, lambda state: \
            oos_season_in_woods_of_winter(state, player, "winter")],

        ["moblin road", "old man near holly's house", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["moblin road", "woods of winter heart piece", False, lambda state: any([
            oos_can_swim(state, player, True),
            oos_has_bracelet(state, player),
            oos_can_jump_1_wide_liquid(state, player, True)
        ])],

        ["suburbs fairy fountain", "central woods of winter", False, lambda state: None],
        ["suburbs fairy fountain (winter)", "central woods of winter", False, lambda state: any([
            oos_can_jump_1_wide_pit(state, player, True),
            oos_can_remove_snow(state, player, True)
        ])],

        ["central woods of winter", "woods of winter tree", False, lambda state: oos_can_harvest_tree(state, player, True)],
        ["central woods of winter", "d2 entrance", True, lambda state: oos_can_break_bush(state, player, True)],
        ["central woods of winter", "cave outside D2", False, lambda state: all([
            oos_season_in_central_woods_of_winter(state, player, "autumn"),
            oos_can_break_mushroom(state, player, True),
            any([
                oos_can_jump_4_wide_pit(state, player),
                oos_has_magnet_gloves(state, player)
            ])
        ])],

        ["central woods of winter", "d2 stump", True, None],

        ["d2 stump", "d2 roof", True, lambda state: oos_has_bracelet(state, player)],
        ["d2 roof", "d2 alt entrances", True, lambda state: not oos_option_no_d2_alt_entrance(state, player)],

        # EYEGLASS LAKE SECTOR #########################################################################################

        ["horon village", "eyeglass lake, across bridge", False, lambda state: any([
            oos_can_jump_4_wide_pit(state, player),
            all([
                oos_season_in_eyeglass_lake(state, player, "autumn"),
                oos_has_feather(state, player)
            ])
        ])],

        ["horon village", "d1 stump", True, lambda state: oos_can_break_bush(state, player, True)],
        ["d1 stump", "north horon", True, lambda state: oos_has_bracelet(state, player)],
        ["d1 stump", "malon trade", False, lambda state: any([
            state.has("Cuccodex", player),
            oos_self_locking_item(state, player, "malon trade", "Cuccodex")
        ])],
        ["d1 stump", "d1 island", True, lambda state: oos_can_break_bush(state, player, True)],
        ["d1 stump", "old man near d1", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["d1 island", "d1 entrance", True, lambda state: state.has("Gnarled Key", player)],
        ["d1 island", "golden beasts old man", False, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, "summer"),
            oos_can_beat_required_golden_beasts(state, player)
        ])],

        ["d1 stump", "eyeglass lake (default)", True, lambda state: all([
            any([
                oos_season_in_eyeglass_lake(state, player, "spring"),
                oos_season_in_eyeglass_lake(state, player, "autumn"),
            ]),
            oos_can_jump_1_wide_pit(state, player, True),
            any([
                oos_can_swim(state, player, False),
                all([
                    # To be able to use Dimitri, we need the bracelet to throw him above the pit
                    oos_option_medium_logic(state, player),
                    oos_can_summon_dimitri(state, player),
                    oos_has_bracelet(state, player)
                ])
            ])
        ])],
        ["d1 stump", "eyeglass lake (dry)", True, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, "summer"),
            oos_can_jump_1_wide_pit(state, player, True)
        ])],
        ["d1 stump", "eyeglass lake (frozen)", True, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, "winter"),
            oos_can_jump_1_wide_pit(state, player, True)
        ])],

        ["d5 stump", "eyeglass lake (default)", True, lambda state: all([
            any([
                oos_season_in_eyeglass_lake(state, player, "spring"),
                oos_season_in_eyeglass_lake(state, player, "autumn"),
            ]),
            oos_can_swim(state, player, True)
        ])],
        ["d5 stump", "eyeglass lake (dry)", False, lambda state: all([
            oos_season_in_eyeglass_lake(state, player, "summer"),
            oos_can_swim(state, player, False)
        ])],
        ["d5 stump", "eyeglass lake (frozen)", True,
         lambda state: oos_season_in_eyeglass_lake(state, player, "winter")],

        ["eyeglass lake portal", "eyeglass lake (default)", False, lambda state: all([
            oos_get_default_season(state, player, "EYEGLASS_LAKE") in ["autumn", "spring"],
            oos_can_swim(state, player, False)
        ])],
        ["eyeglass lake (default)", "eyeglass lake portal", False, None],
        ["eyeglass lake portal", "eyeglass lake (frozen)", False, lambda state: all([
            oos_get_default_season(state, player, "EYEGLASS_LAKE") == "winter",
            any([
                oos_can_swim(state, player, False),
                oos_can_jump_5_wide_liquid(state, player)
            ])
        ])],
        ["eyeglass lake (frozen)", "eyeglass lake portal", False, lambda state: any([
            oos_can_swim(state, player, True),
            oos_can_jump_5_wide_liquid(state, player)
        ])],
        ["eyeglass lake portal", "eyeglass lake (dry)", False, lambda state: \
            oos_get_default_season(state, player, "EYEGLASS_LAKE") == "summer"],

        ["eyeglass lake (dry)", "dry eyeglass lake, west cave", False, lambda state: all([
            oos_can_remove_rockslide(state, player, True),
            oos_can_swim(state, player, False)  # chest is surrounded by water
        ])],

        ["d5 stump", "d5 entrance", False, lambda state: all([
            any([
                oos_has_autumn(state, player),
                # If we don't have autumn, we need to ensure we were able to reach that node with autumn as default
                # season without changing to another season which we wouldn't be able to revert back
                all([
                    oos_get_default_season(state, player, "EYEGLASS_LAKE") == "autumn",
                    oos_can_swim(state, player, False)
                ])
            ]),
            oos_can_break_mushroom(state, player, True)
        ])],
        ["d5 entrance", "d5 stump", False, lambda state: any([
            # Leaving D5 entrance is a risky action since you need quite a few things to be able to get
            # back to that entrance. Ensure player can warp if that's not the case.
            all([
                oos_can_jump_1_wide_pit(state, player, False),
                oos_has_autumn(state, player),
                oos_can_break_mushroom(state, player, True)
            ]),
            oos_can_warp(state, player)
        ])],

        ["d5 stump", "dry eyeglass lake, east cave", False, lambda state: all([
            oos_has_summer(state, player),
            oos_has_bracelet(state, player),
        ])],

        ["d5 entrance", "dry eyeglass lake, east cave", False, lambda state: all([
            oos_get_default_season(state, player, "EYEGLASS_LAKE") == "summer",
            oos_has_bracelet(state, player),
        ])],

        # NORTH HORON / HOLODRUM PLAIN ###############################################################################

        ["north horon", "north horon tree", False, lambda state: oos_can_harvest_tree(state, player, True)],
        ["north horon", "blaino prize", False, lambda state: oos_can_farm_rupees(state, player)],
        ["north horon", "cave north of D1", False, lambda state: all([
            oos_season_in_north_horon(state, player, "autumn"),
            oos_can_break_mushroom(state, player, True),
            oos_has_flippers(state, player)
        ])],
        ["north horon", "old man near blaino", False, lambda state: all([
            any([
                oos_season_in_north_horon(state, player, "summer"),
                oos_can_summon_ricky(state, player)
            ]),
            oos_can_use_ember_seeds(state, player, False)
        ])],
        ["north horon", "underwater item below natzu bridge", False, lambda state: oos_can_swim(state, player, False)],

        ["north horon", "temple remains lower stump", True, lambda state: oos_can_jump_3_wide_pit(state, player)],

        ["ghastly stump", "mrs. ruul trade", False, lambda state: any([
            state.has("Ghastly Doll", player),
            oos_self_locking_item(state, player, "mrs. ruul trade", "Ghastly Doll")
        ])],
        ["ghastly stump", "old man near mrs. ruul", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        ["north horon", "ghastly stump", True, lambda state: any([
            oos_can_jump_1_wide_pit(state, player, True),
            oos_season_in_north_horon(state, player, "winter")
        ])],

        ["spool swamp north", "ghastly stump", False, None],
        ["ghastly stump", "spool swamp north", False, lambda state: all([
            any([
                oos_season_in_north_horon(state, player, "summer"),
                oos_can_jump_4_wide_pit(state, player),
                oos_can_summon_ricky(state, player),
                oos_can_summon_moosh(state, player)
            ])
        ])],

        ["ghastly stump", "spool swamp south", True, lambda state: all([
            oos_can_swim(state, player, True),
            oos_can_break_bush(state, player, True),
        ])],

        # Goron Mountain <-> North Horon <-> D1 island <-> Spool swamp waterway
        ["spool swamp south", "d1 island", True, lambda state: oos_can_swim(state, player, True)],
        ["d1 island", "north horon", True, lambda state: oos_can_swim(state, player, True)],
        ["north horon", "goron mountain entrance", True, lambda state: oos_can_swim(state, player, True)],
        ["goron mountain entrance", "natzu region, across water", True, lambda state: oos_can_swim(state, player, True)],
        ["ghastly stump", "d1 island", True, lambda state: all([
            oos_can_break_bush(state, player, True),
            oos_can_swim(state, player, True)
        ])],

        ["d1 island", "old man in treehouse", False, lambda state: all([
            oos_can_swim(state, player, True),
            oos_has_essences_for_treehouse(state, player)
        ])],
        ["d1 island", "cave south of mrs. ruul", False, lambda state: oos_can_swim(state, player, False)],

        # SPOOL SWAMP #############################################################################################

        ["spool swamp north", "spool swamp tree", False, lambda state: oos_can_harvest_tree(state, player, True)],

        ["spool swamp north", "floodgate keeper's house", False, lambda state: any([
            oos_can_trigger_lever(state, player),
            all([
                oos_option_hard_logic(state, player),
                oos_has_bracelet(state, player)
            ])
        ])],

        ["spool swamp north", "spool swamp digging spot", False, lambda state: all([
            oos_season_in_spool_swamp(state, player, "summer"),
            oos_has_shovel(state, player)
        ])],

        ["floodgate keeper's house", "spool stump", False, lambda state: all([
            any([
                oos_can_use_pegasus_seeds(state, player),
                oos_has_flippers(state, player),
                oos_has_feather(state, player)
            ]),
            oos_has_bracelet(state, player),
            state.has("Floodgate Key", player)
        ])],

        ["spool stump", "d3 entrance", False, lambda state: oos_season_in_spool_swamp(state, player, "summer")],
        ["d3 entrance", "spool stump", False, lambda state: any([
            # Jumping down D3 entrance without having a way to put summer is a risky situation, so expect player
            # to have a way to warp out
            oos_season_in_spool_swamp(state, player, "summer"),
            oos_can_warp(state, player)
        ])],

        ["spool stump", "spool swamp middle", False, lambda state: any([
            oos_get_default_season(state, player, "SPOOL_SWAMP") != 'spring',
            oos_can_remove_season(state, player, 'spring'),
            oos_has_flippers(state, player),
            oos_can_summon_dimitri(state, player)
        ])],

        ["spool swamp middle", "spool swamp south gasha spot", False, lambda state: oos_can_summon_ricky(state, player)],
        ["spool swamp south gasha spot", "spool swamp middle", False, lambda state: any([
            oos_has_feather(state, player),
            oos_can_break_bush(state, player, True)
        ])],

        ["spool swamp south gasha spot", "spool swamp portal", True, lambda state: oos_has_bracelet(state, player)],

        ["spool swamp middle", "spool swamp south", True, lambda state: any([
            oos_can_jump_2_wide_pit(state, player),
            oos_can_summon_moosh(state, player),
            oos_can_summon_dimitri(state, player),
            oos_has_flippers(state, player)
        ])],

        ["spool swamp south", "spool swamp south (winter)", False, lambda state: \
            oos_season_in_spool_swamp(state, player, "winter")],
        ["spool swamp south", "spool swamp south (spring)", False, lambda state: \
            oos_season_in_spool_swamp(state, player, "spring")],
        ["spool swamp south", "spool swamp south (summer)", False, lambda state: \
            oos_season_in_spool_swamp(state, player, "summer")],
        ["spool swamp south", "spool swamp south (autumn)", False, lambda state: \
            oos_season_in_spool_swamp(state, player, "autumn")],
        ["spool swamp south (winter)", "spool swamp south", False, None],
        ["spool swamp south (spring)", "spool swamp south", False, None],
        ["spool swamp south (summer)", "spool swamp south", False, None],
        ["spool swamp south (autumn)", "spool swamp south", False, None],

        ["spool swamp south (spring)", "spool swamp south gasha spot", False, lambda state: \
            oos_can_break_flowers(state, player, True)
         ],
        ["spool swamp south (winter)", "spool swamp south gasha spot", False, lambda state: \
            oos_can_remove_snow(state, player, True)
         ],
        ["spool swamp south (summer)", "spool swamp south gasha spot", False, None],
        ["spool swamp south (autumn)", "spool swamp south gasha spot", False, None],

        ["spool swamp south gasha spot", "spool swamp south (spring)", False, lambda state: all([
            oos_season_in_spool_swamp(state, player, "spring"),
            oos_can_break_flowers(state, player, True)
        ])],
        ["spool swamp south gasha spot", "spool swamp south (winter)", False, lambda state: all([
            oos_season_in_spool_swamp(state, player, "winter"),
            oos_can_remove_snow(state, player, True)
        ])],
        ["spool swamp south gasha spot", "spool swamp south (summer)", False, lambda state: \
            oos_season_in_spool_swamp(state, player, "summer")],
        ["spool swamp south gasha spot", "spool swamp south (autumn)", False, lambda state: \
            oos_season_in_spool_swamp(state, player, "autumn")],

        ["spool swamp south (winter)", "spool swamp cave", False, lambda state: all([
            oos_can_remove_snow(state, player, True),
            oos_can_remove_rockslide(state, player, True)
        ])],

        ["spool swamp south (spring)", "spool swamp heart piece", False, lambda state: \
            oos_can_swim(state, player, True)],

        # NATZU REGION #############################################################################################

        ["north horon", "natzu west", True, lambda state: any([
            oos_can_jump_1_wide_pit(state, player, True),
            oos_can_swim(state, player, True)
        ])],

        ["natzu west", "natzu west (ricky)", True, lambda state: oos_is_companion_ricky(state, player)],
        ["natzu west", "natzu west (moosh)", True, lambda state: oos_is_companion_moosh(state, player)],
        ["natzu west", "natzu west (dimitri)", True, lambda state: oos_is_companion_dimitri(state, player)],

        ["natzu east (ricky)", "sunken city", True, lambda state: oos_is_companion_ricky(state, player)],
        ["natzu east (moosh)", "sunken city", True, lambda state: all([
            oos_is_companion_moosh(state, player),
            any([
                oos_can_summon_moosh(state, player),
                oos_can_jump_3_wide_liquid(state, player)  # Not a liquid, but it's a diagonal jump so that's the same
            ])
        ])],
        ["natzu east (dimitri)", "sunken city", True, lambda state: all([
            oos_is_companion_dimitri(state, player),
            oos_can_jump_1_wide_pit(state, player, False)
        ])],
        ["natzu east (dimitri)", "natzu region, across water", False, lambda state: \
            oos_can_jump_5_wide_liquid(state, player)],

        ["natzu west (ricky)", "natzu east (ricky)", True, lambda state: oos_can_summon_ricky(state, player)],
        ["natzu west (moosh)", "natzu east (moosh)", True, lambda state: any([
            oos_can_summon_moosh(state, player),
            all([
                oos_option_medium_logic(state, player),
                oos_can_break_bush(state, player, True),
                oos_can_jump_3_wide_pit(state, player)
            ])
        ])],
        ["natzu west (dimitri)", "natzu east (dimitri)", True, lambda state: oos_can_swim(state, player, True)],

        ["natzu east (ricky)", "moblin keep bridge", False, None],
        ["natzu east (moosh)", "moblin keep bridge", False, lambda state: any([
            oos_can_summon_moosh(state, player),
            all([
                oos_can_break_bush(state, player),
                oos_can_jump_3_wide_pit(state, player)
            ])
        ])],
        ["natzu east (dimitri)", "moblin keep bridge", False, lambda state: any([
            oos_can_summon_dimitri(state, player),
            all([
                oos_option_hard_logic(state, player),
                state.has("Swimmer's Ring", player)
            ])
        ])],
        ["moblin keep bridge", "moblin keep", False, lambda state: any([
            oos_has_flippers(state, player),
            oos_can_jump_4_wide_liquid(state, player)
        ])],
        ["moblin keep", "moblin keep chest", False, lambda state: any([
            oos_has_bracelet(state, player)
        ])],
        ["moblin keep", "sunken city", False, lambda state: oos_can_warp(state, player)],

        ["natzu east (ricky)", "natzu river bank", True, lambda state: oos_can_summon_ricky(state, player)],
        ["natzu east (moosh)", "natzu river bank", True, lambda state: oos_is_companion_moosh(state, player)],
        ["natzu east (dimitri)", "natzu river bank", True, lambda state: oos_is_companion_dimitri(state, player)],
        ["natzu river bank", "goron mountain entrance", True, lambda state: oos_can_swim(state, player, True)],

        # SUNKEN CITY ############################################################################################

        ["sunken city", "sunken city tree", False, lambda state: all([
            any([
                oos_has_feather(state, player),
                oos_has_flippers(state, player),
                oos_can_summon_dimitri(state, player),
                oos_get_default_season(state, player, "SUNKEN_CITY") == "winter"
            ]),
            oos_can_harvest_tree(state, player, True)
        ])],

        ["sunken city", "sunken city dimitri", False, lambda state: any([
            oos_can_summon_dimitri(state, player),
            all([
                oos_has_bombs(state, player),
                any([
                    oos_has_feather(state, player),
                    oos_has_flippers(state, player),
                    oos_get_default_season(state, player, "SUNKEN_CITY") == "winter"
                ])
            ])
        ])],

        ["sunken city", "ingo trade", False, lambda state: any([
            state.has("Goron Vase", player),
            oos_self_locking_item(state, player, "ingo trade", "Goron Vase")
        ])],
        ["sunken city", "syrup trade", False, lambda state: all([
            any([
                oos_get_default_season(state, player, "SUNKEN_CITY") == "winter",
                all([
                    oos_has_winter(state, player),
                    any([
                        oos_can_swim(state, player, True),
                        state.has("_saved_dimitri_in_sunken_city", player)
                    ])
                ])
            ]),
            state.has("Mushroom", player)
        ])],
        ["syrup trade", "syrup shop", False, lambda state: oos_has_rupees(state, player, 800)],

        # Use Dimitri to get the tree seeds, using dimitri to get seeds being medium difficulty
        ["sunken city dimitri", "sunken city tree", False,lambda state: all([
            oos_option_medium_logic(state, player),
            oos_can_use_seeds(state, player)
        ])],

        ["sunken city dimitri", "master diver's challenge", False, lambda state: all([
            oos_has_sword(state, player, False),
            any([
                oos_has_feather(state, player),
                oos_has_flippers(state, player)
            ])
        ])],

        ["sunken city dimitri", "master diver's reward", False, lambda state: any([
            state.has("Master's Plaque", player),
            oos_self_locking_item(state, player, "master diver's reward", "Master's Plaque")
        ])],
        ["sunken city dimitri", "chest in master diver's cave", False, None],

        ["sunken city", "sunken city, summer cave", False, lambda state: all([
            any([
                oos_get_default_season(state, player, "SUNKEN_CITY") == "summer",
                oos_has_summer(state, player)
            ]),
            oos_has_flippers(state, player),
            oos_can_break_bush(state, player, False)
        ])],

        ["mount cucco", "sunken city", False, lambda state: oos_has_flippers(state, player)],
        ["sunken city", "mount cucco", False, lambda state: all([
            oos_has_flippers(state, player),
            oos_season_in_sunken_city(state, player, "summer")
        ])],

        # MT. CUCCO / GORON MOUNTAINS ##############################################################################

        ["mount cucco", "mt. cucco portal", True, None],

        ["mount cucco", "rightmost rooster ledge", False, lambda state: all([
            any([  # to reach the rooster
                all([
                    oos_season_in_mt_cucco(state, player, "spring"),
                    any([
                        oos_can_break_flowers(state, player, False),
                        # Moosh can break flowers one way, but it won't be of any help when coming back so we need
                        # to be able to warp out
                        state.has("Spring Banana", player) and oos_can_warp(state, player),
                    ])
                ]),
                oos_option_hard_logic(state, player) and oos_can_warp(state, player),
            ]),
            oos_has_bracelet(state, player),  # to grab the rooster
        ])],

        ["rightmost rooster ledge", "mt. cucco, platform cave", False, None],
        ["rightmost rooster ledge", "spring banana tree", False, lambda state: all([
            oos_has_feather(state, player),
            oos_season_in_mt_cucco(state, player, "spring"),
            any([  # can harvest tree
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player)
            ])
        ])],

        ["mount cucco", "mt. cucco, talon's cave entrance", False, lambda state: \
            oos_season_in_mt_cucco(state, player, "spring")],

        ["mt. cucco, talon's cave entrance", "talon trade", False, lambda state: state.has("Megaphone", player)],
        ["talon trade", "mt. cucco, talon's cave", False, None],

        ["mt. cucco, talon's cave entrance", "mt. cucco heart piece", False, None],

        ["mt. cucco, talon's cave entrance", "diving spot outside D4", False, lambda state: oos_has_flippers(state, player)],

        ["mt. cucco, talon's cave entrance", "dragon keyhole", False, lambda state: all([
            oos_has_winter(state, player),  # to reach cave
            oos_has_feather(state, player),  # to jump in cave
            oos_has_bracelet(state, player)  # to grab the rooster
        ])],

        ["dragon keyhole", "d4 entrance", False, lambda state: all([
            state.has("Dragon Key", player),
            oos_has_summer(state, player)
        ])],
        ["d4 entrance", "mt. cucco, talon's cave entrance", False, lambda state: oos_can_warp(state, player)],

        ["mount cucco", "goron mountain, across pits", False, lambda state: any([
            state.has("Spring Banana", player),
            oos_can_jump_4_wide_pit(state, player),
        ])],

        ["mount cucco", "goron blocked cave entrance", False, lambda state: any([
                oos_can_remove_snow(state, player, False),
                state.has("Spring Banana", player)
        ])],
        ["goron blocked cave entrance", "mount cucco", False, lambda state: \
            oos_can_remove_snow(state, player, False)],

        ["goron blocked cave entrance", "goron mountain", True, lambda state: oos_has_bracelet(state, player)],

        ["goron blocked cave entrance", "goron's gift", False, lambda state: oos_has_bombs(state, player)],

        ["goron mountain", "biggoron trade", False, lambda state: all([
            oos_can_jump_1_wide_liquid(state, player, False),
            any([
                state.has("Lava Soup", player),
                oos_self_locking_item(state, player, "biggoron trade", "Lava Soup")
            ])
        ])],

        ["goron mountain", "chest in goron mountain", False, lambda state: all([
            oos_has_bombs(state, player),
            oos_can_jump_3_wide_liquid(state, player)
        ])],
        ["goron mountain", "old man in goron mountain", False, lambda state: \
            oos_can_use_ember_seeds(state, player, False)],

        ["goron mountain entrance", "goron mountain", True, lambda state: any([
            oos_has_flippers(state, player),
            oos_can_jump_4_wide_liquid(state, player),
        ])],

        ["goron mountain entrance", "temple remains lower stump", True, lambda state: \
            oos_can_jump_3_wide_pit(state, player)],

        # TARM RUINS ###############################################################################################

        ["spool swamp north", "tarm ruins", False, lambda state: oos_has_required_jewels(state, player)],

        ["tarm ruins", "lost woods stump", False, lambda state: all([
            oos_has_summer(state, player),
            oos_has_winter(state, player),
            oos_has_autumn(state, player),
            oos_can_break_mushroom(state, player, False)
        ])],

        ["lost woods stump", "lost woods", False, lambda state: oos_can_reach_lost_woods_pedestal(state, player)],

        ["lost woods stump", "d6 sector", False, lambda state: all([
            oos_has_winter(state, player),
            oos_has_autumn(state, player),
            oos_has_spring(state, player),
            oos_has_summer(state, player),
        ])],

        ["d6 sector", "tarm ruins tree", False, lambda state: oos_can_harvest_tree(state, player, False)],
        ["d6 sector", "tarm ruins, under tree", False, lambda state: all([
            oos_season_in_tarm_ruins(state, player, "autumn"),
            oos_can_break_mushroom(state, player, False),
            oos_can_use_ember_seeds(state, player, False)
        ])],

        ["d6 sector", "d6 entrance", False, lambda state: all([
            oos_season_in_tarm_ruins(state, player, "winter"),
            any([
                oos_has_shovel(state, player),
                oos_can_use_ember_seeds(state, player, False)
            ]),
            oos_season_in_tarm_ruins(state, player, "spring"),
            oos_can_break_flowers(state, player, False)
        ])],
        ["d6 entrance", "old man near d6", False, lambda state: oos_can_use_ember_seeds(state, player, False)],

        # SAMASA DESERT ######################################################################################

        ["suburbs", "samasa desert", False, lambda state: state.has("_met_pirates", player)],
        ["samasa desert", "samasa desert pit", False, lambda state: oos_has_bracelet(state, player)],
        ["samasa desert", "samasa desert chest", False, lambda state: oos_has_flippers(state, player)],

        # TEMPLE REMAINS ####################################################################################

        ["temple remains lower stump", "temple remains upper stump", False, lambda state: any([
            all([  # Winter rule
                oos_season_in_temple_remains(state, player, "winter"),
                oos_can_remove_snow(state, player, False),
                oos_can_break_bush(state, player, False),
                oos_can_jump_6_wide_pit(state, player)
            ]),
            all([  # Summer rule
                oos_season_in_temple_remains(state, player, "summer"),
                oos_can_break_bush(state, player, False),
                oos_can_jump_6_wide_pit(state, player)
            ]),
            all([  # Spring rule
                oos_season_in_temple_remains(state, player, "spring"),
                oos_can_break_flowers(state, player, False),
                oos_can_break_bush(state, player, False),
                oos_can_jump_6_wide_pit(state, player)
            ]),
            all([  # Autumn rule
                oos_season_in_temple_remains(state, player, "autumn"),
                oos_can_break_bush(state, player)
            ])
        ])],
        ["temple remains upper stump", "temple remains lower stump", False, lambda state: any([
            # Winter rule
            oos_season_in_temple_remains(state, player, "winter"),
            all([  # Summer rule
                oos_season_in_temple_remains(state, player, "summer"),
                oos_can_break_bush(state, player, False),
                oos_can_jump_6_wide_pit(state, player)
            ]),
            all([  # Spring rule
                oos_season_in_temple_remains(state, player, "spring"),
                oos_can_break_flowers(state, player, False),
                oos_can_break_bush(state, player, False),
                oos_can_jump_6_wide_pit(state, player)
            ]),
            all([  # Autumn rule
                oos_season_in_temple_remains(state, player, "autumn"),
                oos_can_break_bush(state, player)
            ])
        ])],

        ["temple remains upper stump", "temple remains lower portal", False, lambda state: all([
            oos_season_in_temple_remains(state, player, "winter"),
            oos_can_jump_1_wide_pit(state, player, False)
        ])],

        ["temple remains lower portal", "temple remains upper stump", False, lambda state: any([
            # Portal can be escaped only if default season is winter or if volcano erupted
            all([
                oos_get_default_season(state, player, "TEMPLE_REMAINS") == "winter",
                oos_can_jump_1_wide_pit(state, player, False)
            ]),
            all([
                state.has("_triggered_volcano", player),
                oos_can_jump_2_wide_liquid(state, player)
            ]),
        ])],
        ["temple remains lower portal", "temple remains lower stump", False, lambda state: \
            # There is an added ledge in rando that enables jumping from the portal down to the stump, whatever
            # the season is, but it is a risky action so we ask for the player to be able to warp back
            oos_can_warp(state, player)],

        ["temple remains lower stump", "temple remains heart piece", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_can_jump_2_wide_liquid(state, player),
            oos_can_remove_rockslide(state, player, False),
        ])],

        ["temple remains lower stump", "temple remains upper portal", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_season_in_temple_remains(state, player, "summer"),
            oos_can_jump_2_wide_liquid(state, player),
            any([
                oos_has_magnet_gloves(state, player),
                oos_can_jump_6_wide_pit(state, player)
            ])
        ])],
        ["temple remains upper portal", "temple remains lower stump", False, lambda state: all([
            state.has("_triggered_volcano", player),
            oos_can_jump_1_wide_liquid(state, player, False)
        ])],

        ["temple remains upper portal", "temple remains upper stump", False, lambda state: \
            oos_can_jump_1_wide_pit(state, player, False)],

        ["temple remains upper portal", "temple remains lower portal", False, lambda state: \
            oos_get_default_season(state, player, "TEMPLE_REMAINS") == "winter"],


        # ONOX CASTLE #############################################################################################

        ["maku tree", "maku seed", False, lambda state: oos_has_essences_for_maku_seed(state, player)],
        ["maku tree", "maku tree, 3 essences", False, lambda state: oos_has_essences(state, player, 3)],
        ["maku tree", "maku tree, 5 essences", False, lambda state: oos_has_essences(state, player, 5)],
        ["maku tree", "maku tree, 7 essences", False, lambda state: oos_has_essences(state, player, 7)],

        ["north horon", "d9 entrance", False, lambda state: state.has("Maku Seed", player)],
        ["d9 entrance", "onox beaten", False, lambda state: all([
            oos_can_kill_armored_enemy(state, player),
            oos_has_bombs(state, player),
            oos_has_sword(state, player, False),
            oos_has_feather(state, player),
            any([
                oos_option_hard_logic(state, player),
                oos_has_rod(state, player)
            ])
        ])],

        ["onox beaten", "ganon beaten", False, lambda state: all([
            oos_has_sword(state, player, False),
            oos_has_slingshot(state, player),
            oos_can_use_ember_seeds(state, player, True),
        ])],

        # GOLDEN BEASTS #############################################################################################

        ["d0 entrance", "golden darknut", False, lambda state: all([
            oos_season_in_western_coast(state, player, "spring"),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player)
            ])
        ])],
        ["tarm ruins", "golden lynel", False, lambda state: all([
            oos_season_in_lost_woods(state, player, "summer"),
            oos_season_in_lost_woods(state, player, "winter"),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player)
            ])
        ])],
        ["d2 entrance", "golden moblin", False, lambda state: all([
            oos_season_in_central_woods_of_winter(state, player, "autumn"),
            any([
                oos_has_sword(state, player),
                oos_has_fools_ore(state, player),
                # Moblin has the interesting property of being one-shottable using an ember seed
                all([
                    oos_option_medium_logic(state, player),
                    oos_can_use_ember_seeds(state, player, False)
                ])
            ])
        ])],
        ["spool swamp south (summer)", "golden octorok", False, lambda state: any([
            oos_has_sword(state, player),
            oos_has_fools_ore(state, player)
        ])],
    ]
