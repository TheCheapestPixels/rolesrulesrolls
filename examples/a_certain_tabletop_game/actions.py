def rule_ranged_attack(state):
    skill = state['initiator']['stats']['ballistic_skill']
    state['attack_sequence']['attack_skill'] = skill

    weapons = state['initiator']['equipment']['weapons']
    state['attack_sequence']['attack_profile'] = weapons.select('laser_rifle')['only']

    # TODO: How far are the units apart?
    state['attack_sequence']['distance'] = 10
    # TODO: Does line of sight exist?
    state['attack_sequence']['line_of_sight'] = True

    # state['contextual_attacks']
    attack_stat = state['attack_sequence']['attack_profile']['attacks']
    attacks = attack_stat.contextual_attacks(state)
    state['attack_sequence']['attacks'] = attacks


    import pdb; pdb.set_trace()
    pass


def action_attack(state):
    state['attack_sequence'] = {}
    rule_ranged_attack(state)


def action_get_hit(state):
    pass


existing_actions = dict(
    attack=action_attack,
    get_hit=action_get_hit,
)
