from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    category = TreeForeignKey(
        'Category', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_digital = models.BooleanField(default=False)
