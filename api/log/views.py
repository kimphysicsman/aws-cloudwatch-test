from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import logging
import boto3

class HomeView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):

        self.logger.debug("request home get method")

        return render(request, 'index.html')

class LogView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):
        client = boto3.client('logs')        
        log_group_name = 'test'

        response = client.describe_log_streams(logGroupName=log_group_name)

        # 모든 로그 스트림을 반복하면서 각각의 로그 이벤트를 가져옵니다.
        for log_stream in response['logStreams']:
            log_stream_name = log_stream['logStreamName']
            print('------' , log_stream_name, '--------')

            # 각 로그 스트림의 로그 이벤트를 가져옵니다.
            log_events_response = client.get_log_events(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )

            # 각 로그 이벤트의 메시지를 출력합니다.
            for log_event in log_events_response['events']:
                print(log_event['message'])

        return Response({}, status=status.HTTP_200_OK)

    def post(self, request):
        print({
            "url": "log",
            "method": "post",
            })
        
        self.logger.debug("request log post method")

        return Response({}, status=status.HTTP_200_OK)
