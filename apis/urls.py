from django.urls import path
from drf_yasg import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
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
    path("payout/",views.bankApiPaymentView.as_view()),
    path("addBalance/",lambda a:a),
    path("enquiry/",views.bankApiEnquiryView.as_view()),
    path("fetchAllLedgers/", views.getLedger.as_view()),
    path("saveLedger/", views.LedgerSaveRequest.as_view()),
    path("deleteLedger/", views.DeleteLedger.as_view()),
    path("update/", views.UpdateLedger.as_view()),
    path("findByClientCode/", views.findByClientCode.as_view()),
    path("findByClientId/",views.findByClientId.as_view()),
    path("findByTransTime/",views.findByTransTime.as_view())
]
