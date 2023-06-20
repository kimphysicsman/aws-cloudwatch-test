from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import logging

class LogView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):
        print({
            "url": "log",
            "method": "get",
            })
        
        self.logger.debug("request log get method")

        return render(request, 'index.html')

    def post(self, request):
        print({
            "url": "log",
            "method": "post",
            })
        
        self.logger.debug("request log post method")

        return Response({}, status=status.HTTP_200_OK)
