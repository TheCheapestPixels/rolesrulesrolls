from rrr import Attribute


existing_weapons = [
    'laser_rifle',
    'fragmentation_grenade',
]


class EquipmentWeapons(Attribute):
    _name = 'EquipmentWeapons'

    def load(self, loader, value=None):
        if value is None:
            return None
        if isinstance(value, str):
            value = [value]
        assert all(v in existing_weapons for v in value)
        return {v: loader.create(v) for v in value}

    def __repr__(self):
        if not self.value:
            return '-'
        else:
            return ', '.join(repr(v) for v in self.value)

    def select(self, name):
        return self.value[name]


class EquipmentItems(Attribute):
    _name = 'EquipmentItems'


class EquipmentRelic(Attribute):
    _name = 'EquipmentRelic'
