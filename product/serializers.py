from rest_framework import serializers
from .models import Category, Product, Review
from django.core.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'products_count']

    def get_products_count(self, obj):
        return obj.product_set.count()


class CategoryCreateValidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

    name = serializers.CharField(min_length=2, max_length=19)

    def create(self, validated_data):
        return Category.objects.create(name=validated_data['name'])


class ReviewSerializer(serializers.ModelSerializer):

    def get_product_title(self, obj):
        return obj.product.title

    class Meta:
        model = Review
        fields = ['product', 'stars', 'text', 'id']


class ReviewCreateValidateSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, min_length=3, max_length=100)
    product_id = serializers.IntegerField(required=True, min_value=1, max_value=1000000)
    stars = serializers.IntegerField(required=True, min_value=1, max_value=5)

    def validate_product_id(self, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError('Product does not exist!')
        return product

    def create(self, validated_data):
        return Review.objects.create(
            text=validated_data['text'],
            product=validated_data['product_id'],  # Use the product_id
            stars=validated_data['stars']
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'category']


class ProductCreateValidateSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=4, max_length=20)
    description = serializers.CharField(required=False, min_length=4)
    price = serializers.IntegerField(required=True, min_value=1, max_value=100000)
    category = CategorySerializer(many=True)
