from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from .fields import OrderField
from django.core.exceptions import ValidationError

# Create your models here.


class ActiveQueryset(models.QuerySet):
    def isactive(self):
        return self.filter(is_active=True)


class Category(MPTTModel):
    parent = TreeForeignKey(
        "self", on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = TreeForeignKey(
        "Category", on_delete=models.SET_NULL, null=True, blank=True
    )
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def __str__(self):
        return self.name


class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    attribute = models.ForeignKey(
        Attribute, on_delete=models.CASCADE, related_name="attribute_value"
    )
    attribute_value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute.name}-{self.attribute_value}"


class ProductLineAttributeValue(models.Model):
    attribute_value = models.ForeignKey(
        AttributeValue,
        on_delete=models.CASCADE,
        related_name="product_attribute_value_av",
    )
    product_line = models.ForeignKey(
        "ProductLine",
        on_delete=models.CASCADE,
        related_name="product_attribute_value_pl",
    )

    class Meta:
        unique_together = ("attribute_value", "product_line")


class ProductLine(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_line"
    )
    attribute_value = models.ManyToManyField(
        AttributeValue,
        through="ProductLineAttributeValue",
        related_name="product_line_attribute_value",
    )
    product_type = models.ForeignKey(
        "ProductType", on_delete=models.PROTECT)

    price = models.DecimalField(decimal_places=2, max_digits=5)
    sku = models.CharField(max_length=100)
    stock_qty = models.IntegerField()
    order = OrderField(unique_for_field="product", blank=True)
    is_active = models.BooleanField(default=False)

    objects = ActiveQueryset.as_manager()

    def clean(self):
        qs = ProductLine.objects.filter(product=self.product)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductLine, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.sku)


class ProductImage(models.Model):
    productline = models.ForeignKey(
        ProductLine, on_delete=models.CASCADE, related_name="product_image"
    )
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField(upload_to=None, default="test.jpg")
    order = OrderField(unique_for_field="productline", blank=True)

    def clean(self):
        qs = ProductImage.objects.filter(productline=self.productline)
        for obj in qs:
            if self.id != obj.id and self.order == obj.order:
                raise ValidationError("Duplicate value.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)


class ProductType(models.Model):
    name = models.CharField(max_length=100)


class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(
        ProductType,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_pt",
    )
    attribute = models.ForeignKey(
        Attribute,
        on_delete=models.CASCADE,
        related_name="product_type_attribute_a",
    )

    class Meta:
        unique_together = ("product_type", "attribute")
