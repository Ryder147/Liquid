import random
import jwt, datetime

from django.contrib.auth.hashers import make_password
from django.db.models import Sum

from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


import stripe
from yaml import serialize

from .serializers import OrderViewSerializer,CartItemSerializer, OrderGameSerializer, OrderSerializer, NewReviewSerializer, RatingSerializer, UserSerializer, GamedetailSerializer, GamesSerializer, GameReviewSerializer
from .models import Cart, Orders, Ratings, User, Games, OrderGamesConnection,UserLibrary
from .utils.stripe_hook import get_stripe_api_key

stripe.api_key = get_stripe_api_key()

@api_view(['GET'])
def health_check(request, *args, **kwargs):
    return Response({'message':'Health check passed'}, status=200)

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        data['password'] = make_password(data['password'])
        data['stripe_id'] = stripe.Customer.create(email=data['email'])['id']
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed("User not found")
        
        if not user.check_password(password):
            raise AuthenticationFailed("Wrong password")
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat' : datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        return Response({
            "jwt": token
        })

class UserView(APIView):
    def get(self, request):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)
        serializer = UserSerializer(user)
        return Response(serializer.data)

class PaymentView(APIView):
    def post(self, request):
        token = request.headers.get('Authorization').split()[1]

        user = check_jwt(token)
        items = request.data["games"]
        items_stripe_ids = [Games.objects.filter(id=game_id).first().stripe_id for game_id in items]
        line_items = [{
                "price": item_stripe_id,
                "quantity": 1,
                } for item_stripe_id in items_stripe_ids]
        payment_session = stripe.checkout.Session.create(
            success_url=request.data["success_url"],
            cancel_url=request.data["cancel_url"],
            line_items=line_items,
            mode="payment",
            customer=user.stripe_id
        )

        data = {
            "create_time": datetime.datetime.now(),
            "payment_intent_id": payment_session['payment_intent'],
            'is_paid': False,
            "status": "created",
            "user_id": user.id,
            "total_price": payment_session['amount_total']/100,
            "checkout_session_id": payment_session['id']
        }
        serializer = OrderSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        
        for item in items:
            ogdata = {
                "order":serializer.data["id"],
                "game":item
            }
            ogserializer = OrderGameSerializer(data=ogdata)
            ogserializer.is_valid(raise_exception=True)
            ogserializer.save()

        return Response({"payment_url":payment_session['url']})


def check_jwt(token):
    if not token:
        raise AuthenticationFailed("Unauthenticated!")
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Token Expired, Unauthenticated!")
    
    user = User.objects.filter(id=payload['id']).first()
     
    return user
          
class GamesView(APIView):
    def get(self, request):
        allgames = Games.objects.all()
        serializer = GamesSerializer(allgames, many = True)
        return Response(serializer.data)  

class GameDetailsView(APIView):
    def get(self, request, id):
        gamedetails = Games.objects.filter(id=id)
        serializer = GamedetailSerializer(gamedetails, many = True)
        return Response(serializer.data)
    

class ReviewView(APIView):
    def get(self, request, id):
        reviews = Games.objects.filter(id=id)
        serializer = GameReviewSerializer(reviews, many = True)
        return Response(serializer.data)

    def post(self, request, id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)
        data = request.data
        data["game"]=id
        data["user"]=user.id
        data["published_date"]=datetime.datetime.now().date()
        serializer = NewReviewSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RandomGamesView(APIView):
    def get(self,request,count):
        games = list(Games.objects.all())
        random_games = random.sample(games, count)

        serializer = GamesSerializer(random_games, many=True)
        return Response(serializer.data)

class UpvoteView(APIView):
    def post(self,request,id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)

        Ratings.objects.filter(user=user.id, game=id).delete()
        data = {
            "game" : id,
            "user" : user.id,
            "value" : 1
        }
        serializer = RatingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DownvoteView(APIView):
    def post(self,request,id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)

        Ratings.objects.filter(user=user.id,game=id).delete()
        data = {
            "game" : id,
            "user" : user.id,
            "value" : -1
        }
        serializer = RatingSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class CancelvoteView(APIView):
    def post(self,request,id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)

        Ratings.objects.filter(user=user.id,game=id).delete()
        return Response({"message":"vote canceled"})

class UservoteView(APIView):
    def get(self,request,id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)
        rating = Ratings.objects.filter(user=user.id,game=id).first()
        if rating:
            value = rating.value
        else:
            value = 0
        response = {
            "game_id" : id,
            "user_id" : user.id,
            "rating" : value
        }
        return Response(response)

class GameRatingView(APIView):
    def get(self,request,id):
        game_rating = Ratings.objects.aggregate(Sum('value'))
        print(game_rating)
        response = {
            "game_id" : id,
            "rating" : game_rating['value__sum']
        }
        return Response(response)

class AddCartItemView(APIView):
    def post(self,request,id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)

        Cart.objects.filter(user=user.id,game=id).delete()
        data = {
            "game" : id,
            "user" : user.id,
        }
        serializer = CartItemSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RemoveCartItemView(APIView):
    def post(self,request,id):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)

        Cart.objects.filter(user=user.id,game=id).delete()
        return Response({"message":"Item removed"})

class UserCartView(APIView):
    def get(self,request):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)
        cart = Cart.objects.filter(user=user.id)
        game_ids = cart.values_list('game',flat=True).distinct()
        response = {
            "user":user.id,
            "cart":[]
        }
        for game_id in game_ids:
            game = Games.objects.filter(id=game_id).first()
            serializer = GamesSerializer(game)
            response['cart'].append(serializer.data)
        return Response(response)

class OrdersView(APIView):
    def get(self,request):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)
        orders = Orders.objects.filter(user_id=user.id)
        response = {
            "user_id":user.id,
            "orders":[]
        }
        for order in orders:
            serializer = OrderViewSerializer(order)
            response['orders'].append(serializer.data)
        return Response(response)

class UserLibraryView(APIView):
    def get(self,request):
        token = request.headers.get('Authorization').split()[1]
        user = check_jwt(token)
        user_library = UserLibrary.objects.filter(user=user.id)
        game_ids = user_library.values_list('game',flat=True).distinct()
        response = {
            "user":user.id,
            "library":[]
        }

        for game_id in game_ids:
            game = Games.objects.filter(id=game_id).first()
            serializer = GamesSerializer(game)
            response['library'].append(serializer.data)
        return Response(response)
