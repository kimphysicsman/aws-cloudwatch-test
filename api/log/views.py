from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import logging
import boto3

class HomeView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):

        self.logger.debug({
            "method": "get",
            "user": "dongwoo",
            "app": "test"
        })

        return render(request, 'index.html')

class LogView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):
        client = boto3.client('logs', region_name='ap-northeast-2')        
        log_group_name = 'test'
        log_stream_name = 'test'

        log_events_response = client.get_log_events(
                        logGroupName=log_group_name,
                        logStreamName=log_stream_name
                    )

        # log_events_response = client.filter_log_events(
        #         logGroupName=log_group_name,
        #         filterPattern='request'
        #     )


        # 각 로그 이벤트의 메시지를 출력합니다.
        for log_event in log_events_response['events']:
            print(log_event['message'])

        return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        
        self.logger.debug({
            "method": "post",
            "user": "dongwoo",
            "app": "test"
        })

        return Response({}, status=status.HTTP_200_OK)
