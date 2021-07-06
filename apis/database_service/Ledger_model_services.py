from apis import const
from rest_framework import status

from datetime import datetime
from ..models import LedgerModel
from ..models import ModeModel
from ..models import ChargeModel
from . import Log_model_services
from django.db import connection

class Ledger_Model_Service:
    def __init__(self, client_id=None, client_code=None, trans_amount_type=None,type_status=None, amount=None, van=None, trans_type=None, trans_status=None, bank_ref_no=None, customer_ref_no=None, bank_id=None, trans_time=None, bene_account_name=None, bene_account_number=None, bene_ifsc=None, request_header=None, createdBy=None, updatedBy=None, deletedBy=None, created_at=None, deleted_at=None, updated_at=None, status=True, mode=None, charge=None):
        self.client_id=client_id
        self.client_code=client_code
        self.amount=amount
        self.trans_type=trans_type
        self.trans_status = trans_status
        self.bank_ref_no=bank_ref_no
        self.customer_ref_no=customer_ref_no
        self.trans_amount_type = trans_amount_type
        self.bank_id=bank_id
        self.trans_time=trans_time
        self.type_status=type_status
        self.bene_account_name=bene_account_name
        self.bene_account_number=bene_account_number
        self.bene_ifsc=bene_ifsc
        
        self.request_header=request_header
        self.van=van
        self.createdBy=createdBy
        self.updatedBy=updatedBy
        self.deletedBy=deletedBy
        self.created_at=created_at
        self.deleted_at = deleted_at
        self.updated_at=updated_at
        self.status = status
        self.mode = mode
        self.charge = charge
    def save(self,client_ip_address=None):
        log_service = Log_model_services.Log_Model_Service(log_type="create",table_name="apis_ledgermodel",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        ledgermodel = LedgerModel()
        ledgermodel.client=self.client_id
        ledgermodel.client_code=self.client_code
        ledgermodel.amount=self.amount
        ledgermodel.trans_type=self.trans_type
        ledgermodel.type_status=self.type_status
        ledgermodel.trans_status=self.trans_status
        ledgermodel.bank_ref_no=self.bank_ref_no
        ledgermodel.customer_ref_no=self.customer_ref_no
        ledgermodel.bank=self.bank_id
        ledgermodel.trans_time = self.trans_time
        ledgermodel.trans_amount_type = self.trans_amount_type
        ledgermodel.van=self.van
        ledgermodel.bene_account_name=self.bene_account_name
        ledgermodel.bene_account_number=self.bene_account_number
        ledgermodel.bene_ifsc=self.bene_ifsc
        ledgermodel.request_header=self.request_header
        ledgermodel.createdBy=self.createdBy
        ledgermodel.updatedBy = self.updatedBy
        ledgermodel.deletedBy=self.deletedBy
        ledgermodel.created_at = self.created_at
        ledgermodel.deleted_at = self.deleted_at
        ledgermodel.updated_at = self.updated_at
        ledgermodel.status = self.status
        ledgermodel.mode=self.mode
        ledgermodel.charge = self.charge
        ledgermodel.save()
        log_service.table_id=ledgermodel.id
        log_service.save()
        # Log_model_services.Log_Model_Service()
        return ledgermodel.id
    def fetch_by_clientid(self,client_id,client_ip_address,created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_ledgermodel",remarks="fetching all records from ledger table by client id",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        ledgerModels=LedgerModel.objects.filter(client=client_id)
        log_service.save()
        return ledgerModels
    def fetch_by_clientcode(self,client_code,client_ip_address,created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_ledgermodel",remarks="fetching all records from ledger table by client code ",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        ledgerModels=LedgerModel.objects.filter(client_code=client_code)
        log_service.save()
        return ledgerModels
    def fetch_by_id(self,id,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_ledgermodel",remarks="fetching record from ledger table by primary key ",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        ledgerModels=LedgerModel.objects.get(id=id)
        log_service.table_id=ledgerModels.id
        log_service.save()
        return ledgerModels
    def fetch_by_van(self,van,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_ledgermodel",remarks="fetching all records from ledger table by van ",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        ledgerModels=LedgerModel.objects.filter(van=van)
        log_service.save()
        return ledgerModels
    def update_status(self,id,status,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="update",table_name="apis_ledgermodel",remarks="updating status from ledger table for the record fetched by id ",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        ledgerModel=LedgerModel.objects.get(id=id)
        ledgerModel.trans_status=status
        ledgerModel.save()
        log_service.table_id=ledgerModel.id
        log_service.save()
        return ledgerModel

    def fetchAll(self):
        ledgerModel = LedgerModel.objects.filter(status=True)
        return ledgerModel
    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True
    
    @staticmethod
    def getBalance(merchant_id,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="get balance",table_name="apis_ledgermodel",remarks="getting balance from apis_ledgermodel table via getBalance stored procedure",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        cursors = connection.cursor()
        cursors.execute('call getBalance("'+merchant_id+'",@balance)')
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        print(value)
        log_service.save()
        return value[0][0]
    @staticmethod
    def calculate_charge(mode,amount,client_ip_address):
        mode = ModeModel.objects.filter(mode=mode)
        charge=ChargeModel.objects.filter(mode=mode[0].id,min_amount__lt=amount,max_amount__gt=amount)
        charge_amount=0
        if(len(charge)>0 and charge[0].charge_percentage_or_fix=="percentage"):
            charge_amount=(amount/100)*charge[0].charge
            return charge_amount
        elif (len(charge)>0 and charge[0].charge_percentage_or_fix=="fix"):
            return charge[0].charge
        else:
            None
            



class fetchAllLedgersService:
    def fetchAll():
        ledgerModel = LedgerModel.objects.filter(status=True)
        return ledgerModel

def deleteById(id,deletedBy):
    ledger = LedgerModel.objects.filter(id=id)
    print("service ledger = ",ledger)
    if(len(ledger)>0):
        ledgermodel = LedgerModel()
        ledgerModel = ledger[0]
        print("service     ", ledgerModel)
        ledgerModel.status = False
        ledgerModel.deletedBy = deletedBy
        ledgerModel.deleted_at = datetime.now()
        ledgerModel.save()
        return True
    return False

def findById(id):
    ledger = LedgerModel.objects.filter(id=id)
    if(len(ledger)>0):
        return True
    else:
        return False

#update
class Ledger_update_Model_Service:
    def __init__(self, id=None,client_id=None, client_code=None, type_status=None, amount=None, van=None, trans_type=None, trans_status=None, bank_ref_no=None, customer_ref_no=None, bank_id=None, trans_time=None, bene_account_name=None, bene_account_number=None, bene_ifsc=None, request_header=None, createdBy=None, updatedBy=None, deletedBy=None, created_at=None, deleted_at=None, updated_at=None, status=True, mode=None, charge=None):
        self.id= id
        self.client_id = client_id
        self.client_code = client_code
        self.amount = amount
        self.trans_type = trans_type
        self.trans_status = trans_status
        self.bank_ref_no = bank_ref_no
        self.customer_ref_no = customer_ref_no
        self.bank_id = bank_id
        self.trans_time = trans_time
        self.type_status = type_status
        self.bene_account_name = bene_account_name
        self.bene_account_number = bene_account_number
        self.bene_ifsc = bene_ifsc
        self.request_header = request_header
        self.van = van
        self.createdBy = createdBy
        self.updatedBy = updatedBy
        self.deletedBy = deletedBy
        self.updated_at = updated_at
        self.status = status
        self.mode = mode
        self.charge = charge

    def save(self):
        ledgermodel = LedgerModel()
        ledgermodel.id = self.id
        ledgermodel.client = self.client_id
        ledgermodel.client_code = self.client_code
        ledgermodel.amount = self.amount
        ledgermodel.trans_type = self.trans_type
        ledgermodel.type_status = self.type_status
        ledgermodel.trans_status = self.trans_status
        ledgermodel.bank_ref_no = self.bank_ref_no
        ledgermodel.customer_ref_no = self.customer_ref_no
        ledgermodel.bank = self.bank_id
        ledgermodel.trans_time = self.trans_time
        ledgermodel.van = self.van
        ledgermodel.bene_account_name = self.bene_account_name
        ledgermodel.bene_account_number = self.bene_account_number
        ledgermodel.bene_ifsc = self.bene_ifsc
        ledgermodel.request_header = self.request_header
        ledgermodel.createdBy = self.createdBy
        ledgermodel.updatedBy = self.updatedBy
        ledgermodel.deletedBy = self.deletedBy
        
        ledgermodel.updated_at = self.updated_at
        ledgermodel.status = self.status
        ledgermodel.mode = self.mode
        ledgermodel.charge = self.charge
        ledgermodel.save()
        return ledgermodel.id

   
