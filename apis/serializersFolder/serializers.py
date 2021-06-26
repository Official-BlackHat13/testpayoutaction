from rest_framework import serializers
from ..database_models import LedgerModel
class LedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerModel
        fields = ("id", "client", "client_code", "amount",
                  "trans_type", "type_status", "bank_ref_no", "customer_ref_no", "bank", "trans_status", "bene_account_name", "bene_account_number", "bene_ifsc", "request_header", "mode", "charge", "trans_time", "van", "created_at", "deleted_at", "updated_at", "createdBy", "updatedBy", "deletedBy","status")


class CreateLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LedgerModel
        fields = ("client", "client_code", "amount",
                  "trans_type", "type_status", "bank_ref_no", "customer_ref_no", "bank", "trans_status", "bene_account_name", "bene_account_number", "bene_ifsc", "request_header", "mode", "charge", "trans_time", "van", "created_at", "deleted_at", "updated_at", "createdBy", "updatedBy", "deletedBy", "status")
