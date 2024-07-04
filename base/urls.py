from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from . import views

# Routes
urlpatterns = [
    path("", views.endpoints, name="endpoints"),

    path("users/", views.UserListCreateApiView.as_view(), name="users"),
    path("users/<str:pk>/", views.UserDetailApiView.as_view(), name="users-details"),
    path("users-profile/", views.UserProfileListApiView.as_view(),
         name="users-profile"),
    path("users-profile/<str:pk>", views.UserProfileRetrieveUpdateDestroyView.as_view(),
         name="users-profile-detail"),
    path("change-password/", views.ChangePasswordView.as_view(),
         name="change-password"),
    path('password-reset/', views.PasswordResetRequestView.as_view(),
         name='password-reset-request'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),

    path("signin/", views.CustomTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),

    path("translation/", views.TranslationRequestListCreateApiView.as_view(),
         name="translation"),
    path("translation/<str:pk>/", views.TranslationRequestRetrieveUpdateDestroyApiView.as_view(),
         name="translation-details"),

    path("text-to-speech/", views.TextToSpeechRequestListCreateApiView.as_view(),
         name="text-to-speech"),
    path("text-to-speech/<str:pk>/", views.TextToSpeechRequestRetrieveUpdateDestroyApiView.as_view(),
         name="text-to-speech-detail"),

    path("speech-to-text/", views.SpeechToTextRequestListCreateApiView.as_view(),
         name="speech-to-text-detail"),
    path("speech-to-text/<str:pk>/", views.SpeechToTextRequestRetrieveUpdateDestroyApiView.as_view(),
         name="speech-to-text-detail"),

    path("saved-pharse/", views.SavedPhraseListCreateApiView.as_view(),
         name="saved-phrase"),
    path("saved-pharse/<str:pk>/", views.SavedPhraseRetrieveUpdateDestroyApiView.as_view(),
         name="saved-phrase-detail")
]
