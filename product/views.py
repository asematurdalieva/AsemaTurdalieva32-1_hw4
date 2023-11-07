from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.models import Product, Category, Review
from product.serializers import (ProductSerializer, CategorySerializer, ReviewSerializer,
                                 ProductCreateValidateSerializer, ReviewCreateValidateSerializer,
                                CategoryCreateValidateSerializer)
from django.db.models import Avg
from rest_framework import status


@api_view(['GET', 'POST'])
def products_list_api_view(request):
    if request.method == "GET":

        products = Product.objects.all()
        products_json = ProductSerializer(instance=products, many=True).data

        return Response(data=products_json)
    elif request.method == "POST":
        serializer = ProductCreateValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data={'message': 'Request failed',
                                  'errors': serializer.errors})

        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category = serializer.validated_data.get('category')

        product = Product.objects.create(title=title, description=description, price=price)
        product.category.set(category)
        product.save()

        return Response(status=status.HTTP_201_CREATED,
                        data={'id': product.id, 'title': product.title})


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response(data={'message': 'Product not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        product_json = ProductCreateValidateSerializer(product, many=False).data
        return Response(data=product_json)

    elif request.method == "PUT":
        serializer = ProductCreateValidateSerializer(data=request.data)

        if serializer.is_valid():
            title = serializer.validated_data.get('title')
            description = serializer.validated_data.get('description')
            price = serializer.validated_data.get('price')
            category = serializer.validated_data.get('category')

            product.title = title
            product.description = description
            product.price = price
            product.category.set(category)
            product.save()

            return Response(data={'message': 'Product updated successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(data={'message': 'Invalid data', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': "Product deleted"})

@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == "GET":
        categories = Category.objects.all()
        categories_json = CategorySerializer(categories, many=True).data

        return Response(data=categories_json)

    elif request.method == "POST":
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'id': serializer.instance.id, 'name': serializer.instance.name})
        return Response(data={'message': 'Invalid data'},
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return Response(data={'message': 'Category not found!'},
                        status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        category_json = CategorySerializer(category, many=False).data
        return Response(data=category_json)

    elif request.method == "PUT":
        serializer = CategoryCreateValidateSerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'message': 'Category updated'})
        return Response(data={'message': 'Invalid data'},
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT,
                        data={'message': "Category deleted"})


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == "GET":
        reviews = Review.objects.all()
        reviews_json = ReviewSerializer(reviews, many=True).data

        return Response(data=reviews_json)

    elif request.method == "POST":
        serializer = ReviewCreateValidateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED,
                            data={'id': serializer.instance.id, 'text': serializer.instance.text})
        return Response(status=status.HTTP_400_BAD_REQUEST,
                        data={'message': 'Invalid data',
                              'errors': serializer.errors})


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response(data={'message': 'Review not found!'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        review_json = ReviewCreateValidateSerializer(review, many=False).data
        return Response(data=review_json)

    elif request.method == "PUT":
        serializer = ReviewCreateValidateSerializer(data=request.data)

        if serializer.is_valid():
            text = serializer.validated_data.get('text')
            product_id = serializer.validated_data.get('product_id')  # Get the ID
            stars = serializer.validated_data.get('stars')

            review.text = text
            review.product_id = product_id  # Update with the product ID
            review.stars = stars

            review.save()

            return Response(data={'message': 'Review updated successfully'}, status=status.HTTP_201_CREATED)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT, data={'message': "Review deleted"})


@api_view(['GET'])
def product_reviews_api_view(request):
    reviews = Review.objects.all()
    reviews_json = ReviewSerializer(reviews, many=True).data

    return Response(data=reviews_json)


@api_view(['GET'])
def average_rating_api_view(request):
    average_rating = Review.objects.aggregate(avg_rating=Avg('stars'))
    return Response({'avg_rating': average_rating['avg_rating']})
