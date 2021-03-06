# shipBonusHMLExploDamageAC
#
# Used by:
# Ship: Sacrilege
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("Amarr Cruiser").level
    fit.modules.filteredChargeBoost(lambda mod: mod.charge.requiresSkill("Heavy Missiles"),
                                    "explosiveDamage", ship.getModifiedItemAttr("shipBonusAC") * level)
