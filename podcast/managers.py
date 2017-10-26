from django.db.models import Manager, Q
from django.utils import timezone


class EpisodeManager(Manager):
    def is_public(self):
        return self.get_queryset().filter(status='public', pub_date__lte=timezone.now())

    def is_public_or_secret(self):
        return self.get_queryset().filter(Q(status='public', pub_date__lte=timezone.now()) | Q(status='secret'))
