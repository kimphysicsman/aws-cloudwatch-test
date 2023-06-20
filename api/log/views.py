from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView


class LogView(APIView):
    def get(self, request):
        print({
            "url": "log",
            "method": "get",
            })
        return render(request, 'index.html')

    def post(self, request):
        print({
            "url": "log",
            "method": "post",
            })
        return Response({}, status=status.HTTP_200_OK)
