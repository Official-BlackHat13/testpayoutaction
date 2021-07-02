from apis import const
from rest_framework import status
from sabpaisa import auth
from datetime import datetime
from ..database_service import Client_model_service
from rest_framework.permissions import AND
from ..models import LedgerModel
from . import Log_model_services
from django.db import connection
from sabpaisa import main
class Ledger_Model_Service:
    def __init__(self,id=None, merchant=None, client_code=None, trans_amount_type=None, type_status=None, amount=None, van=None, trans_type=None, trans_status=None, bank_ref_no=None, customer_ref_no=None, bank_id=None, trans_time=None, bene_account_name=None, bene_account_number=None, bene_ifsc=None, request_header=None, createdBy=None, updatedBy=None, deletedBy=None, created_at=None, deleted_at=None, updated_at=None, status=True, mode=None, charge=None):
        self.id = id
        self.merchant=merchant
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

    def save(self,createdBy, merchant, client_ip_address=None):
        #log_service = Log_model_services.Log_Model_Service(log_type="create",table_name="apis_ledgermodel",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        ledgermodel = LedgerModel()
        ledgermodel.merchant=self.merchant
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

        #start
        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=createdBy, client_ip_address=client_ip_address)

        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        respId = ledgermodel.id
        if(ledgermodel.id<=0):
            return "0"
        resp = str(respId)
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp
        #end
    
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

    def deleteById(id, deletedBy,merchant):
        ledger = LedgerModel.objects.filter(id=id,merchant=merchant)
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            
            ledgerModel.status = False
            ledgerModel.deletedBy = deletedBy
            ledgerModel.deleted_at = datetime.now()
            ledgerModel.save()
            return True
        return False

    # def fetchAll(self):
    #     ledgerModel = LedgerModel.objects.filter(status=True)
    #     return ledgerModel
    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True
    
    @staticmethod
    def getBalance(clientCode,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="get balance",table_name="apis_ledgermodel",remarks="getting balance from apis_ledgermodel table via getBalance stored procedure",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        cursors = connection.cursor()
        cursors.execute('call getBalance("'+clientCode+'",@balance)')
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        print(value)
        log_service.save()
        return value[0][0]

    def update(self,id,merchant):
        ledger = LedgerModel.objects.filter(id=id, merchant=merchant)
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            ledgermodel.id = id
            ledgermodel.merchant = self.merchant
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
            # ledgermodel.deleted_at = ledgermodel.deleted_at
            # ledgermodel.created_at = ledgermodel.created_at
            ledgermodel.created_at = self.created_at
            ledgermodel.status = self.status
            ledgermodel.mode = self.mode
            ledgermodel.charge = self.charge
            ledgermodel.save()
        print("..... ",ledgermodel)
        return ledgermodel.id

        
    @staticmethod
    def getBalance(clientCode):
        cursors = connection.cursor()
        cursors.execute('call getBalance("'+clientCode+'",@balance)')
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        
        print(value)
        return value[0][0]

    def updateTransTime(id, transTime):
        ledger = LedgerModel.objects.filter(id=id)
        print("service ledger = ", ledger)
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("service     ", ledgerModel)
            ledgerModel.updated_at = datetime.now()
            ledgerModel.trans_time = transTime
            ledgerModel.save()
            return True
        return False
