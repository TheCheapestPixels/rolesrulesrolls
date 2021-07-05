A Certain Tapletop Game
=======================

### `action_attack`

`act(grunt_1, 'attack', grunt_2)` results in `action_attack` with a
state of
```
initiator: <grunt_1>
target: <grunt_2>
```
being called. It adds
```
attack_sequence: {}
```
and calls `rule_ranged_attack`.


### `rule_ranged_attack`

```
attack_sequence.distance = 10
attack_sequence.line_of_sight = True
attack_sequence.attack_skill = initiator.stats.ballistic_skill
attack_sequence.attack_profile = initiator.equipment.weapons.select(weapon).profile
attack_sequence.attacks = attack_sequence.attack_profile.attacks.contextual_attacks()
attack_sequence.hit_roll = !roll(hit_roll)
? attack_sequence.hit_roll.hits >= 0
T attack_sequence.hit_roll = !roll(wound_roll)
  ? attack_sequence.wound_roll.wounds >= 0
  T !act(target, receive_wounds, attacker=initiator)
```

### hit roll

```
attack_sequence.hit_roll.dice.<n>.natural = ...
attack_sequence.hit_roll.dice.<n>.failed  = ...
attack_sequence.hit_roll.hits = ...
attack_sequence.hit_roll.misses = ...
```


### wound roll