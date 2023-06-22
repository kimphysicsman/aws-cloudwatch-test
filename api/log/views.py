from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import json
import logging
import boto3
import datetime 
from faker import Faker

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
    
    def post(self, request):
        fake = Faker("ko_KR")


        for i in range(0, 15):
            mall_id = 'wendy' if  i % 2 == 0 else 'hani'
            shop_no = '1' if i % 3 == 0 else '2'
            user = fake.name()
            product_no = fake.random.randrange(0, 100)
            order_id = i
            path_name = fake.address()
            event = 'mouseclick'
            value = fake.word()
            is_mobile = True if i % 4 != 0 else False
            
            data = {
                "mall_id": mall_id, 
                "shop_no": shop_no,
                "user": user,
                "product_no": product_no,
                "order_id": order_id,
                "path_name": path_name,
                "event": event,
                "value": value,
                "is_mobile": is_mobile,                
            }

            # print(data)
            self.logger.debug(json.dumps(data))


        return Response({}, status=status.HTTP_200_OK)

class LogView(APIView):
    logger = logging.getLogger(__name__)

    def get(self, request):

        start = datetime.datetime.now()
        start_timestamp = start.timestamp() * 1000

        log_group_name = 'test'
        log_stream_name = 'test'

        client = boto3.client('logs', region_name='ap-northeast-2')
        log_events_response = client.filter_log_events(
                logGroupName=log_group_name,
                startTime=int(1687324392442),
                endTime=int(start_timestamp),
                limit=100,
                filterPattern='{ $.mall_id = wendy }'
                # filterPattern='{ $.method = "post" }'
            )

        end = datetime.datetime.now()
        print("filter_log_events :", end - start)

        # # 각 로그 이벤트의 메시지를 출력합니다.
        # for log_event in log_events_response['events']:
        #     print(json.loads(log_event['message']))


        # log_events_response = client.get_log_events(
        #                 logGroupName=log_group_name,
        #                 logStreamName=log_stream_name
        #             )
        
        # # 각 로그 이벤트의 메시지를 출력합니다.
        # for event in log_events_response['events']:
        #     message = event['message']
        #     # 로그 메시지가 JSON 형태라고 가정하고 파싱
        #     try:
        #         log_data = json.loads(message)
        #         print(log_data)
        #     except json.JSONDecodeError:
        #         pass

        
        # end_2 = datetime.datetime.now()
        # print("log_events_response['events']", len(log_events_response['events']))
        # print("get_log_events :", end_2 - end)

        return Response({'response' : log_events_response}, status=status.HTTP_200_OK)

    def post(self, request):
        
        data = {
            "method": "post",
            "user": "dongwoo",
            "app": "test"
        }

        self.logger.debug(json.dumps(data))

        return Response({}, status=status.HTTP_200_OK)
