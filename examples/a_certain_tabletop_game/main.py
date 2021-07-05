import crayons

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


class TextInterface:
    def __init__(self, loader):
        self.loader = loader
        self.grunt_1 = loader.create('grunt')
        self.grunt_2 = loader.create('grunt')

    def run(self):
        print("grount 1 attacks grunt 2")
        callbacks = {'choose_dice': self.choose_dice}
        report = act(
            self.grunt_1,
            'attack',
            target=self.grunt_2,
            # TODO: Let the user / environment choose these.
            weapon='laser_rifle',  # User choice
            profile='only',  # User choice
            distance=10,  # Environmental
            line_of_sight=True,  # Environmental
            callbacks=callbacks,
        )
        self.print_attack_report(report['attack_sequence'])

    def print_attack_report(self, attack_sequence):
        hit_roll = attack_sequence['hit_roll']
        num_dice = hit_roll['num_dice']
        dice = {idx: hit_roll[idx] for idx in range(num_dice)}

        dice_indices = range(num_dice)
        dice_id_strings = []
        dice_value_strings = []
        for d_idx in dice_indices:
            d = dice[d_idx]
            dice_id_strings.append(
                '{}'.format(crayons.white('{:2d}'.format(d_idx))),
            )
            if not d.get('success', False):
                dice_value_strings.append(
                    '{}'.format(crayons.red('{:2d}'.format(d['face']))),
                )
            else:
                dice_value_strings.append(
                    '{}'.format(crayons.green('{:2d}'.format(d['face']))),
                )
        print("#dice: {}".format(' '.join(dice_id_strings)))
        print("roll : {}".format(' '.join(dice_value_strings)))
        import pdb; pdb.set_trace()
        pass

    def choose_dice(self, state):
        import pdb; pdb.set_trace()
        pass


if __name__ == '__main__':
    import yaml
    with open('roles.yaml', 'r') as f:
        roles_specs = yaml.safe_load(f)
    with open('actors.yaml', 'r') as f:
        actor_specs = yaml.safe_load(f)
    loader = ActorLoader(
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
    interface = TextInterface(loader)
    interface.run()
