# Based on https://github.com/Koed00/django-q/issues/107#issuecomment-721158308

from time import sleep

from django.utils import timezone
from django_q.brokers.orm import ORM, _timeout
from django_q.conf import Conf


class NamedBroker(ORM):
    def queue_size(self) -> int:
        return self.get_connection().filter(key=self.list_key, lock__lte=_timeout(), extension__name=self.name).count()

    def lock_size(self) -> int:
        return self.get_connection().filter(key=self.list_key, lock__gt=_timeout(), extension__name=self.name).count()

    def purge_queue(self):
        return self.get_connection().filter(key=self.list_key, extension__name=self.name).delete()

    def enqueue(self, task):
        from metadata_catalogue.core.models import OrmQExtension  # noqa

        package = self.get_connection().create(key=self.list_key, payload=task, lock=_timeout())
        OrmQExtension.objects.create(orm_q=package, name=self.name)
        return package.pk

    def dequeue(self):
        tasks = self.get_connection().filter(key=self.list_key, lock__lt=_timeout(), extension__name=self.name)[
            0 : Conf.BULK
        ]
        if tasks:
            task_list = []
            for task in tasks:
                if (
                    self.get_connection()
                    .filter(id=task.id, lock=task.lock, extension__name=self.name)
                    .update(lock=timezone.now())
                ):
                    task_list.append((task.pk, task.payload))
                # else don't process, as another cluster has been faster than us on that task
            return task_list
        # empty queue, spare the cpu
        sleep(Conf.POLL)


class GeneralPurposeBroker(NamedBroker):
    """
    Generic usage broker, for other delayed tasks
    """

    name = "general_purpose"
