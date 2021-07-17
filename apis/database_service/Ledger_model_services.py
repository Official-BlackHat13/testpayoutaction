from requests.api import request
from apis import const
import string
import random
from rest_framework import status
from sabpaisa import auth
from datetime import datetime
from apis.Utils.generater import *
from ..database_service import Client_model_service
from rest_framework.permissions import AND
from ..models import LedgerModel,ModeModel


from ..models import ChargeModel

from . import Log_model_services
from django.db import connection
from sabpaisa import main
import pytz
class Ledger_Model_Service:
    def __init__(self,id=None, merchant=None,client_code=None,linked_ledger_id=None,payout_trans_id=None,trans_amount_type=None, type_status=None, amount=None, van=None, trans_type=None, trans_status=None, bank_ref_no=None, customer_ref_no=None, bank_id=None, trans_time=None, bene_account_name=None, bene_account_number=None, bene_ifsc=None, request_header=None, createdBy=None, updatedBy=None, deletedBy=None, created_at=None, deleted_at=None, updated_at=None, status=True, mode=None, charge=None):
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
        self.linked_ledger_id=linked_ledger_id
        self.type_status=type_status
        self.bene_account_name=bene_account_name
        self.bene_account_number=bene_account_number
        self.bene_ifsc=bene_ifsc
        self.payout_trans_id=payout_trans_id
        self.request_header=request_header
        self.van=van
        self.createdBy=createdBy
        self.updatedBy=updatedBy
        self.deletedBy=deletedBy
        self.created_at=created_at
        self.deleted_at = deleted_at
        self.updated_at=updated_at
        # self.status = status
        self.mode = mode
        self.charge = charge
    def to_json(self):
        json  = {}
        json["amount"]=self.amount
        json['customer_ref_no']=self.customer_ref_no
        json["trans_time"]=self.trans_time
        json['payout_trans_id']=self.payout_trans_id
        json['charge']=self.charge
        json['mode']=self.mode
        json["bene_account_name"]=self.bene_account_name
        json['bene_account_number']=self.bene_account_number
        json['bene_ifsc']=self.bene_ifsc
        json["trans_status"]=self.trans_status
        return json

    def save(self,createdBy, client_ip_address=None):
        #log_service = Log_model_services.Log_Model_Service(log_type="create",table_name="apis_ledgermodel",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        ledgermodel = LedgerModel()
        ledgermodel.merchant=self.merchant
        ledgermodel.client_code=self.client_code
        ledgermodel.amount=self.amount
        ledgermodel.trans_type=self.trans_type
        ledgermodel.type_status=self.type_status
        ledgermodel.trans_status=self.trans_status
        ledgermodel.created_at=datetime.now()
        ledgermodel.bank_ref_no=self.bank_ref_no
        ledgermodel.customer_ref_no=self.customer_ref_no
        ledgermodel.bank=self.bank_id
        ledgermodel.trans_time = self.trans_time
        ledgermodel.payout_trans_id=self.payout_trans_id
        ledgermodel.trans_amount_type = self.trans_amount_type
        ledgermodel.van=self.van
        ledgermodel.bene_account_name=self.bene_account_name
        ledgermodel.bene_account_number=self.bene_account_number
        ledgermodel.bene_ifsc=self.bene_ifsc
        ledgermodel.request_header=self.request_header
        ledgermodel.createdBy=self.createdBy
        ledgermodel.updatedBy = self.updatedBy
        ledgermodel.linked_ledger_id=self.linked_ledger_id
        ledgermodel.deletedBy=self.deletedBy
        # ledgermodel.created_at = self.created_at
        ledgermodel.deleted_at = self.deleted_at
        ledgermodel.updated_at = self.updated_at
        # ledgermodel.status = self.status
        ledgermodel.mode=self.mode
        ledgermodel.charge = self.charge
        ledgermodel.save()

        #start
        # clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
        #     id=self.merchant, created_by=createdBy, client_ip_address=client_ip_address)

        # authKey = clientModel.auth_key
        # authIV = clientModel.auth_iv
        # respId = ledgermodel.id
        # if(ledgermodel.id<=0):
        #     return "0"
        # resp = str(respId)
        # encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        # return encResp
        return ledgermodel.id
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
    @staticmethod
    def fetch_customer_ref_no(customer_ref_no,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="fetch",table_name="apis_ledgermodel",remarks="fetching all records from ledger table by van ",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        ledgerModels=LedgerModel.objects.filter(customer_ref_no=customer_ref_no)
        log_service.save()
        return ledgerModels

    def update_status(self,id,status,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="update",table_name="apis_ledgermodel",remarks="updating status from ledger table for the record fetched by id ",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)

        ledgerModel=LedgerModel.objects.get(id=id)
        ledgerModel.trans_status=status
        ledgerModel.updated_at=datetime.now(pytz.timezone('Asia/Kolkata'))
        ledgerModel.save()
        log_service.table_id=ledgerModel.id
        
        log_service.save()
        return ledgerModel

    def deleteById(id, deletedBy,merchant,client_ip_address,createdBy):
        log_service = Log_model_services.Log_Model_Service(log_type="delete", table_name="apis_ledgermodel", remarks="deleting records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=createdBy)
        ledger = LedgerModel.objects.filter(id=id,merchant=merchant)
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            
            ledgerModel.status = False
            ledgerModel.deletedBy = deletedBy
            ledgerModel.deleted_at = datetime.now()
            ledgerModel.save()
            log_service.table_id = id
            log_service.save()
            return True
        return False

    # def fetchAll(self):
    #     ledgerModel = LedgerModel.objects.filter(status=True)
    #     return ledgerModel
    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True
    
    @staticmethod
    def getBalance(merchant_id,client_ip_address,created_by):
        log_service=Log_model_services.Log_Model_Service(log_type="get balance",table_name="apis_ledgermodel",remarks="getting balance from apis_ledgermodel table via getBalance stored procedure",client_ip_address=client_ip_address,server_ip_address=const.server_ip,created_by=created_by)
        
        cursors = connection.cursor()
        print(merchant_id)
        cursors.execute("call getBalance('"+merchant_id+"',@balance,@cred,@deb)")
        cursors.execute("select @balance")
        # cursors.execute("Call getAmount("'credited'",5,@cred);")
        # cursors.execute("Call getAmount("'debited'",5,@deb);")
        # cursors.execute("")
        value = cursors.fetchall()
        cursors.close()
        print(value[0][0])
        log_service.save()
        return int(value[0][0])
    @staticmethod
    def calculate_charge(merchant_id,mode,amount,client_ip_address):
        mode = ModeModel.objects.filter(mode=mode)
        print(mode[0].id)
        charge=ChargeModel.objects.filter(mode=mode[0].id,min_amount__lt=amount,max_amount__gt=amount,merchant_id=merchant_id)
        # print(charge[0].charge_percentage_or_fix)
        charge_amount=0
        if(len(charge)>0 and charge[0].charge_percentage_or_fix=="percentage"):
            charge_amount=(amount/100)*charge[0].charge
            return charge_amount
        elif (len(charge)>0 and charge[0].charge_percentage_or_fix=="fix"):
            print(charge[0].charge)
            return charge[0].charge
        else:
            return 0
            


    def update(self,id,merchant,client_ip_address,created_by):
        log_service = Log_model_services.Log_Model_Service(log_type="update", table_name="apis_ledgermodel", remarks="updating records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        log_service.table_id = id
        log_service.save()
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
        return ledgermodel.id

        
    # @staticmethod
    # def getBalance(clientCode):
    #     cursors = connection.cursor()
    #     cursors.execute('call getBalance("'+clientCode+'",@balance)')
    #     cursors.execute("select @balance")
    #     value = cursors.fetchall()
    #     cursors.close()
        
    #     print(value)
    #     return value[0][0]

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

    def addBal(decResp, client_ip_address,merchant,clientCode):
        log_service = Log_model_services.Log_Model_Service(log_type="create", table_name="apis_ledgermodel", remarks="saving records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=decResp.get("created_by"))
        ledgermodel = LedgerModel()
        ledgermodel.amount = decResp.get("amount")
        modeOfTrans = decResp.get("mode")
        m = ModeModel.objects.filter(mode = modeOfTrans)
        ledgermodel.mode = m[0].id
        ledgermodel.bank_ref_no = const.bank_ref_no
        ledgermodel.trans_amount_type = "credited"
        ledgermodel.trans_type = "payin"
        ledgermodel.type_status = "Generated"
        ledgermodel.request_header = "request header"
        bankResp = "NULL"
        ledgermodel.remarks = " "
        ledgermodel.merchant = merchant
        ledgermodel.client_code = clientCode
        #CR06e65070-dbd6-11eb-9816-507b9d006cb8
        ledgermodel.customer_ref_no = generate_unique_customerRef()
        ledgermodel.bank = const.bank
        ledgermodel.trans_time = datetime.now()
        ledgermodel.van = " "
        ledgermodel.bene_account_name = const.bene_account_name
        ledgermodel.bene_account_number = const.bene_account_number
        ledgermodel.bene_ifsc = const.bene_ifsc
        ledgermodel.createdBy = "merchantID :: "+str(merchant)
        ledgermodel.created_at = datetime.now()
        ledgermodel.status = True
        ledgermodel.trans_status = "Success"#success
        ledgermodel.payout_trans_id = generate_token()
        ledgermodel.charge = 1.0
        ledgermodel.save()  
        log_service.table_id = ledgermodel.id
        log_service.save()
        return str(ledgermodel.id)
        
