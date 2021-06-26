import yaml


def enact(actor, action, **kwargs):
    func = actor['actor'][action]
    state = dict(initiator=actor, **kwargs)
    func(state)
    return state


# TODO: Make actual exception instead of `raise Exception`
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
        for role_name, role_spec in role_spec.items():
            role = {}
            for field_name, field_spec in role_spec.items():
                if field_spec == 'None':
                    field = None
                elif isinstance(field_spec, (bool, int)):
                    field = field_spec
                elif isinstance(field_spec, str):
                    try:
                        field = self.actions[field_spec]
                    except KeyError:
                        raise Exception(
                            f"Unknown function {role_name}."
                            f"{field_name}: {field_spec}"
                        )
                elif isinstance(field_spec, list):
                    field_cls = self.attributes[field_spec[0]]
                    field = field_cls(*field_spec[1:])
                else:
                    raise Exception(
                        f"Unparseable field {role_name}.{field_name}: "
                        f"{field_spec}"
                    )
                role[field_name] = field
            actor[role_name] = role
        return actor
