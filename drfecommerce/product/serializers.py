from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ('id',)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ('id',)


class ProductLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductLine
        exclude = ('id',)


class ProductSerializer(serializers.ModelSerializer):
    category = BrandSerializer()
    brand = BrandSerializer()
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        exclude = ('id',)
