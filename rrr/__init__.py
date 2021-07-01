# class Actor:
#     def __init__(self, name, roles):
#         self.name = name
#         self.roles = roles
# 
#     def __repr__(self):
#         if self.roles:
#             roles = ', '.join(self.roles.keys())
#             return f'Actor({self.name}: {roles})'
#         else:
#             return f'Actor({self.name})'


class Attribute:
    _name = None
    def __init__(self, loader, *args, **kwargs):
        self.value = self.load(loader, *args, **kwargs)

    def __repr__(self):
        return f'{self._name}({self.value})'

    def load(self, loader, *args, **kwargs):
        print(f"WARNING: No loader implemented on {self._name}! "
              "Defaulting to args[0]")
        if not args and not kwargs:
            return None
        else:
            return args[0]


class Actions:
    _name = 'Actions'
    _actions = {}
    def __init__(self, actor_loader, actions):
        assert all(a in self._actions for a in actions)
        self.actions = {an: self._actions[an] for an in actions}

    def act(self, action, state):
        return self.actions[action](state)

    def __repr__(self):
        if not self.actions:
            return '-'
        else:
            return ', '.join(a for a in self.actions.keys())


def act(_actor, _action, **kwargs):
    state = dict(initiator=_actor, **kwargs)
    actor_role = _actor['actor']['actions']
    actor_role.act(_action, state)
    return state


class ActorLoader:
    def __init__(self, actor_specs, role_specs, role_classes):
        role_classes = {rc._name: rc for rc in role_classes}

        # Roles: Turn strings into classes
        self.roles = {}
        for role_name, field_specs in role_specs.items():
            role = {}
            for field_name, field_class in field_specs.items():
                role[field_name] = role_classes[field_class]
            self.roles[role_name] = role

        # 
        self.actors = {}
        for actor_name, roles in actor_specs.items():
            actor = {}
            # rnac = role name and class
            for rnac, fields in roles.items():
                assert rnac.count('<') == 1
                role_name, _, role_class = rnac.partition('<')
                actor[role_name] = dict(
                    cls=role_class,
                    fields=fields,
                )
            self.actors[actor_name] = actor

    def create(self, actor_type):
        actor = {}
        actor_spec = self.actors[actor_type]
        for role_name, role_spec in actor_spec.items():
            role = {}
            role_class_name = role_spec['cls']
            field_classes = self.roles[role_class_name]
            fields = role_spec['fields']
            for field_name, field_class in field_classes.items():
                if field_name in fields:
                    field_value = field_class(self, fields[field_name])
                else:
                    field_value = field_class(self)
                role[field_name] = field_value
            actor[role_name] = role
        return actor
