import json
import boto3
import datetime 
import requests
from faker import Faker

from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from requests_aws4auth import AWS4Auth

from api.settings import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    OPENSEARCH_DOMAIN,
)

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
            limit=10000000,
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

"""boto3를 통해 CloudWatch에서 쿼리 실행하는 함수
"""
def request_start_query(query):
    log_group_name = 'test2'
    log_stream_name = 'test2'
    client = boto3.client('logs', region_name='ap-northeast-2')

    start = datetime.datetime.now()
    start_timestamp = start.timestamp() * 1000
    response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(1687324392442),
        endTime=int(start_timestamp),
        queryString=query,
        limit=1000,
    )

    query_id = response['queryId']
    print(query_id)

    while True:
        result = client.get_query_results(
            queryId=query_id
        )

        if result['status'] == 'Scheduled' or result['status'] == 'Running':
            continue

        break

    return result


"""OpenSearch에 데이터 저장 요청하는 함수
"""
def put_data_in_OpenSearch(data):
    username = 'TEST'
    password = AWS_SECRET_ACCESS_KEY

    url = f'{OPENSEARCH_DOMAIN}/test/_doc'
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        url,
        auth=(username, password),
        json=data,
        headers=headers
    )

    print(response.status_code)
    print(response.json())

    return response

"""OpenSearch에 데이터 저장 요청하는 함수
"""
def create_data_in_OpenSearch(data):
    username = 'TEST'
    password = AWS_SECRET_ACCESS_KEY

    url = f'{OPENSEARCH_DOMAIN}/test/_doc'
    headers = {'Content-Type': 'application/json'}

    response = requests.post(
        url,
        auth=(username, password),
        json=data,
        headers=headers
    )

    print(response.status_code)
    print(response.json())

    return response

def create_doc_list_in_OpenSearch(doc_list):
    username = 'TEST'
    password = AWS_SECRET_ACCESS_KEY

    url = f'{OPENSEARCH_DOMAIN}/test/_bulk?filter_path=-items.index._*'
    # url = f'{OPENSEARCH_DOMAIN}/test/_bulk'
    headers = {'Content-Type': 'application/json'}

    bulk_data = ''
    for doc in doc_list:
        bulk_data += json.dumps(doc) + '\n'


    response = requests.post(
        url,
        auth=(username, password),
        headers=headers,
        data=bulk_data,
    )

    print(response.status_code)
    print(response.json())

    return response

def search_doc_in_OpenSearch(index, query):
    # url = f'{OPENSEARCH_DOMAIN}/{index}/_search?filter_path=hits.hits._source,took'
    url = f'{OPENSEARCH_DOMAIN}/{index}/_search'
    username = 'TEST'
    password = AWS_SECRET_ACCESS_KEY

    response = requests.get(url, auth=(username, password), json=query)

    # print(response.status_code)
    # print(response.json())

    return response



def get_aws_auth():
    region = 'ap-northeast-2'  # OpenSearch Service가 생성된 리전으로 변경합니다.
    service = 'es'

    # IAM User 또는 Role의 Credential 정보를 가져옵니다.
    session = boto3.Session()
    credentials = session.get_credentials()

    # AWS4Auth 인증 정보를 생성합니다.
    aws_auth = AWS4Auth(
        credentials.access_key,
        credentials.secret_key,
        region,
        service,
        session_token=credentials.token
    )

    print(aws_auth)

    return aws_auth


def get_fake_data_list(length):
    fake = Faker("ko_KR")

    data_list = []
    for i in range(0, length):
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

    return data_list

class HomeView(APIView):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):

        for j in range(0, 3000):
            data_list = get_fake_data_list(3000)
            
            response = put_log_data_list(data_list)
            print("put_log_data:", j * 3000)

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

    def post(self, request):
        query = '''
            fields @timestamp, @message, @logStream, @log
            | stats count() as log_count by @logStream
        '''

        response = request_start_query(query)

        return Response({
            "response": response
        }, status=status.HTTP_200_OK)


class OpenSearchView(APIView):
    def get(self, reqeust):
        query = {
            "query": {
                "bool": {
                "must": [
                    {"match": {"mall_id": "wendy"}},
                    {"match": {"shop_no": 1}}
                ]
                }
            },
            "size": 10000
        }

        response = search_doc_in_OpenSearch('test', query)

        return Response({
            "response": response.json(),
        }, status=response.status_code)

    def post(self, request):
        data = {
            "mall_id": "mall_id", 
            "shop_no": "shop_no",
            "user": "user",
            "product_no": "product_no",
            "order_id": "order_id",
            "path_name": "path_name",
            "event": "event",
            "value": "value",
            "is_mobile": "is_mobile",                
        }

        response = create_data_in_OpenSearch(data)

        return Response({
            "response": response.json()
        }, status=response.status_code)
    
    def put(self, request):
        result = {
            "success": 0,
            "error": 0,
            "took": 0,
        }

        for i in range(0, 999):
            data_list = get_fake_data_list(10000)

            doc_list = []
            for data in data_list:
                index = {"index": {"_index": "test"}}
                doc_list.append(index)
                doc_list.append(data)
            
            response = create_doc_list_in_OpenSearch(doc_list).json()

            result["took"] += int(response["took"])
            if response["error"]:
                result["error"] += 1
            else:
                result["success"] += 1

            print(i , result["took"])

        return Response({
            "response": result
        }, status=response.status_code)