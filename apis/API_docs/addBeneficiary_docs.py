from drf_yasg import openapi

response_schema_dict = {

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
                "message":"data parsed and saved to database",
                "response_code":"1"
            }
        }
    )
}
request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
        'auth-token(header)': openapi.Schema(type=openapi.TYPE_STRING, description='string'),
        'files': openapi.Schema(type=openapi.TYPE_STRING, description='excelfile'),
    })