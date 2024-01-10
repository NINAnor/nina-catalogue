import rules

from .conf import settings


@rules.predicate
def always_visible(user, object):
    return True


@rules.predicate
def is_project_owner(user, object):
    return user in object.members.all()


rules.add_perm("nina.project_view", always_visible)
rules.add_perm("nina.project_edit", is_project_owner | rules.is_staff)
rules.add_perm("nina.project_add", rules.is_staff)
rules.add_perm("nina.project_delete", rules.is_staff)
