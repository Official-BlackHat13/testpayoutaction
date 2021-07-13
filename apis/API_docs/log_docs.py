from drf_yasg import openapi
response_dict={

    "200": openapi.Response(
        description="custom 200 description",
        examples={
            "application/json": {
       "data_length": 1,
    "data": "encrypted_data"
    }
}
            

        
    ),
    
   
}