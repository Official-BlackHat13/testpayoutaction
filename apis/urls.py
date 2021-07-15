from apis.view_api import payout
from django.urls import path
from drf_yasg import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt import views as jwt_views
from . import  views
schema_view = get_schema_view(
   openapi.Info(
      title="Sabpaisa Payout APIs",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path("", schema_view.with_ui("redoc",cache_timeout=0)),
   #  path("test/",views.bankApiViewtest.as_view()),
    path('token/',jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'),
    path('token/refresh/',jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path("PayoutTransactionRequest/",views.payout.bankApiPaymentView.as_view()),
    #path("addBalance/",lambda a:a),
   #  path("enquiry/",views.bankApiEnquiryView.as_view()),
   #  path("fetchAllLedgers/", views.getLedgers.as_view()),
   #  path("saveLedger/", views.LedgerSaveRequest.as_view()),
   #  path("deleteLedger/", views.DeleteLedger.as_view()),
   #  path("update/", views.UpdateLedger.as_view()),
   #  path("auth/",views.Auth.as_view()),
    path("enc/",views.extras.encryptJSON.as_view()),
   #  path("decrypt/", views.decryptJson.as_view()),
   #  path("enc/",views.encryptJSON.as_view()),
   #  path("decrypt/", views.decryptJson.as_view()),
    path("getLogs/<slug:page>/<slug:length>",views.logs.GetLogs.as_view()),
    path("PayoutTransactionEnquiry/", views.payout.paymentEnc.as_view()),
   #  path("head/",views.tester.as_view()),
   #  path("encHeader/",views.encHeader.as_view()),
    path("addBalance/",views.payout.addBalanceApi.as_view()),
   path("fetch/<slug:page>/<slug:length>",views.extras.fetch.as_view()),
    path("signup/",views.auth.Auth.as_view()),
    path("getLogs/<slug:page>/<slug:length>",views.logs.GetLogs.as_view()),
    path("loginrequest/",views.login.LoginRequestAPI.as_view()),
    path("loginverified/",views.login.LoginVerificationAPI.as_view()),
    path("resendotp/",views.login.ResendLoginOTP.as_view()),
    path("addBeneficiary/",views.beneficiary.addSingleBeneficiary.as_view()),
    path("fetchBeneficiary/",views.beneficiary.fetchBeneficiary.as_view()),
   #  path("updateBeneficiary/",views.updateBeneficiary.as_view()),
   #  path("deleteBeneficiary/",views.deleteBeneficiary.as_view()),
   #  path("addBeneficiary/",views.saveBeneficiary.as_view()),
    path("adminSignup/",views.auth.AuthAdmin.as_view()),
    path("adminLogin/",views.login.LoginRequestAdminAPI.as_view()),
    path("addBeneficiaries/",views.beneficiary.saveBeneficiary.as_view()),
    path("addCharge/",views.charge.addCharge.as_view()),
    path("fetchCharges/",views.charge.fetchCharges.as_view())
   #  path("testicic/",)
   #  path("createTest",views.getTest.as_view()),
   #  path("updateTest/<int:id>",views.updateTest.as_view()),
   #  path("getRoles")
   #  path("test/",views.Test.as_view())
]
