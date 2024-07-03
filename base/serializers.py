from rest_framework import serializers
from django.utils.dateformat import DateFormat
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        # Assuming userprofile is a related name on the user model
        userprofile_id = user.userprofile.id if hasattr(
            user, 'userprofile') else None

        data['profile_id'] = userprofile_id
        return data


class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'fullname',
            'email',
            'password',
            'date_joined'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = super().create(validated_data)
        user.set_password(password)
        user.save()

        return user

    def get_date_joined(self, obj):
        # Format the date_joined field as "June 22, 2020"
        return DateFormat(obj.date_joined).format('F j, Y')


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        try:
            user = CustomUser.objects.get(email=value)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(
                "User with this email does not exist.")
        return value


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=4)
    new_password = serializers.CharField(max_length=128)

    def validate(self, attrs):
        email = attrs.get('email')
        otp = attrs.get('otp')
        new_password = attrs.get('new_password')

        try:
            user = CustomUser.objects.get(email=email)
            otp_record = PasswordResetOTP.objects.get(
                user=user, otp=otp, is_used=False)
        except (CustomUser.DoesNotExist, PasswordResetOTP.DoesNotExist):
            raise serializers.ValidationError("Invalid email or OTP.")

        if otp_record.is_used:
            raise serializers.ValidationError(
                "This OTP has already been used.")

        attrs['user'] = user
        return attrs

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        otp_record = PasswordResetOTP.objects.get(
            user=user, otp=self.validated_data['otp'])
        otp_record.is_used = True
        otp_record.save()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'id',
            'profile_pic',
            'user',
        ]


class TranslationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranslationRequest
        fields = [
            'id',
            'user',
            'source_text',
            'translated_text',
            'source_language',
            'target_language',
            'timestamp',
        ]


class TextToSpeechRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TextToSpeechRequest
        fields = [
            "id",
            "user",
            "text",
            "language",
            "audio_file",
            "timestamp",
        ]


class SpeechToTextRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpeechToTextRequest
        fields = [
            "id",
            "user",
            "audio_file",
            "language",
            "transcribed_text",
            "timestamp",
        ]


class SavedPhraseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavedPhrase
        fields = [
            "id",
            "user",
            "phrase",
            "language",
            "timestamp",
        ]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is not correct")
        return value

    def validate_new_password(self, value):
        validate_password(value)
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
