# import toml
# 
# 
# with open("rules/rolls.toml", 'r') as f:
#     ROLLS = toml.loads(f.read())

from rrr import Actor


class Stat():
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
    state['tool'] = state['initiator'].stats['inventory_main_hand']
    #from pprint import pprint
    #pprint(tool.stats)
    #pprint(target.stats)

    # FIXME: We should find the common functionality, but for now we
    # will assume shanking.
    action = 'attack'
    action_func = state['tool'].stats['_actions'][action]
    action_func(state)


def shank(state):
    state['follow_up_hit'] = state['target'].act(
        'get_hit',
        damage=state['tool'].stats['damage'],
    )
    state['follow_up_exp'] = state['initiator'].act(
        'gain_experience',
        skill='skill_melee_attack',
        increase=1,
    )


def handle_damage(state):
    state['initiator'].stats['attribute_health'].adjust(
        -state['damage'],
    )


def increase_skill(state):
    state['initiator'].stats[state['skill']].adjust(state['increase'])


if __name__ == '__main__':
    def char_stats():
        return dict(
            _roles=dict(
                attacker=None,
                attackee=None,
            ),
            _actions=dict(
                default_act=use_main_hand,
                get_hit=handle_damage,
                gain_experience=increase_skill,
            ),
            attribute_health=Stat(10),
            skill_melee_attack=Stat(0),
            inventory_main_hand=None,
            inventory_torso=None,
        )
    char_a = Actor(char_stats())
    char_b = Actor(char_stats())

    def screwdriver_stats():
        return dict(
            _actions=dict(
                unscrew=None,
                attack=shank,
            ),
            _roles=dict(
                into_main_hand_takeable=None,  # FIXME: Only an example.
            ),
            damage=2,
        )
    screwdriver = Actor(screwdriver_stats())
    char_a.set_stat('inventory_main_hand', screwdriver)

    def electric_socket():
        return dict(
            _roles=dict(
                screwable=None,
            ),
            status_is_closed=True,
        )
    socket = Actor(electric_socket())
    
    def attack():
        from pprint import pprint
        report = char_a.act('default_act', target=char_b)
        print(f"Target health {char_b.stats['attribute_health']}, "
              f"Attacker skill {char_a.stats['skill_melee_attack']}")
        pprint(report)

    for _ in range(3):
        attack()
    # char_a.act('default_act', target=socket)
