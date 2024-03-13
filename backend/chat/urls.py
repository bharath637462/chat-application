from chat import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    # Authentications
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Chat Messsage
    path('my-messages/<user_id>/', views.MyInbox.as_view()),
    path('get-messages/<sender_id>/<receiver_id>/', views.GetMessages.as_view()),
    path('send-message/', views.SendMessage.as_view()),

    #  Get / Filter Data
    path('profile/<int:pk>/', views.ProfileDetail.as_view()),
    path('search/<username>/', views.SearchUser.as_view()),
]