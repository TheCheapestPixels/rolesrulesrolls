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

    def increase(self, delta):
        self.adjust(delta)

    def decrease(self, delta):
        self.adjust(-delta)

    def __repr__(self):
        return f'{self.level} / {self.maximum}'


# Some examples for actions

def use_main_hand(state):
    state['tool'] = state['initiator']['inventory_main_hand']
    # TODO:
    # * We know 'initiator', 'tool', and 'target', now we need to
    #   * choose the appropriate action (here ['weapon']['attack'] or
    #     ['tool']['screw'])
    #   * request a decision from the game in case of ambiguity
    action_func = state['tool']['weapon']['attack']
    action_func(state)


def shank(state):
    state['follow_up_hit'] = enact(
        state['target'],
        'get_hit',
        damage=state['tool']['weapon']['damage'],
    )
    state['follow_up_exp'] = enact(
        state['initiator'],
        'gain_experience',
        role='attacker',
        skill='skill_melee_attack',
        increase=1,
    )


def handle_damage(state):
    health = state['initiator']['attackee']['attribute_health']
    health.decrease(state['damage'])


def increase_skill(state):
    skill = state['initiator'][state['role']][state['skill']]
    skill.increase(state['increase'])


def screw(state):
    pass
    

def flip_status(state):
    pass
    

if __name__ == '__main__':
    roles = RoleLoader(
        actions=[
            use_main_hand,
            handle_damage,
            increase_skill,
            shank,
            screw,
            flip_status,
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
        print(f"Target health {char_b['attackee']['attribute_health']}, "
              f"Attacker skill {char_a['attacker']['skill_melee_attack']}")

    for _ in range(15):
        attack()
    # char_a.act('default_act', target=socket)
