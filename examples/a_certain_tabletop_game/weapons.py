from rrr import Attribute


class WeaponRange(Attribute):
    _name = 'WeaponRange'

    def load(self, loader, value):
        assert isinstance(value, int)
        return value

    def half_distance(self):
        return self.value / 2.0


class WeaponType(Attribute):
    _name = 'WeaponType'

    def load(self, loader, value):
        weapon_types = [
            'assault',
            'rapid_fire',
            'heavy',
            'pistol',
            'grenade',
        ]
        assert value in weapon_types
        return value

    def get(self):
        return self.value


class WeaponAttacks(Attribute):
    _name = 'WeaponAttacks'

    def load(self, loader, value):
        # TODO: int, d<n>
        assert isinstance(value, (str, int))
        return value

    def contextual_attacks(self, state):
        attacks = self.value

        # Rapid fire at half distance
        weapon_type = state['attack_sequence']['attack_profile']['type'].get()
        if weapon_type == 'rapid_fire':
            distance = state['attack_sequence']['distance']
            half_distance = state['attack_sequence']['attack_profile']['range'].half_distance()
            if distance <= half_distance:
                attacks *= 2

        return attacks


class WeaponStrength(Attribute):
    _name = 'WeaponStrength'

    def load(self, loader, value):
        assert isinstance(value, int) or value in ['user', 'x2']
        return value


class WeaponArmorPenetration(Attribute):
    _name = 'WeaponArmorPenetration'

    def load(self, loader, value):
        assert isinstance(value, int)
        return value


class WeaponDamage(Attribute):
    _name = 'WeaponDamage'

    def load(self, loader, value):
        assert isinstance(value, int) or value in ['d3', 'd6']
        return value


class WeaponAbilities(Attribute):
    _name = 'WeaponAbilities'

    def load(self, loader, value=None):
        existing_abilities = ['blast']
        if value is None:
            value = []
        else:
            assert all(v in existing_abilities for v in value)
        return value

    def __repr__(self):
        if self.value:
            return ', '.join(self.abilities)
        else:
            return '-'
