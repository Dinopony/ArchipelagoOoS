from rule_builder.rules import Rule as BaseRule
from worlds.tloz_oos import OracleOfSeasonsWorld

Rule = BaseRule[OracleOfSeasonsWorld]

LogicLine = tuple[str, str, bool, Rule] | tuple[str, str, bool, Rule, bool]
