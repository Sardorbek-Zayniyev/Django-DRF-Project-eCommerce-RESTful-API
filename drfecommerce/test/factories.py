import factory
from drfecommerce.product.models import Category, Brand, Product


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: "Category_%d" % n)


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: "Brand_%d" % n)


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    brand = factory.SubFactory(BrandFactory)
    category = factory.SubFactory(CategoryFactory)
    name = "test_product"
    description = "test_description"
    is_digital = True
