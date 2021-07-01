rolesrulesrolls
===============

An attempt to implement a generic engine for game rules, and allow users
to edit these rules in YAML.


TODO
----

* When the rules need input from the enveloping game, a request should
  be made, and it being answered should resume rule execution. This
  could be done using a callback in the state, or maybe by using
  `yield`.
* YAMLization
  * The Python functions that implement actions need to become
    YAML-defined.
* There needs to be a YAML files that defines how to make rolls and how
  to interpret their results.
* Serialization: Turn actors into YAML again.
* Hot upgrade: Reloading YAML files at runtime and migrating the actors
  to the new rule set.
* Precognition: A mechanism to dry-run an action and get a report on all
  possible ways (and their respective probabilities) that the action
  could play out. This will allow for generic game-playin AIs, and for
  supporting user choices.
