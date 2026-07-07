from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class PhoneTokenSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone_number"] = serializers.CharField()

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get("request"),
            phone_number=attrs["phone_number"],
            password=attrs["password"],
        )

        if not user:
            raise serializers.ValidationError("invalid phone number or password")

        refresh = self.get_token(user)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}
