# freighterAgilityBonus2O2
#
# Used by:
# Ship: Bowhead
type = "passive"
def handler(fit, ship, context):
    level = fit.character.getSkill("ORE Freighter").level
    fit.ship.boostItemAttr("shipMaintenanceBayCapacity", ship.getModifiedItemAttr("freighterBonusO1")*level)
