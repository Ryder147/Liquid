from django.urls import path

from .views import (
    AddCartItemView,
    CancelvoteView,
    DownvoteView,
    RandomGamesView,
    UpvoteView,
    health_check, 
    RegisterView, 
    LoginView, 
    UserView, 
    PaymentView,
    GamesView,
    GameDetailsView,
    ReviewView,
    UservoteView,
    GameRatingView,
    RemoveCartItemView,
    UserCartView,
    OrdersView,
    UserLibraryView
)

urlpatterns = [
    path('health/', health_check),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('payment/',PaymentView.as_view()),
    path('games/', GamesView.as_view()),
    path('gamedetails/<int:id>/', GameDetailsView.as_view()),
    path('gamereviews/<int:id>/', ReviewView.as_view()),
    path('randomgames/<int:count>/', RandomGamesView.as_view()),
    path('upvote/<int:id>/', UpvoteView.as_view()),
    path('downvote/<int:id>/', DownvoteView.as_view()),
    path('cancelvote/<int:id>/', CancelvoteView.as_view()),
    path('uservote/<int:id>/', UservoteView.as_view()),
    path('gamerating/<int:id>/', GameRatingView.as_view()),
    path('addcartitem/<int:id>/', AddCartItemView.as_view()),
    path('removecartitem/<int:id>/', RemoveCartItemView.as_view()),
    path('cart/', UserCartView.as_view()),
    path('orders/', OrdersView.as_view()),
    path('library/', UserLibraryView.as_view()),
]
