from rest_framework import serializers

from .models import Category, Brand, Product, ProductLine, ProductImage, Attribute, AttributeValue


class CategorySerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="name")

    class Meta:
        model = Category
        fields = ["category_name"]


class BrandSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="name")

    class Meta:
        model = Brand
        fields = ["brand_name"]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        exclude = ("id", "productline")


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ('id', 'name')


class AttributeValueSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(many=False)

    class Meta:
        model = AttributeValue
        fields = ('attribute', "attribute_value")


class ProductLineSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductLine
        fields = ("price", "sku", "stock_qty", "order",
                  "product_image", "attribute_value", )

        def to_representation(self, instance):
            data = super().to_representation(instance)
            av_data = data.pop('attribute')
            attr_values = {}
            for key in av_data:
                attr_values.update(
                    {
                        key['attribute']['id']: key['attribute_value']
                    }
                )
            data.update({"specification": attr_values})
            return data


class ProductSerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name")
    category_name = serializers.CharField(source="category.name")
    product_line = ProductLineSerializer(many=True)

    class Meta:
        model = Product
        fields = (
            "name",
            "slug",
            "description",
            "brand_name",
            "category_name",
            "product_line",
        )
