from datetime import date, datetime
import time
from sabpaisa import auth

import bank_api
from ..database_service import Client_model_service,Ledger_model_services
from ..Utils import splitString
from ..bank_models.IDFC_Model import payment_request_model
from ..bank_models.ICICI_Model import payment_request_model as icic_payment_model
from ..bank_models.ICICI_Model import payment_response_model as icici_response
from ..database_service.Log_model_services import Log_Model_Service
from ..bank_models.PAYTM_Model import payment_request_model as paytm_request_model
from ..bank_models.PAYTM_Model import payment_response_model as paytm_response_model
from ..bank_models.PAYTM_Model import paytm_extra
from .. import const

from ..RequestModels.payoutrequestmodel import PayoutRequestModel
import requests
import paytmchecksum 
import threading
import json
class PayoutService:
    def __init__(self,merchant_id=None,encrypted_code=None,client_ip_address=None):
        self.merchant_id=merchant_id
        self.client_ip_address = client_ip_address
        self.encrypted_code=encrypted_code
    def excutePAYTM(self):
        log = Log_Model_Service(log_type="excuting PAYTM service",client_ip_address=self.client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            clientModel=clientModelService.fetch_by_id(self.merchant_id)
            authKey=clientModel.auth_key
            authIV=clientModel.auth_iv
            query=auth.AESCipher(authKey,authIV).decrypt(self.encrypted_code)
            map=splitString.StringToMap(query)
            if map["usern"]!=clientModel.client_username and map["pass"]!=clientModel.client_password:
                return False
            payoutrequestmodel,valid,message=PayoutRequestModel.from_json(map)
            
            if(valid):
             bal = Ledger_model_services.Ledger_Model_Service.getBalance(self.merchant_id)
             if bal<payoutrequestmodel.txnAmount:
                 return "Not Sufficent Balance"
             ledgerModelService = Ledger_model_services.Ledger_Model_Service() 
             clientModelService=Client_model_service.Client_Model_Service()
             clientmodel=clientModelService.fetch_by_id(self.merchant_id)
             ledgerModelService.client_id=clientModel.id
             ledgerModelService.client_code=clientModel.client_code
             ledgerModelService.amount=payoutrequestmodel.txnAmount
             ledgerModelService.bank_id=clientmodel.bank
             ledgerModelService.bank_ref_no="waiting"
             ledgerModelService.customer_ref_no=payoutrequestmodel.clientTransactionId
             ledgerModelService.status="initated"
             ledgerModelService.bene_account_name=payoutrequestmodel.accountHolderName
             ledgerModelService.bene_account_number=payoutrequestmodel.creditAccountNumber
             ledgerModelService.bene_ifsc=payoutrequestmodel.ifscCode
             ledgerModelService.type_status="Generated"
             ledgerModelService.trans_type=payoutrequestmodel.clientPaymode
             ledgerModelService.van=payoutrequestmodel.van
             ledgerModelService.trans_amount_type = "debited"
             ledgerModelService.trans_time=datetime.now()
             id=ledgerModelService.save(client_ip_address=self.client_ip_address)
             ledgerModelService.update_status(id,'Requested')
             order_id=paytm_extra.generate_order_id()
             request_model=paytm_request_model.Payment_Request_Model(subwalletGuid=const.paytm_subwalletGuid,orderId=order_id,beneficiaryAccount=payoutrequestmodel.creditAccountNumber,beneficiaryIFSC=payoutrequestmodel.ifscCode,amount=payoutrequestmodel.txnAmount,purpose=paytm_extra.purpose_list[0])
             post_data = json.dumps(request_model.to_json())
             checksum = paytmchecksum.generateSignature(post_data, const.paytm_merchant_key)
             
             response = requests.post(bank_api.paytm.staging_paytmPaymentAPI(),json=request_model.to_json(),headers={"Content-type": "application/json", "x-mid": const.paytm_merchant_id, "x-checksum":checksum})

             response_model = paytm_response_model.Payment_Response_Model.from_json(response.json())
             if(response_model.status=="ACCEPTED"):
                 ledgerModelService.update_status(id,"Proccesing")
                 class ServiceThread(threading.Thread):
                     def run(self):
                         time.sleep(20)
                         checksum=paytmchecksum.generateSignature(json.dumps({"orderId":order_id}), const.paytm_merchant_key)
                         response = requests.post(bank_api.paytm.staging_paytmEnquiryAPI(),json={"orderId":order_id},headers={"Content-type": "application/json", "x-mid": const.paytm_merchant_id, "x-checksum":checksum})
                         if response.json()['status']=="SUCCESS":
                             ledgerModelService.update_status(id,"Success")
                         else:
                             ledgerModelService.update_status(id,"Failed")
                         print("Service Done")
             return "Payout Done"
            else:
             return message
        except Exception as e:
              return e.args
    def excuteICICI(self):
        log = Log_Model_Service(log_type="excuting ICICI service",client_ip_address=self.client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            clientModel=clientModelService.fetch_by_clientcode(self.client_code)
            authKey=clientModel.auth_key
            authIV=clientModel.auth_iv
            query=auth.AESCipher(authKey,authIV).decrypt(self.encrypted_code)
            map=splitString.StringToMap(query)
            if map["usern"]!=clientModel.client_username and map["pass"]!=clientModel.client_password:
                return False
            payoutrequestmodel,valid,message=PayoutRequestModel.from_json(map)
            if(valid):
             bal = Ledger_model_services.Ledger_Model_Service.getBalance(self.client_code)
             if bal<payoutrequestmodel.txnAmount:
                 return "Not Sufficent Balance"
             ledgerModelService = Ledger_model_services.Ledger_Model_Service() 
             clientModelService=Client_model_service.Client_Model_Service()
             clientmodel=clientModelService.fetch_by_clientcode(self.client_code)
             ledgerModelService.client_id=clientModel.client
             ledgerModelService.client_code=self.client_code
             ledgerModelService.amount=payoutrequestmodel.txnAmount
             ledgerModelService.bank_id=clientmodel.bank
             ledgerModelService.bank_ref_no="waiting"
             ledgerModelService.customer_ref_no=payoutrequestmodel.clientTransactionId
             ledgerModelService.status="initated"
             ledgerModelService.bene_account_name=payoutrequestmodel.accountHolderName
             ledgerModelService.bene_account_number=payoutrequestmodel.creditAccountNumber
             ledgerModelService.bene_ifsc=payoutrequestmodel.ifscCode
             ledgerModelService.type_status="Generated"
             ledgerModelService.trans_type=payoutrequestmodel.clientPaymode
             ledgerModelService.van=payoutrequestmodel.van
             ledgerModelService.trans_amount_type = "debited"
             ledgerModelService.trans_time=datetime.now()
             id=ledgerModelService.save(client_ip_address=self.client_ip_address)
             header = icic_payment_model.Header_Request(Username=bank_api.icici.icic_details()["iciciImpsUserName"],Password=bank_api.icici.icic_details()["Password"])
             body = icic_payment_model.Body_Request(IFSCCode=payoutrequestmodel.ifscCode,remiMobileNumber=payoutrequestmodel.payeeMob,remarks="payment",customerID=bank_api.icici.icic_details()["iciciImpsUserName"],customerReferenceNumber=payoutrequestmodel.clientTransactionId,debitAccountNumber=bank_api.icici.icic_details()["debitAccount"],creditAccountNumber=payoutrequestmodel.creditAccountNumber,transactionAmount=payoutrequestmodel.txnAmount)
             response = requests.post(headers=header.to_Json(),json=body.to_json())
             response_obj = icici_response.Response_Model.from_json(json=response.json())
             if(response_obj.status=="Success"):
                 ledgerModelService.update_status(id,'Success')
             else:
                  ledgerModelService.update_status(id,'Failed')
             return "Payout Done"
            else:
             return message
        except Exception as e:
            return e.args
    def excutePAYTM(self):
        log=Log_Model_Service(log_type="excuting PAYTM service",client_ip_address=self.client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            clientModel=clientModelService.fetch_by_clientcode(self.client_code)
            authKey=clientModel.auth_key
            authIV=clientModel.auth_iv
            query=auth.AESCipher(authKey,authIV).decrypt(self.encrypted_code)
            map=splitString.StringToMap(query)
            if map["usern"]!=clientModel.client_username and map["pass"]!=clientModel.client_password:
                return False
            payoutrequestmodel,valid,message=PayoutRequestModel.from_json(map)
            if(valid):
             bal = Ledger_model_services.Ledger_Model_Service.getBalance(self.client_code)
             if bal<payoutrequestmodel.txnAmount:
                 return "Not Sufficent Balance"
             ledgerModelService = Ledger_model_services.Ledger_Model_Service() 
             clientModelService=Client_model_service.Client_Model_Service()
             clientmodel=clientModelService.fetch_by_clientcode(self.client_code)
             ledgerModelService.client_id=clientModel.client
             ledgerModelService.client_code=self.client_code
             ledgerModelService.amount=payoutrequestmodel.txnAmount
             ledgerModelService.bank_id=clientmodel.bank
             ledgerModelService.bank_ref_no="waiting"
             ledgerModelService.customer_ref_no=payoutrequestmodel.clientTransactionId
             ledgerModelService.status="initated"
             ledgerModelService.bene_account_name=payoutrequestmodel.accountHolderName
             ledgerModelService.bene_account_number=payoutrequestmodel.creditAccountNumber
             ledgerModelService.bene_ifsc=payoutrequestmodel.ifscCode
             ledgerModelService.type_status="Generated"
             ledgerModelService.trans_type=payoutrequestmodel.clientPaymode
             ledgerModelService.van=payoutrequestmodel.van
             ledgerModelService.trans_amount_type = "debited"
             ledgerModelService.trans_time=datetime.now()
             id=ledgerModelService.save(client_ip_address=self.client_ip_address)
             response_obj={}
             if(response_obj.status=="Success"):
                 ledgerModelService.update_status(id,'Success')
             else:
                  ledgerModelService.update_status(id,'Failed')
             return "Payout Done"
            else:
             return message
        except:
            pass
    
    def excuteIDFC(self):
        log = Log_Model_Service(log_type="excuting IDFC service",client_ip_address=self.client_ip_address,server_ip_address=const.server_ip,created_by=self.client_code)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            clientModel=clientModelService.fetch_by_clientcode(self.client_code)
            authKey=clientModel.auth_key
            authIV=clientModel.auth_iv
            query=auth.AESCipher(authKey,authIV).decrypt(self.encrypted_code)
            map=splitString.StringToMap(query)
            if map["usern"]!=clientModel.client_username and map["pass"]!=clientModel.client_password:
                return False
            payoutrequestmodel,valid,message=PayoutRequestModel.from_json(map)
            if(valid):
             ledgerModelService = Ledger_model_services.Ledger_Model_Service() 
             clientModelService=Client_model_service.Client_Model_Service()
             clientmodel=clientModelService.fetch_by_clientcode(self.client_code)
             ledgerModelService.client_id=clientModel.client
             ledgerModelService.client_code=self.client_code
             ledgerModelService.amount=payoutrequestmodel.txnAmount
             ledgerModelService.bank_id=clientmodel.bank
             ledgerModelService.bank_ref_no="waiting"
             ledgerModelService.customer_ref_no=payoutrequestmodel.clientTransactionId
             ledgerModelService.status="initated"
             ledgerModelService.bene_account_name=payoutrequestmodel.accountHolderName
             ledgerModelService.bene_account_number=payoutrequestmodel.creditAccountNumber
             ledgerModelService.bene_ifsc=payoutrequestmodel.ifscCode
             ledgerModelService.type_status="Generated"
             ledgerModelService.trans_type=payoutrequestmodel.clientPaymode
             ledgerModelService.van=payoutrequestmodel.van
             ledgerModelService.trans_time=datetime.now()
             id=ledgerModelService.save()
             message_header=payment_request_model.Message_Header()
             message_header.cnvId=payoutrequestmodel.clientTransactionId
             message_header.msgId=str(id)
             message_body=payment_request_model.Message_Body()
             message_body.beneAccNo=payoutrequestmodel.creditAccountNumber
             message_body.beneMail=payoutrequestmodel.payeeEmail
             message_body.beneMobile=payoutrequestmodel.payeeMob
             message_body.beneName=payoutrequestmodel.accountHolderName
             message_body.clientCode=self.client_code
             message_body.cusTxnRef=payoutrequestmodel.clientTransactionId
             message_body.paymentType=payoutrequestmodel.clientPaymode
             message_body.beneAddr1=""
             message_body.beneAddr2=""
             message_body.valueDate=date.today()
             message_body.tranCcy="inr"
             message_body.tranAmount=payoutrequestmodel.txnAmount
             message_body.ifsc=payoutrequestmodel.ifscCode
             message_body.beneAccType="current"
             

        except Exception as e:
            print(e.args)
            return False            


