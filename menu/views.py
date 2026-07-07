from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .services import get_menu_for_cache


class MenuView(APIView):
    def get(self, request):
        menu = get_menu_for_cache()
        return Response({"menu": menu}, status=status.HTTP_200_OK)
