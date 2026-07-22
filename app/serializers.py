from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = "__all__"
        read_only_fields = ['id']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password")
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

        attrs["user"] = user
        return attrs