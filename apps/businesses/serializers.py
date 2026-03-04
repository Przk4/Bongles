from rest_framework import serializers
from apps.businesses.models import Business, BusinessCategory, BusinessReview


class BusinessCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessCategory
        fields = ['id', 'name', 'description', 'icon']


class BusinessReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = BusinessReview
        fields = ['id', 'customer_name', 'rating', 'comment', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']


class BusinessListSerializer(serializers.ModelSerializer):
    reviews_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Business
        fields = [
            'id', 'name', 'logo', 'banner', 'city', 'rating',
            'reviews_count', 'is_open'
        ]
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()


class BusinessDetailSerializer(serializers.ModelSerializer):
    reviews = BusinessReviewSerializer(many=True, read_only=True)
    owner_name = serializers.CharField(source='owner.get_full_name', read_only=True)
    
    class Meta:
        model = Business
        fields = [
            'id', 'owner_name', 'name', 'description', 'logo', 'banner',
            'address', 'city', 'postal_code', 'latitude', 'longitude',
            'phone_number', 'email', 'website', 'opening_time', 'closing_time',
            'is_open', 'rating', 'total_reviews', 'is_verified', 'created_at',
            'updated_at', 'reviews'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'total_reviews']


class BusinessCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = [
            'name', 'description', 'logo', 'banner', 'address', 'city',
            'postal_code', 'latitude', 'longitude', 'phone_number', 'email',
            'website', 'opening_time', 'closing_time', 'is_open'
        ]
