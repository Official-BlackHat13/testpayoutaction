from drf_yasg import openapi


response_login_request = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "message": "user created",
    "merchant_id":"client merchant id",
    "response_code": "1",
    "CLIENT_AUTH_KEY": "client auth key",
    "CLIENT_AUTH_IV": "client auth iv",
    "token": {
        "refresh": "refresh token",
        "access": "access token"
    }
}
            

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

response_login_verification = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "message": "user created",
    "merchant_id":"client merchant id",
    "response_code": "1",
    "CLIENT_AUTH_KEY": "client auth key",
    "CLIENT_AUTH_IV": "client auth iv",
    "token": {
        "refresh": "refresh token",
        "access": "access token"
    }
}
            

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
        
    
    })


request_admin=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'username': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'password': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        
    
    })