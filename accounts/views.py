from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import PhoneTokenSerializer

class PhoneTokenView(TokenObtainPairView):
    serializer_class = PhoneTokenSerializer

