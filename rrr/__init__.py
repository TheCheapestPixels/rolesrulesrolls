import yaml


def enact(actor, action, **kwargs):
    func = actor['_actions'][action]
    state = dict(initiator=actor, **kwargs)
    func(state)
    return state
