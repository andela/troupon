"""Generic API configuration."""
import os

from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ServerAPI(APIView):
    """Return Google API key"""

    def get(self, request, *args, **kw):
        key = os.getenv("GOOGLE_SERVER_KEY")
        response = Response(key, status=status.HTTP_200_OK)
        return response
