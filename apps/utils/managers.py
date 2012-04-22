# -*- coding: utf-8 -*-

from django.db import models
from django.db.models.query import QuerySet


class PublishedMixin(object):
    def published(self):
        return self.filter(is_published=True)

class PublishedQuerySet(QuerySet, PublishedMixin):
    pass

class PublishedManager(models.Manager, PublishedMixin):
    def get_query_set(self):
        return PublishedQuerySet(self.model, using=self._db)

class SideblockMixin(object):
    def sideblock(self):
        return self.filter(is_published=True, is_sideblock=True)

class SideblockQuerySet(QuerySet, SideblockMixin):
    pass

class SideblockManager(models.Manager, SideblockMixin):
    def get_query_set(self):
        return SideblockQuerySet(self.model, using=self._db)


#class PublishedManager(models.Manager):
#    def get_query_set(self):
#        return super(PublishedManager, self).get_query_set().filter(is_published=True)
