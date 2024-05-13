from django.db import models
from flourish_follow.models import Contact


class PreFlourishContactManager(models.Manager):
    def get_queryset(self):
        """ Return only objects from pre-flourish
        """
        qs = super().get_queryset()
        return qs.filter(subject_identifier__icontains='P')


class PreFlourishContact(Contact):

    objects = PreFlourishContactManager()

    class Meta:
        proxy = True
