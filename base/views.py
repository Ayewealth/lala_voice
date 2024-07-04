from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail

from .models import *
from .serializers import *
# Create your views here.


@api_view(['GET'])
def endpoints(request):
    data = [
        'signin/',
        'token/refresh/',

        'users/',
        'users/{id}/',
        'users-profile/',
        'change-password/',
        'password-reset/',
        'password-reset-confirm/',

        'translation/',
        'translation/{id}/',

        'text-to-speech/',
        'text-to-speech/{id}/',

        'speech-to-text/',
        'speech-to-text/{id}/',

        'saved-phrase/',
        'saved-phrase/{id}/'
    ]
    return Response(data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class UserProfileListApiView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserProfileRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class TranslationRequestListCreateApiView(generics.ListCreateAPIView):
    queryset = TranslationRequest.objects.all()
    serializer_class = TranslationRequestSerializer
    permission_classes = [IsAuthenticated]


class TranslationRequestRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TranslationRequest.objects.all()
    serializer_class = TranslationRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class TextToSpeechRequestListCreateApiView(generics.ListCreateAPIView):
    queryset = TextToSpeechRequest.objects.all()
    serializer_class = TextToSpeechRequestSerializer
    permission_classes = [IsAuthenticated]


class TextToSpeechRequestRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TextToSpeechRequest.objects.all()
    serializer_class = TextToSpeechRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class SpeechToTextRequestListCreateApiView(generics.ListCreateAPIView):
    queryset = SpeechToTextRequest.objects.all()
    serializer_class = SpeechToTextRequestSerializer
    permission_classes = [IsAuthenticated]


class SpeechToTextRequestRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SpeechToTextRequest.objects.all()
    serializer_class = SpeechToTextRequestSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class SavedPhraseListCreateApiView(generics.ListCreateAPIView):
    queryset = SavedPhrase.objects.all()
    serializer_class = SavedPhraseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SavedPhrase.objects.filter(user=self.request.user)


class SavedPhraseRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SavedPhrase.objects.all()
    serializer_class = SavedPhraseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "pk"


class ChangePasswordView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        user = CustomUser.objects.get(email=email)
        otp_record, created = PasswordResetOTP.objects.get_or_create(
            user=user, is_used=False)
        otp_record.generate_otp()

        send_mail(
            'Your Password Reset OTP',
            f'Your OTP for password reset is: {otp_record.otp}',
            'your_email',
            [email],
            fail_silently=False,
        )

        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
