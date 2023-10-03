from __future__ import annotations

from typing import Dict

from Options import Option, Range, ItemDict, DefaultOnToggle, Choice, Toggle, OptionDict


class ArtifactCount(Range):
    """
    Determines the number of artifacts required to trigger the fight against Meta Ridley
    """
    display_name = "Artfiact count"
    range_start = 0
    range_end = 12
    default = 6


class AmmoMissileLauncher(Range):
    """
    The increase in maximum quantity of missiles when obtaining the Missile Launcher
    """
    display_name = "Missile Launcher ammo"
    range_start = 1
    range_end = 250
    default = 5


class AmmoMissileExpansion(Range):
    """
    The increase in maximum quantity of missiles when obtaining a Missile Expansion
    """
    display_name = "Missile Expansion ammo"
    range_start = 0
    range_end = 250
    default = 5


class AmmoMainPowerBomb(Range):
    """
    The increase in maximum quantity of power bombs when obtaining the Main Power Bomb
    """
    display_name = "Main Power Bomb ammo"
    range_start = 1
    range_end = 8
    default = 4


class AmmoPowerBombExpansion(Range):
    """
    The increase in maximum quantity of power bombs when obtaining a Power Bomb Expansion
    """
    display_name = "Power Bomb Expansion ammo"
    range_start = 1
    range_end = 8
    default = 1


class EnergyPerTank(Range):
    """
    The increase in maximum energy when obtaning an Energy Tank
    """
    display_name = "Energy per tank"
    range_start = 0
    range_end = 900
    default = 100


class WarpToStart(DefaultOnToggle):
    """
    If enabled, save stations can teleport you back to your starting room by pressing L+R and selecting "No" when
    asked if you want to save your game.
    """
    display_name = "Allow warping back to start"


class CutsceneMode(Choice):
    """
    The way cutscenes are handled in the randomizer:
    - Original: no changes to the cutscenes are made
    - Minor: removes cutscenes that don't affect the game too much when removed
    - Major: removes most cutscenes
    - Competitive: same as minor with a few cutscenes let intact to be more adapted to races
    """
    display_name = "Cutscene removal mode"

    option_original = 0
    option_minor = 1
    option_major = 2
    option_competitive = 3
    default = 1


class MainPlazaDoor(DefaultOnToggle):
    """
    In the vanilla game, there is a door between Main Plaza and Vault rooms which can only be taken in one direction,
    which decreases the variety of possible routing options in the early game.
    If enabled, this option unlocks the door to be open from both ways.
    """
    display_name = "Unlock door from Main Plaza to Vault"


class BlueSaveDoors(DefaultOnToggle):
    """
    If enabled, make all save station doors blue to ensure it is always possible to heal and save the game.
    This has almost no logical impact but decreases the odds of dying, especially for beginner players.
    """
    display_name = "Make save stations always accessible"


class BackwardsFrigate(DefaultOnToggle):
    """
    In the vanilla game, it is not possible to cross the sunken frigate without using out-of-bound tricks because
    of a door which needs to be powered using Wave Beam from the other side.
    If enabled, this makes the door openable from behind without being powered, adding interesting routing options.
    """
    display_name = "Allow backwards Tallon frigate"


class BackwardsLabs(DefaultOnToggle):
    """
    In the vanilla game, there is a forcefield in Phendrana labs which require scanning a switch to open.
    When crossing labs backwards, the switch is visible but cannot be scanned through the forcefield, blocking the path.
    If enabled, this makes the switch scannable through the barrier, opening a backwards route for labs.
    """
    display_name = "Allow backwards Phendrana labs"


class BackwardsUpperMines(DefaultOnToggle):
    """
    In the vanilla game, there is a barrier in Main Quarry which can only be disabled from one side. When using tricks,
    it's possible to come from the other side and be blocked unless the barrier was previously opened.
    If enabled, this option automatically remove the barrier when approched from behind.
    """
    display_name = "Allow backwards upper Phazon Mines"


class BackwardsLowerMines(Toggle):
    """
    In the vanilla game, there are huge bars blocking the path behind Omega Pirate forcing you to take a specific path
    to reach the lower mines.
    If enabled, this removes the barrier and opens the whole lower mines sector with less logic constraints.
    """
    display_name = "Allow backwards lower Phazon Mines"


class PhazonEliteWithoutDynamo(DefaultOnToggle):
    """
    In the vanilla game, the Phazon Elite miniboss in Elite Research cannot be triggered unless you collected the
    item in Central Dynamo.
    If enabled, this removes this artificial requirement making the boss fightable as soon as you have Power Bombs.
    """
    display_name = "Phazon Elite without Central Dynamo item"


class ItemDistribution(ItemDict):
    """
    Determines the items that will be shuffled in the world (artifacts excluded).
    If smaller than the location pool size (100), Nothing items are used to fill the remaining locations.
    """
    display_name = "Items distribution"
    default = {
        "Wave Beam": 1,
        "Ice Beam": 1,
        "Plasma Beam": 1,
        "Missile Launcher": 1,
        "Grapple Beam": 1,
        "Thermal Visor": 1,
        "X-Ray Visor": 1,
        "Space Jump Boots": 1,
        "Energy Tank": 14,
        "Morph Ball": 1,
        "Morph Ball Bomb": 1,
        "Boost Ball": 1,
        "Spider Ball": 1,
        "Power Bomb": 1,
        "Varia Suit": 1,
        "Gravity Suit": 1,
        "Phazon Suit": 1,
        "Super Missile": 1,
        "Wavebuster": 1,
        "Ice Spreader": 1,
        "Flamethrower": 1,
        "Missile Expansion": 49,
        "Power Bomb Expansion": 4
    }


class TrickLevels(OptionDict):
    """
    Determines the difficulty of tricks that you will be taken in account inside the logic.
    """
    display_name = "Trick levels"
    default = {
        "BJ": 0,
        "BSJ": 0,
        "BoostlessSpiner": 0,
        "CBJ": 0,
        "ClipThruObjects": 0,
        "Combat": 0,
        "DBoosting": 0,
        "Dash": 0,
        "HeatRun": 0,
        "IS": 0,
        "IUJ": 0,
        "InvisibleObjects": 0,
        "Knowledge": 0,
        "LJump": 0,
        "Movement": 0,
        "OoB": 0,
        "RJump": 0,
        "SJump": 0,
        "StandEnemies": 0,
        "Standable": 0,
        "UnderwaterMovement": 0,
        "WallBoost": 0
    }


metroid_prime_option_definitions: Dict[str, type(Option)] = {
    "artifact_target": ArtifactCount,
    "ammo_missile_launcher": AmmoMissileLauncher,
    "ammo_missile_expansion": AmmoMissileExpansion,
    "ammo_main_power_bomb": AmmoMainPowerBomb,
    "ammo_power_bomb_expansion": AmmoPowerBombExpansion,
    "energy_per_tank": EnergyPerTank,
    "warp_to_start": WarpToStart,
    "cutscene_mode": CutsceneMode,

    "main_plaza_door": MainPlazaDoor,
    "blue_save_doors": BlueSaveDoors,
    "backwards_frigate": BackwardsFrigate,
    "backwards_labs": BackwardsLabs,
    "backwards_upper_mines": BackwardsUpperMines,
    "backwards_lower_mines": BackwardsLowerMines,
    "phazon_elite_without_dynamo": PhazonEliteWithoutDynamo,

    "item_distribution": ItemDistribution,
    "trick_levels": TrickLevels
}
