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
    "402": openapi.Response(
        description="custom 402 description",
        examples={
            "application/json": {"message":"Not Sufficent Balance","response_code":"0"}
        }
    ),
    "401":openapi.Response(
        description="custom 401 description",
        examples={
            "application/json":{"message":"credential not matched","response_code":"3"}
        }
    ),
    "204":openapi.Response(
        description="custom 204 description",
        examples={
            "application/json":{"message":"error msg","response_code":"2"}
        }
    ),
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'clientCode': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })