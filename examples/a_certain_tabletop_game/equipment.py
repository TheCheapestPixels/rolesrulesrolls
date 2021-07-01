existing_weapons = [
    'laser_rifle',
    'fragmentation_grenade',
]


class EquipmentWeapons:
    _name = 'EquipmentWeapons'

    def __init__(self, actor_loader, weapons):
        if isinstance(weapons, str):
            weapons = [weapons]
        assert all(w in existing_weapons for w in weapons)
        self.weapons = {w: actor_loader.create(w) for w in weapons}

    def select(self, name):
        return self.weapons[name]

    def __repr__(self):
        if not self.weapons:
            return '-'
        else:
            return ', '.join(repr(w) for w in self.weapons)


class EquipmentItems:
    _name = 'EquipmentItems'
    def __init__(self, actor_loader, value=None):
        print(f"Partially implemented role {self._name} used")
        if value is None:
            value = []
        self.value = value

    def __repr__(self):
        return f'{self.value}'


class EquipmentRelic:
    _name = 'EquipmentRelic'
    def __init__(self, actor_loader, relic=None):
        print(f"Partially implemented role {self._name} used")
        self.relic = relic

    def __repr__(self):
        if self.relic is None:
            return '-'
        else:
            return f'{self.relic}'
