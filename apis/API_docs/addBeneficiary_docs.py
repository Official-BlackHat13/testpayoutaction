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



fetch_request=openapi.Schema(
    type=openapi.TYPE_OBJECT, 
    properties={
    "account_number":"account_number",
    "ifsc_code":"ifsc_code"
})

fetch_response={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
    "message": "[{'id': 28, 'full_name': 'full nmae', 'account_number': '987655', 'ifsc_code': '9181991', 'merchant_id': 3, 'created_at': datetime.datetime(2021, 7, 12, 20, 1, 17, 605527, tzinfo=<UTC>), 'deleted_at': None, 'updated_at': None, 'created_by': None, 'deleted_by': None, 'updated_by': None}]",
    "responseCode": "1"
}
        }
    )
}

