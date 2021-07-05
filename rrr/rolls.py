import random


### Dice rules, which affect each dice as it is rolled.

def roll_dice(d, faces):
    d['face'] = random.randint(1, faces)


def threshold(d, target_number):
    if d['face'] >= target_number:
        d['success'] = True
    else:
        d['success'] = False


def one_always_fails(d):
    if d['face'] == 1:
        d['success'] = False


def may_reroll_ones(dice):
    if dice['face'] == 1:
        dice['may_reroll'] = True


def may_reroll_failed(d):
    if not d.get('success', False):
        d['may_reroll'] = True


all_dice_rules = {
    f.__name__: f for f in [
        roll_dice,
        threshold,
        one_always_fails,
        may_reroll_ones,
        may_reroll_failed,
    ]
}


### Throw rules, which affect a set of already trown dice.

def count_successes(t):
    dice_dicts = [t[idx] for idx in range(t['num_dice'])]
    successes = [d for d in dice_dicts if d.get('success', False)]
    t['successes'] = len(successes)


all_throw_rules = {
    f.__name__: f for f in [
        count_successes,
    ]
}


### The actual functions.
def throw(num_dice=1, dice_rules=None, throw_rules=None):
    if throw_rules is None:
        throw_rules = {}
    if dice_rules is None:
        dice_rules = {}
    throw = {'num_dice': num_dice}
    for idx in range(num_dice):
        throw[idx] = roll(dice_rules)
    for rule_name, rule_arg in throw_rules.items():
        if rule_arg is None:
            all_throw_rules[rule_name](throw)
        else:
            all_throw_rules[rule_name](throw, rule_arg)
    return throw


def roll(rules):
    dice = {}
    for rule_name, rule_arg in rules.items():
        if rule_arg is None:
            all_dice_rules[rule_name](dice)
        else:
            all_dice_rules[rule_name](dice, rule_arg)
    return dice

t = throw(
    num_dice=20,
    dice_rules=dict(
        roll_dice=6,
        threshold=4,
        one_always_fails=None,
        may_reroll_failed=None,
    ),
)
import pprint
pprint.pprint (t)
