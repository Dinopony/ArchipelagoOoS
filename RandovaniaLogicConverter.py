from BaseClasses import Location, Region, Entrance, Item, ItemClassification

TRIVIAL_CONNECTION = {
    "type": "and",
    "data": {
        "comment": None,
        "items": []
    }
}


class RandovaniaLogicData:
    def __init__(self, header, regions, base_location_id, base_item_id):
        self.header = header
        self.regions = regions
        self.base_location_id = base_location_id
        self.base_item_id = base_item_id


class RandovaniaLogicRule:
    def __init__(self, data, logic_converter):
        self.data = data
        self.multiworld = logic_converter.multiworld
        self.player = logic_converter.player
        self.item_names_matching_table = logic_converter.item_names_matching_table
        self.rule_templates = logic_converter.rule_templates
        self.events_table = logic_converter.events_table

    def test(self, state):
        return self._test_rule(self.data, state)

    def _test_rule(self, rule_data, state):
        if rule_data["type"] == "and":
            # AND: all sub-rules must be true
            return all([self._test_rule(condition, state) for condition in rule_data["data"]["items"]])
        elif rule_data["type"] == "or":
            # OR: one of the sub-rules must be true
            return any([self._test_rule(condition, state) for condition in rule_data["data"]["items"]])
        elif rule_data["type"] == "template":
            # TEMPLATE: test a previously defined 'template rule'
            return self.rule_templates[rule_data["data"]].test(state)
        elif rule_data["type"] == "resource":
            if rule_data["data"]["type"] == "items":
                # RESOURCE.ITEMS: player needs to have the specified item
                item_internal_name = rule_data["data"]["name"]
                item_display_name = self.item_names_matching_table[item_internal_name]
                value = state.has(item_display_name, self.player)
            elif rule_data["data"]["type"] == "tricks":
                # RESOURCE.TRICKS: player needs to have toggled on the specified trick option at generation-time
                value = self._test_trick(rule_data["data"]["name"], rule_data["data"]["amount"])
            elif rule_data["data"]["type"] == "events":
                # RESOURCE.EVENTS: player needs to have triggered specified event
                value = self._test_event(state, rule_data["data"]["name"])
            elif rule_data["data"]["type"] == "damage":
                # RESOURCE.DAMAGE: player must be able to absorb a specified amount of damage
                value = self._test_damage(rule_data["data"]["amount"])
            elif rule_data["data"]["type"] == "misc":
                # RESOURCE.MISC: test a specific parameter (most of the time, a seed generation option)
                value = self._test_misc(rule_data["data"]["name"])
            else:
                raise "Unhandled rule type"

            if "negate" in rule_data["data"] and rule_data["data"]["negate"] is True:
                return not value
            return value

        raise "Unhandled rule type"

    def _test_event(self, state, event_name):
        if event_name not in self.events_table:
            raise "Unknown Randovania event is being checked!"
        return any(state.can_reach(region, None, self.player) for region in self.events_table[event_name])

    def _test_trick(self, trick_name, expected_level):
        trick_levels = self.multiworld.trick_levels[self.player]
        level = trick_levels[trick_name] if trick_name in trick_levels else 0
        return level >= expected_level

    def _test_damage(self, amount):
        # TODO: Handle damage properly (+ handle damage strictness?)
        return True

    def _test_misc(self, variable_name):
        try:
            return getattr(self.multiworld, variable_name)[self.player] != 0
        except AttributeError:
            return False



class RandovaniaLogicConverter:
    def __init__(self, multiworld, player, logic_data: RandovaniaLogicData):
        self.planned_connections = {}
        self.multiworld = multiworld
        self.player = player
        self.item_names_matching_table = {}
        self.logic_data = logic_data
        self.current_location_id = logic_data.base_location_id
        self.current_item_id = logic_data.base_item_id
        self.rule_templates = {}
        self.events_table = {}

    def create_regions(self):
        for region_data in self.logic_data.regions:
            self._process_region(region_data)

    def create_items(self):
        item_names_to_id = {}
        for item_name, item_data in self.logic_data.header["resource_database"]["items"].items():
            self.item_names_matching_table[item_name] = item_data["long_name"]
        return item_names_to_id

    def _process_region(self, region_data):
        rdv_region_name = region_data["name"]
        for area_name, area_data in region_data["areas"].items():
            namespace = self.convert_name(rdv_region_name, area_name)
            for node_name, node_data in area_data["nodes"].items():
                self._process_node(namespace, node_name, node_data)

    def _process_node(self, namespace, node_name, node_data):
        real_name = self.convert_name(namespace, node_name)
        region = Region(real_name, self.player, self.multiworld)
        self.multiworld.regions.append(region)

        for destination_name, details in node_data["connections"].items():
            destination_real_name = self.convert_name(namespace, destination_name)
            self.planned_connections[(real_name, destination_real_name)] = details

        if node_data["node_type"] == "dock":
            # Node is a dock, it means the region will have a trivial connection to another one
            dest_region = node_data["default_connection"]["region"]
            dest_area = node_data["default_connection"]["area"]
            dest_node = node_data["default_connection"]["node"]
            dest_name = self.convert_name(dest_region, dest_area, dest_node)
            self.planned_connections[(real_name, dest_name)] = TRIVIAL_CONNECTION
        elif node_data["node_type"] == "pickup" and not real_name.endswith("(Items Every Room)"):
            # Node is a pickup, create a matching location and add it
            location = Location(self.player, real_name, self.current_location_id, region)
            self.current_location_id += 1
            region.locations.append(location)
        elif node_data["node_type"] == "event":
            # Node is an event, link this region to this event name
            if not node_data["event_name"] in self.events_table:
                self.events_table[node_data["event_name"]] = []
            self.events_table[node_data["event_name"]].append(region)

    def set_rules(self):
        self._load_rule_templates()
        self._process_planned_connections()

        # Setup win condition
        win_rule = RandovaniaLogicRule(self.logic_data.header["victory_condition"], self)
        self.multiworld.completion_condition[self.player] = lambda state: win_rule.test(state)

    def _load_rule_templates(self):
        for template_name, template_rule in self.logic_data.header["resource_database"]["requirement_template"].items():
            self.rule_templates[template_name] = RandovaniaLogicRule(template_rule, self)

    def _process_planned_connections(self):
        for region_pair, details in self.planned_connections.items():
            from_region = self.multiworld.get_region(region_pair[0], self.player)
            to_region = self.multiworld.get_region(region_pair[1], self.player)

            entrance = Entrance(self.player, f"{region_pair[0]} -> {region_pair[1]}", from_region)
            from_region.exits.append(entrance)
            entrance.connect(to_region)

            if not self.is_trivial_connection(details):
                entrance.access_rule = self.build_logic_rule(details)

    def build_logic_rule(self, data):
        """
        Lambdas are created in a for loop, so values need to be captured
        """
        rule = RandovaniaLogicRule(data, self)
        return lambda state: rule.test(state)

    @staticmethod
    def is_trivial_connection(connection_details):
        return connection_details["type"] == "and" and len(connection_details["data"]["items"]) == 0

    @staticmethod
    def convert_name(*args) -> str:
        return "/".join(args)

    @staticmethod
    def build_item_name_to_id_table(header_data, base_item_id):
        item_names_to_id = {}
        current_item_id = base_item_id
        for item_name, item_data in header_data["resource_database"]["items"].items():
            item_names_to_id[item_data["long_name"]] = current_item_id
            current_item_id += 1

        # Add hardcoded ammo
        item_names_to_id["Missile Expansion"] = current_item_id
        current_item_id += 1
        item_names_to_id["Power Bomb Expansion"] = current_item_id
        current_item_id += 1
        item_names_to_id["Nothing"] = current_item_id

        return item_names_to_id

    @staticmethod
    def build_location_name_to_id_table(regions_data, base_location_id):
        location_name_to_id_table = {}
        current_location_id = base_location_id

        for region_data in regions_data:
            region_name = region_data["name"]
            for area_name, area_data in region_data["areas"].items():
                for node_name, node_data in area_data["nodes"].items():
                    if node_data["node_type"] == "pickup" and not node_name.endswith("(Items Every Room)"):
                        location_name = RandovaniaLogicConverter.convert_name(region_name, area_name, node_name)
                        location_name_to_id_table[location_name] = current_location_id
                        current_location_id += 1

        return location_name_to_id_table
