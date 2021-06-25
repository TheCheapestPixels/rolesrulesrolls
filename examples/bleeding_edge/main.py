# import toml
# 
# 
# with open("rules/rolls.toml", 'r') as f:
#     ROLLS = toml.loads(f.read())

from rrr import enact
from rrr import RoleLoader


class Stat():
    _name = 'Stat'
    def __init__(self, level):
        self.level = level
        self.maximum = 10
        self.overflow = False # Maximum is hard limit

    def adjust(self, delta):
        self.level = max(min(self.level + delta, self.maximum), 0)

    def __repr__(self):
        return f'{self.level} / {self.maximum}'


# Some examples for actions

def use_main_hand(state):
    state['tool'] = state['initiator']['inventory_main_hand']
    #from pprint import pprint
    #pprint(tool.stats)
    #pprint(target.stats)

    # FIXME: We should find the common functionality, but for now we
    # will assume shanking.
    action = 'attack'
    action_func = state['tool']['_actions'][action]
    action_func(state)


def shank(state):
    state['follow_up_hit'] = enact(
        state['target'],
        'get_hit',
        damage=state['tool']['damage'],
    )
    state['follow_up_exp'] = enact(
        state['initiator'],
        'gain_experience',
        skill='skill_melee_attack',
        increase=1,
    )


def handle_damage(state):
    state['initiator']['attribute_health'].adjust(
        -state['damage'],
    )


def increase_skill(state):
    state['initiator'][state['skill']].adjust(state['increase'])


if __name__ == '__main__':
    roles = RoleLoader(
        actions=[
            use_main_hand,
            handle_damage,
            increase_skill,
            shank,
        ],
        attributes=[
            Stat,
        ],
    )
    with open('roles.yaml', 'r') as f:
        roles.load(f)

    char_a = roles.create('character')
    char_b = roles.create('character')
    char_a['inventory_main_hand'] = roles.create('screwdriver')
    socket = roles.create('electric_socket')
    
    def attack():
        from pprint import pprint
        report = enact(
            char_a,
            'default_act',
            target=char_b,
        )
        print(f"Target health {char_b['attribute_health']}, "
              f"Attacker skill {char_a['skill_melee_attack']}")

    for _ in range(15):
        attack()
    # char_a.act('default_act', target=socket)
