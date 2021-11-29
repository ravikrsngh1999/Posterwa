from rest_framework import serializers
from .models import *




class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = "__all__"



class SubCategorySerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	class Meta:
		model = SubCategory
		fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
	subcategory = SubCategorySerializer()
	class Meta:
		model = Product
		fields = "__all__"
