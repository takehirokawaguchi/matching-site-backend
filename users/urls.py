from django.urls import path, include
from users.views import *


urlpatterns = [
    path('auth/', include('djoser.urls.jwt')),
    # path('profile/<int:pk>/', UserDetailView.as_view(),name='profile-detail'),
    path('profile/<int:pk>/', UserDetailView.as_view(),name='profile-detail'),
    path('profile/<int:pk>/update/', UserUpdateView.as_view(),name='profile-update'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('messages/<user_id>/', MyInbox.as_view(), name='my-messages'),
    path('get-messages/<sender_id>/<receiver_id>/', GetMessages.as_view(), name='get-messages'),
    path('get-all-messages/', GetAllMessages.as_view(), name='get-all-messages'),
    path('send-message/', SendMessage.as_view(), name='send-messages'),
    path('search/<username>/', SearchUser.as_view(), name='search-user'),
]