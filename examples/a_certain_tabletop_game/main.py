from rrr import act
from rrr import ActorLoader
from rrr import Actions as BaseActions

from models import ModelStatMovement
from models import ModelStatWeaponSkill
from models import ModelStatBallisticSkill
from models import ModelStatStrength
from models import ModelStatToughness
from models import ModelStatWounds
from models import ModelStatAttacks
from models import ModelStatLeadership
from models import ModelStatSave
from weapons import WeaponRange
from weapons import WeaponType
from weapons import WeaponAttacks
from weapons import WeaponStrength
from weapons import WeaponArmorPenetration
from weapons import WeaponDamage
from weapons import WeaponAbilities
from equipment import EquipmentWeapons
from equipment import EquipmentItems
from equipment import EquipmentRelic
from actions import existing_actions

class Actions(BaseActions):
    _actions = existing_actions


if __name__ == '__main__':
    import yaml
    with open('roles.yaml', 'r') as f:
        roles_specs = yaml.safe_load(f)
    with open('actors.yaml', 'r') as f:
        actor_specs = yaml.safe_load(f)
    actor_loader = ActorLoader(
        actor_specs,
        roles_specs,
        role_classes=[
            ModelStatMovement,
            ModelStatWeaponSkill,
            ModelStatBallisticSkill,
            ModelStatStrength,
            ModelStatToughness,
            ModelStatWounds,
            ModelStatAttacks,
            ModelStatLeadership,
            ModelStatSave,
            WeaponRange,
            WeaponType,
            WeaponAttacks,
            WeaponStrength,
            WeaponArmorPenetration,
            WeaponDamage,
            WeaponAbilities,
            EquipmentWeapons,
            EquipmentItems,
            EquipmentRelic,
            Actions,
        ],
    )

    #laser_rifle = actor_loader.create('laser_rifle')
    #grenade = actor_loader.create('fragmentation_grenade')
    grunt_1 = actor_loader.create('grunt')
    grunt_2 = actor_loader.create('grunt')
    report = act(grunt_1, 'attack', target=grunt_2)
    import pdb; pdb.set_trace()
    pass
