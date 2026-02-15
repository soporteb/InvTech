from django.db import models


class Location(models.Model):
    site = models.CharField(max_length=120, blank=True)
    floor = models.CharField(max_length=120, blank=True)
    type = models.CharField(max_length=120, blank=True)
    exact_name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['exact_name']

    def __str__(self):
        return self.exact_name


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Status(models.Model):
    name = models.CharField(max_length=120, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
