import rules

from . import enums
from .conf import settings


@rules.predicate
def is_owner(user, object):
    return object.owner == user


@rules.predicate
def is_public(user, object):
    return object.visibility == enums.Visibility.PUBLIC


if not settings.MAPS_CUSTOM_RULES:
    rules.add_perm("maps.map_view", is_public | is_owner | rules.is_staff)
    rules.add_perm("maps.map_edit", is_owner | rules.is_staff)
    rules.add_perm("maps.map_add", is_owner | rules.is_staff)
    rules.add_perm("maps.map_delete", is_owner | rules.is_staff)

    rules.add_perm("maps.portal_view", is_public | is_owner | rules.is_staff)
    rules.add_perm("maps.portal_edit", is_owner | rules.is_staff)
    rules.add_perm("maps.portal_add", is_owner | rules.is_staff)
    rules.add_perm("maps.portal_delete", is_owner | rules.is_staff)
