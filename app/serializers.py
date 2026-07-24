from rest_framework import serializers
from rest_framework.authentication import authenticate
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ['id']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            age=validated_data.get("age"),
        )

        user.phone = validated_data.get("phone")
        user.age = validated_data.get("age")
        user.bio = validated_data.get("bio")
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only = True)

    def validate(self, attrs):
        user = authenticate(
            email=attrs["email"],
            password=attrs["password"]
        )

        if not user:
            raise serializers.ValidationError("Email yoki parol noto'g'ri.")

        refresh = RefreshToken.for_user(user)

        return {
            "refresh":str(refresh),
            "access":str(refresh.access_token)
        }

class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")

        try:
            token = RefreshToken(RefreshToken)
            return {
                "access":str(token.access_token)
            }

        except TokenError:
            raise serializers.ValidationError("xatolik bor")