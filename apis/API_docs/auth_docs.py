from drf_yasg import openapi

response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message":"Payout done",
                "response_code":"1"
            },
            

        }
    ),
    "409": openapi.Response(
        description="custom 402 description",
        examples={
            "application/json":{
    "message": "some error",
    "error":"error args"
}
        }
    ),
   
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        "email":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        "client_id":openapi.Schema(type=openapi.TYPE_INTEGER, description='string'),
        "client_code":openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    
    })