def rule_ranged_attack(loader, state):
    state['attack_sequence']['weapon'] = state['weapon']  # FIXME: Request from user instead.
    state['attack_sequence']['profile'] = state['profile']  # FIXME: Request from user instead.
    state['attack_sequence']['distance'] = state['distance']  # FIXME: Request from env instead.
    state['attack_sequence']['line_of_sight'] = state['line_of_sight']  # FIXME: Request from env instead.
    
    state['attack_sequence']['attack_skill'] = state['initiator']['stats']['ballistic_skill']
    state['attack_sequence']['attack_profile'] = state['initiator']['equipment']['weapons'].select(state['weapon'])[state['profile']]
    state['attack_sequence']['attacks'] = state['attack_sequence']['attack_profile']['attacks'].contextual_attacks(state)
    state['attack_sequence']['hit_roll'] = loader.roll(
        num_dice=state['attack_sequence']['attacks'],  # FIXME: Multiply with `hit dice per attack`
        dice_rules=dict(
            dice_type=6,
            threshold=state['attack_sequence']['attack_skill'],
            one_always_fails=None,
        ),
        throw_rules=dict(
            count_successes=None,
        ),
    )
    # TODO: Accumulate hits
    #import pdb; pdb.set_trace()
    if state['attack_sequence']['hit_roll']['successes'] >= 1:
        #state['attack_sequence']['wound_threshold'] = 
        state['attack_sequence']['wound_roll'] = loader.roll(
            num_dice=state['attack_sequence']['attacks'],
            dice_rules=dict(
                dice_type=6,
                threshold=4,
                one_always_fails=None,
            ),
        )


def action_attack(loader, state):
    state['attack_sequence'] = {}
    rule_ranged_attack(loader, state)


def action_get_hit(loader, state):
    pass


existing_actions = dict(
    attack=action_attack,
    get_hit=action_get_hit,
)
