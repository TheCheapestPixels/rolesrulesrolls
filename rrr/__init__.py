import yaml


def enact(actor, action, **kwargs):
    func = actor['_actions'][action]
    state = dict(initiator=actor, **kwargs)
    func(state)
    return state


class RoleLoader:
    def __init__(self, actions=None, attributes=None):
        if actions is None:
            actions = []
        if attributes is None:
            attributes = []
        self.actions = {f.__name__: f for f in actions}
        self.attributes = {c._name: c for c in attributes}

    def load(self, stream):
        self.role_specs = yaml.safe_load(stream)
        
    def create(self, role_name):
        actor = {}
        role_spec = self.role_specs[role_name]
        for field, value_spec in role_spec.items():
            if field == '_actions':
                value = {an: self.actions[fn]
                         for an, fn in value_spec.items()}
            elif field == '_roles':
                value = {rn: None for rn in value_spec}
            else:
                if value_spec == 'None':
                    value = None
                elif isinstance(value_spec, list):
                    value_cls = self.attributes[value_spec[0]]
                    value = value_cls(*value_spec[1:])
                else:
                    value = value_spec
            actor[field] = value
        return actor
