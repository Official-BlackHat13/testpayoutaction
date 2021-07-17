from apis.database_service.Slab_model_services import Slab_Model_Service
from rest_framework.views import APIView
from rest_framework.response import *
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from ..API_docs import slab_docs



class SlabView(APIView):
    @swagger_auto_schema(request_body=slab_docs.request,responses=slab_docs.response)
    def post(self,req):
        try:
            merchant_id = req.data["merchant_id"]
            max_amount = req.data["max_amount"]
            min_amount = req.data["min_amount"]
            slabview = Slab_Model_Service(merchant_id=merchant_id,min_amount=min_amount,max_amount=max_amount)
            if slabview.save()==None:
                return Response({"message":"slab for this merchant already exist","response_code":"0"},status=status.HTTP_226_IM_USED)
            return Response({"message":"slab Added","response_code":"1"},status=status.HTTP_200_OK)
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({"message":"some Technical Error","Response_code":"2",},status=status.HTTP_500_INTERNAL_SERVER_ERROR)