from rest_framework import status
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
import json
import boto3
import datetime 
from faker import Faker

"""boto3를 통해 로그데이터를 CloudWatch에 저장하는 함수
"""
def put_log_data_list(data_list):
    # 로그이벤트 리스트 생성
    log_events = []
    for data in data_list:
        log_event = {
            'timestamp': int(datetime.datetime.now().timestamp() * 1000),
            'message': json.dumps(data)
        }
        log_events.append(log_event)

    # CloudWatch 저장소 정보
    log_group_name = 'test2'
    log_stream_name = 'test2'

    client = boto3.client('logs', region_name='ap-northeast-2')

    start = datetime.datetime.now()
    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )
    end = datetime.datetime.now()
    print("=================")
    print("** put_log_data_list() info **")
    print("data_list length:", len(data_list))
    print("time:", end - start)
    print("=================")

    return response

"""boto3를 통해 CloudWatch로부터 로그데이터를 필터링하여 가져오는 함수
"""
def get_filter_log_events():
    log_group_name = 'test2'
    log_stream_name = 'test2'
    filter_pattern = '{ $.mall_id = wendy }'
    client = boto3.client('logs', region_name='ap-northeast-2')

    start = datetime.datetime.now()
    start_timestamp = start.timestamp() * 1000
    response = client.filter_log_events(
            logGroupName=log_group_name,
            logStreamNames=[
                log_stream_name
            ],
            startTime=int(1687324392442),
            endTime=int(start_timestamp),
            limit=10000,
            filterPattern=filter_pattern
        )
    log_events = response["events"]

    end = datetime.datetime.now()
    print("=================")
    print("** get_filter_log_events() info **")
    print("log_events length:", len(log_events))
    print("time:", end - start)
    print("=================")

    return log_events


class HomeView(APIView):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        fake = Faker("ko_KR")

        data_list = []
        for i in range(0, 9999):
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
            data_list.append(data)

        response = put_log_data_list(data_list)


        return Response({
            "message": "done", 
            }, status=status.HTTP_200_OK)

class LogView(APIView):
    def get(self, request):
        log_events = get_filter_log_events()

        data_list = []
        for log_event in log_events:
            data = log_event['message']
            if(len(data_list) < 100):
                data_list.append(json.loads(data))
        
        return Response({'data_list' : data_list}, status=status.HTTP_200_OK)
