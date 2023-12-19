import rules

from . import enums


@rules.predicate
def is_owner(user, object):
    return object.owner == user


@rules.predicate
def is_public(user, object):
    return object.visibility == enums.Visibility.PUBLIC


rules.add_perm("maps.map_view", is_public | is_owner | rules.is_staff)
rules.add_perm("maps.map_edit", is_owner | rules.is_staff)
rules.add_perm("maps.map_add", is_owner | rules.is_staff)
rules.add_perm("maps.map_delete", is_owner | rules.is_staff)
