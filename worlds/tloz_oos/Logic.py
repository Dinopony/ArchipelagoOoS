from BaseClasses import MultiWorld
from worlds.tloz_oos.data.logic.DungeonsLogic import (make_d0_logic, make_d1_logic, make_d2_logic, make_d3_logic,
                                                      make_d4_logic, make_d5_logic, make_d6_logic, make_d7_logic,
                                                      make_d8_logic)
from worlds.tloz_oos.data.logic.OverworldLogic import make_holodrum_logic
from worlds.tloz_oos.data.logic.SubrosiaLogic import make_subrosia_logic


def create_connections(multiworld: MultiWorld, player: int):
    dungeon_entrances = []
    for reg1, reg2 in multiworld.worlds[player].dungeon_entrances.items():
        dungeon_entrances.append([reg1, reg2, True, None])

    portal_connections = []
    for reg1, reg2 in multiworld.worlds[player].portal_connections.items():
        portal_connections.append([reg1, reg2, True, None])

    all_logic = [
        make_holodrum_logic(player),
        make_subrosia_logic(player),
        make_d0_logic(player),
        make_d1_logic(player),
        make_d2_logic(player),
        make_d3_logic(player),
        make_d4_logic(player),
        make_d5_logic(player),
        make_d6_logic(player),
        make_d7_logic(player),
        make_d8_logic(player),
        dungeon_entrances,
        portal_connections,
    ]

    def add_entrance(rules, start, end, rule):
        old_rule = rules[(start,end)]
        if rule is None:
            rule = lambda _: True
        rules[(start, end)] = lambda state: (old_rule(state) or rule(state))

    logic_rules = defaultdict(lambda: lambda _: False)

    # Create connections
    for logic_array in all_logic:
        for start, end, is_two_way, rule in logic_array:
            add_entrance(logic_rules, start, end, rule)
            if is_two_way:
                add_entrance(logic_rules, end, start, rule)

    for (start, end), rule in logic_rules.items():
        region_1 = multiworld.get_region(start, player)
        region_2 = multiworld.get_region(end, player)

        region_1.connect(region_2, None, rule)
