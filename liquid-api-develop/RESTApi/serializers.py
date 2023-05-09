from rest_framework import serializers

from .models import Cart, OrderGamesConnection, Orders, Ratings, User, Games, Requirements, Screens, Reviews

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'login', 'password', 'stripe_id']
        extra_kwargs = {
            'password': {'write_only': True},
            'stripe_id': {'write_only': True}
        }

class GamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = '__all__'


class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        exclude = ('id', 'game' ) 
class ScreensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Screens
        exclude = ('id', 'game' ) 

        
class GamedetailSerializer(serializers.ModelSerializer):
    screens = ScreensSerializer(many = True, read_only=True)
    requirements = RequirementsSerializer(many = True, read_only=True)
    class Meta:
        model = Games
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(  
        read_only=True,
        slug_field='login'
     )
    class Meta:
        model = Reviews
        fields = ['user', 'review_text']

class GameReviewSerializer(serializers.ModelSerializer):
    game_id = serializers.IntegerField(source='id')
    game_reviews = ReviewSerializer(many=True)
    class Meta:
        model = Games
        fields = ['game_id', 'game_reviews']

class NewReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ['id', 'review_text', 'published_date', 'game', 'user']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = [
            'id', 
            'create_time', 
            'pay_time', 
            'payment_intent_id', 
            'is_paid',
            'status',
            'user_id',
            'total_price',
            'checkout_session_id'
            ]

class OrderGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGamesConnection
        fields = [
            'id',
            'order',
            'game'
            ]

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        extra_kwargs = {
            'user_id': {'write_only': True}
        }

class OrderViewSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        return obj.payment_intent_id[3:]

    def get_date(self, obj):
        return obj.create_time.strftime("%Y-%m-%d")
    class Meta:
        model = Orders
        exclude=['user_id',"checkout_session_id","create_time","payment_intent_id"]
    