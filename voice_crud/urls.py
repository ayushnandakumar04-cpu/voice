from django.urls import path
from voice_crud.views import SignupRegisterView,GetMeView,FeedBackListCreateView,FeedBackListRetrieveview,FeedbackSummaryView
from rest_framework.authtoken.views import ObtainAuthToken
urlpatterns = [
    path('signup/',SignupRegisterView.as_view()),
    path('me/',GetMeView.as_view()),
    path('feedback/',FeedBackListCreateView.as_view()),
    path('feedback/<int:pk>/',FeedBackListRetrieveview.as_view()),
    path('token',ObtainAuthToken.as_view()),
    path('summary/',FeedbackSummaryView.as_view()),
    
]