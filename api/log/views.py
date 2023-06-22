from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging
import boto3
import datetime 

class HomeView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):

        data = {
            "method": "get",
            "user": "dongwoo",
            "app": "test"
        }

        self.logger.debug(json.dumps(data))

        return render(request, 'index.html')

class LogView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):

        now = datetime.datetime.now()
        timestamp = now.timestamp() * 1000

        log_group_name = 'test'
        log_stream_name = 'test'

        client = boto3.client('logs', region_name='ap-northeast-2')

        # log_events_response = client.get_log_events(
        #                 logGroupName=log_group_name,
        #                 logStreamName=log_stream_name
        #             )

        log_events_response = client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(1687324392442),
                endTime=int(timestamp),
                limit=100,
                # filterPattern='{ $.method = post }'
                # filterPattern='{ $.method = "post" }'
            )


        # 각 로그 이벤트의 메시지를 출력합니다.
        # for log_event in log_events_response['events']:
        #     print(log_event['message'])

        return Response({'response' : log_events_response}, status=status.HTTP_200_OK)

    def post(self, request):
        
        data = {
            "method": "post",
            "user": "dongwoo",
            "app": "test"
        }

        self.logger.debug(json.dumps(data))

        return Response({}, status=status.HTTP_200_OK)
