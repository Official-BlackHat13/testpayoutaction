from drf_yasg import openapi

response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "200_key1": "200_value_1",
                "200_key2": "200_value_2",
            }
        }
    ),
    "205": openapi.Response(
        description="custom 205 description",
        examples={
            "application/json": {
                "205_key1": "205_value_1",
                "205_key2": "205_value_2",
            }
        }
    ),
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'clientCode': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'query': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
    })