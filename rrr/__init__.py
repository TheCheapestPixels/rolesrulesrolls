class Action:
    def __init__(self):
        pass


class Actor:
    def __init__(self, stats):
        self.stats = stats

    def set_stat(self, stat, value):
        self.stats[stat] = value

    def act(self, action, **kwargs):
        func = self.stats['_actions'][action]
        state = dict(initiator=self, **kwargs)
        func(state)
        return state


def enact(actor, action, **kwargs):
    func = actor['_actions'][action]
    state = dict(initiator=actor, **kwargs)
    func(state)
    return state
