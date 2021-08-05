from apis.database_service.Webhook_Request_model_service import Webhook_Request_Model_Service
from datetime import date, datetime
import time
from sabpaisa import auth
import bank_api
from ..database_service import Client_model_service,Ledger_model_services,Mode_model_services,Beneficiary_model_services,Slab_model_services
from ..Utils import splitString
from ..bank_models.IDFC_Model import payment_request_model
from ..bank_models.ICICI_Model import payment_request_model as icic_payment_model
from ..bank_models.ICICI_Model import payment_response_model as icici_response
from ..database_service.Log_model_services import Log_Model_Service
from ..bank_models.PAYTM_Model import payment_request_model as paytm_request_model
from ..bank_models.PAYTM_Model import payment_response_model as paytm_response_model
from ..bank_models.PAYTM_Model import paytm_extra
from ..models import RoleModel,MerchantModel
from ..Utils import statuscodes
from .. import const
from ..Utils import generater
from ..RequestModels.payoutrequestmodel import PayoutRequestModel
import requests
import paytmchecksum 
import threading
import json
from ..database_service.Webhook_model_service import Webhook_Model_Service
from apis import Utils
class PayoutService:
    def __init__(self,merchant_id=None,encrypted_code=None,client_ip_address=None):
        self.merchant_id=merchant_id
        self.client_ip_address = client_ip_address
        self.encrypted_code=encrypted_code
    def excutePAYTM(self,mode_rec):
        log = Log_Model_Service(log_type="excuting PAYTM service",client_ip_address=self.client_ip_address,server_ip_address=const.server_ip,created_by=self.merchant_id)
        log.save()
        try:
            clientModelService = Client_model_service.Client_Model_Service()
            clientModel=clientModelService.fetch_by_id(self.merchant_id,self.client_ip_address,"Merchant_Id ::"+str(self.merchant_id))
            authKey=clientModel.auth_key
            authIV=clientModel.auth_iv
            # auth_token = req.headers["auth_token"]
            # merchant_id= auth.AESCipher(const.AuthKey,const.AuthIV).decrypt(auth_token)
            # merchant=MerchantModel.objects.get(id=self.merchant_id)
            # role = RoleModel.objects.get(id=merchant.role)
            query=self.encrypted_code
            if clientModel.is_encrypt:
             query=auth.AESCipher(authKey,authIV).decrypt(self.encrypted_code)
            map=splitString.StringToMap(query)
            print(str(map))
            map["mode"]=mode_rec
            # if map["usern"]!=clientModel.client_username and map["pass"]!=clientModel.client_password:
            #     return [False,{}]
            payoutrequestmodel,valid,message=PayoutRequestModel.from_json(map)
            # print('upiid :: '+payoutrequestmodel.upiId)
            print("valid :: "+str(valid))
            # print(payoutrequestmodel.clientPaymode)
            mode=Mode_model_services.Mode_Model_Service.fetch_by_mode(payoutrequestmodel.mode)
            if(valid):
             bal = Ledger_model_services.Ledger_Model_Service.getBalance(self.merchant_id,self.client_ip_address,"Merchant_ID :: "+str(self.merchant_id))
             print("amount :: "+payoutrequestmodel.amount)
             print("balance ::"+str(bal))
             log = Log_Model_Service(log_type="Checking for duplicate order id",client_ip_address=self.client_ip_address,server_ip_address=const.server_ip,remarks="checking for duplicate order id for merchant id :: "+ self.merchant_id+" orderid :: "+str(payoutrequestmodel.orderId))
             log.save()
             check_cus=Ledger_model_services.Ledger_Model_Service.fetch_by_customer_ref_no(self.merchant_id,payoutrequestmodel.orderId)
             if check_cus==None:
                 return ["Duplicate Order id",{},False]
             if bal<int(payoutrequestmodel.amount):                 
                 return ["Not Sufficent Balance",{},False]
             if mode_rec=="UPI":
                bene=Beneficiary_model_services.Beneficiary_Model_Services.fetch_by_upiId(self.merchant_id,payoutrequestmodel.upiId)
             else:
                bene=Beneficiary_model_services.Beneficiary_Model_Services.fetch_by_account_number_ifsc(self.merchant_id,payoutrequestmodel.beneficiaryAccount,payoutrequestmodel.beneficiaryIFSC)
             
             if bene==None:
                 return ["Beneficiary Not Added",{},False]
             if not Slab_model_services.Slab_Model_Service.check_slab(self.merchant_id,payoutrequestmodel.amount):
                 return ["Cannot proccess this volume of amount",{},False]
             ledgerModelService = Ledger_model_services.Ledger_Model_Service() 
             clientModelService=Client_model_service.Client_Model_Service()
             clientmodel=clientModelService.fetch_by_id(self.merchant_id,self.client_ip_address,"Merchant Id ::"+str(self.merchant_id))
             ledgerModelService.client_id=clientModel.id
             ledgerModelService.merchant=self.merchant_id
             ledgerModelService.client_code=clientModel.client_code
             ledgerModelService.amount=payoutrequestmodel.amount
             ledgerModelService.bank_id=clientmodel.bank_id
             ledgerModelService.bank_ref_no="null"
             
             ledgerModelService.customer_ref_no=payoutrequestmodel.orderId
             ledgerModelService.trans_status="Initiated"
             if mode_rec!="UPI":
                print("if ledger")
                ledgerModelService.bene_account_name=payoutrequestmodel.beneficiaryName
                ledgerModelService.bene_account_number=payoutrequestmodel.beneficiaryAccount
                ledgerModelService.bene_ifsc=payoutrequestmodel.beneficiaryIFSC
             else:
                 print("else ledger")
                 ledgerModelService.upiId=payoutrequestmodel.upiId
             ledgerModelService.request_header="null"
             ledgerModelService.type_status="Generated"
             ledgerModelService.trans_type="payout"
             
            #  order_id=paytm_extra.generate_order_id()
            #  ledgerModelService.customer_ref_no=order_id
             
             charge=Ledger_model_services.Ledger_Model_Service.calculate_charge(self.merchant_id,mode_rec,payoutrequestmodel.amount,self.client_ip_address)
             print("charges :: "+str(charge))
             if charge==[0,0]:
                 return ["charges not added to this mode",{},False]

             taxes=Ledger_model_services.Ledger_Model_Service.calculate_tax(clientModel.is_tax_inclusive,[ls for ls in charge[1]])
             
             print("charge :: "+str(charge))
             ledgerModelService.charge=taxes[2]
             ledgerModelService.van="null"
             ledgerModelService.status_code=statuscodes.statuscodes["Initiated"]
             ledgerModelService.mode=mode.id
             ledgerModelService.is_tax_inclusive=clientModel.is_tax_inclusive
             ledgerModelService.tax=taxes[0]
             ledgerModelService.payout_trans_id=generater.generate_token()
             ledgerModelService.trans_amount_type = "debited"
             ledgerModelService.trans_time=datetime.now()
             id=ledgerModelService.save(client_ip_address=self.client_ip_address,createdBy="Merchant Id :: "+ str(self.merchant_id))
             ledgerModelService.update_status(id,'Requested',client_ip_address=self.client_ip_address,created_by="Merchant_Id :: "+str(self.merchant_id))
             ledger_id=id
             tax_ledger=Ledger_model_services.Ledger_Model_Service()
             tax_ledger.client_id=clientModel.id
             tax_ledger.merchant=self.merchant_id
             tax_ledger.client_code=clientModel.client_code
             tax_ledger.amount=taxes[0]
             tax_ledger.bank_id=clientmodel.bank_id
             tax_ledger.bank_ref_no="null"
             tax_ledger.customer_ref_no=payoutrequestmodel.orderId
             tax_ledger.trans_status="Pending"
             if mode_rec!="UPI":
                print("if ledger")
                tax_ledger.bene_account_name=payoutrequestmodel.beneficiaryName
                tax_ledger.bene_account_number=payoutrequestmodel.beneficiaryAccount
                tax_ledger.bene_ifsc=payoutrequestmodel.beneficiaryIFSC
             else:
                 print("else ledger")
                 tax_ledger.upiId=payoutrequestmodel.upiId
             tax_ledger.type_status="Generated"
             tax_ledger.trans_type="tax"
             tax_ledger.request_header="null"
             tax_ledger.mode=mode.id
             tax_ledger.van=""
             tax_ledger.charge=0
             tax_ledger.tax=0
             tax_ledger.is_tax_inclusive=ledgerModelService.is_tax_inclusive
             tax_ledger.linked_ledger_id=ledgerModelService.payout_trans_id
             tax_ledger.payout_trans_id=generater.generate_token()
             tax_ledger.trans_amount_type = "debited"
             tax_ledger.charge_id=0
             #  ledgerModelService.
             tax_ledger.trans_time=datetime.now()
             tax_ledger.save("Merchant Id :: "+str(self.merchant_id),self.client_ip_address)
             irt=0
             for i in charge[1]:
                                    print(i)
                                    charge_ledger=Ledger_model_services.Ledger_Model_Service()
                                    charge_ledger.client_id=clientModel.id
                                    charge_ledger.merchant=self.merchant_id
                                    charge_ledger.client_code=clientModel.client_code
                                    charge_ledger.amount=i[0]
                                    charge_ledger.bank_id=clientmodel.bank_id
                                    charge_ledger.bank_ref_no="null"
                                    charge_ledger.customer_ref_no=payoutrequestmodel.orderId
                                    charge_ledger.trans_status="Pending"
                                    if mode_rec!="UPI":
                                        print("if ledger")
                                        charge_ledger.bene_account_name=payoutrequestmodel.beneficiaryName
                                        charge_ledger.bene_account_number=payoutrequestmodel.beneficiaryAccount
                                        charge_ledger.bene_ifsc=payoutrequestmodel.beneficiaryIFSC
                                    else:
                                        print("else ledger")
                                        charge_ledger.upiId=payoutrequestmodel.upiId
                                    charge_ledger.type_status="Generated"
                                    charge_ledger.trans_type="charge"
                                    charge_ledger.request_header="null"
                                    charge_ledger.mode=mode.id
                                    charge_ledger.van=""
                                    charge_ledger.charge=0
                                    charge_ledger.tax=taxes[1][irt][1]
                                    charge_ledger.is_tax_inclusive=ledgerModelService.is_tax_inclusive
                                    charge_ledger.linked_ledger_id=ledgerModelService.payout_trans_id
                                    charge_ledger.payout_trans_id=generater.generate_token()
                                    charge_ledger.trans_amount_type = "debited"
                                    charge_ledger.charge_id=taxes[1][irt][0]
                                    #  ledgerModelService.
                                    charge_ledger.trans_time=datetime.now()
                                    charge_ledger.save("Merchant Id :: "+str(self.merchant_id),self.client_ip_address)
                                    irt+=1
             if mode_rec=="UPI":
                 request_model=paytm_request_model.Payment_Request_Model(transfer_mode=payoutrequestmodel.mode,subwalletGuid=const.paytm_subwalletGuid,orderId=ledgerModelService.payout_trans_id,beneficiaryVPA=payoutrequestmodel.upiId,amount=payoutrequestmodel.amount,purpose=payoutrequestmodel.purpose)
             
             else:
                request_model=paytm_request_model.Payment_Request_Model(beneficiaryName=payoutrequestmodel.beneficiaryName,transfer_mode=payoutrequestmodel.mode,subwalletGuid=const.paytm_subwalletGuid,orderId=ledgerModelService.payout_trans_id,beneficiaryAccount=payoutrequestmodel.beneficiaryAccount,beneficiaryIFSC=payoutrequestmodel.beneficiaryIFSC,amount=payoutrequestmodel.amount,purpose=payoutrequestmodel.purpose)
             
             log_model=Log_Model_Service(log_type="Paytm_Request",server_ip_address=const.server_ip,client_ip_address=self.client_ip_address,full_request=str(request_model.to_json()))
             log_id=log_model.save()
             post_data = json.dumps(request_model.to_json())
             checksum = paytmchecksum.generateSignature(post_data, const.paytm_merchant_key)
             
             response = requests.post(bank_api.paytm.staging_paytmPaymentAPI(),json=request_model.to_json(),headers={"Content-type": "application/json", "x-mid": const.paytm_merchant_id, "x-checksum":checksum})
             print(response.json())
             Log_Model_Service.update_response(log_id,response=str(response.json()))
             response_model = paytm_response_model.Payment_Response_Model.from_json(response.json())
             client_ip_address_temp=self.client_ip_address
             merchant_id_temp = self.merchant_id
             class ServiceThread2(threading.Thread):
                    def run(self):
                        log = Log_Model_Service(log_type="Thread",client_ip_address=client_ip_address_temp,server_ip_address=const.server_ip,remarks="Running service thread on webhook apis for merchant id :: "+ merchant_id_temp)
                        log.save()
                        transhistory=Ledger_model_services.Ledger_Model_Service.fetch_by_id(id=ledger_id,client_ip_address=client_ip_address_temp,created_by="system")
                        
                        webhookrequest=Webhook_Request_Model_Service()
                        webhookrequest.payout_trans_id=transhistory.payout_trans_id
                        webhookrequest.hit_init_time=datetime.now()
                        webhookrequest.status=False
                        id=webhookrequest.save()
                        
                        webhooks = Webhook_Model_Service.fetch_by_merchant_id(merchant_id_temp,client_ip_address_temp)
                        print("Webhook Started at :: "+webhooks.webhook)
                        if not webhooks.is_instant:
                            print("Interval Webhook :: "+str(webhooks.time_interval)+" min ")
                            interval=webhooks.time_interval
                            time.sleep(60*interval)
                        if webhooks==None:
                            pass
                        else:
                            
                            transhistoryJson=Ledger_model_services.Ledger_Model_Service.fetch_by_id_tojson(id=ledger_id,client_ip_address=client_ip_address_temp,created_by="system")
                            response=requests.post(webhooks.webhook,json=transhistoryJson)
                            print("First Response from webhook :: "+str(response.json()))
                            if response.status_code!=200:
                                for i in range(webhooks.max_request):
                                    
                                    response=requests.post(webhooks.webhook,json=transhistoryJson)
                                    print(str(i)+"th response from webhook :: "+response.text)
                                    if response.status_code==200:
                                        break
                            if response.status_code==200:
                                print("updating response as true")
                                Webhook_Request_Model_Service.update_webhook(id,True,response.text) 
                            else:
                                print("updating response as false")
                                Webhook_Request_Model_Service.update_webhook(id,False,response.text)                       

             if(response_model.status=="ACCEPTED"):
                ledgerModelService.update_status(id,"Proccesing",client_ip_address=self.client_ip_address,created_by="Merchant ID :: "+str(self.merchant_id))
                client_ip_address_temp=self.client_ip_address
                merchant_id_temp = self.merchant_id
                thread = None   
                class ServiceThread(threading.Thread):
                     def run(self):
                         log = Log_Model_Service(log_type="Thread",full_request={"orderId":payoutrequestmodel.orderId},client_ip_address=client_ip_address_temp,server_ip_address=const.server_ip,remarks="Running service thread on paytm enquiry api for merchant id :: "+ merchant_id_temp)
                         logid=log.save()
                         time.sleep(40)
                         checksum=paytmchecksum.generateSignature(json.dumps({"orderId":payoutrequestmodel.orderId}), const.paytm_merchant_key)
                         response = requests.post(bank_api.paytm.staging_paytmEnquiryAPI(),json={"orderId":payoutrequestmodel.orderId},headers={"Content-type": "application/json", "x-mid": const.paytm_merchant_id, "x-checksum":checksum})
                         log.update_response(logid,response.text)
                         print(response.json())
                         if response.json()['status']=="SUCCESS":
                             ledgerModelService.update_status(id,"Success",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                             ledgerModelService.update_trans_time(id,datetime.now(),client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                             charge = Ledger_model_services.Ledger_Model_Service.fetch_by_linked_id(ledgerModelService.payout_trans_id)
                             if clientModel.is_charge:
                                
                                for i in charge:
                                    ledgerModelService.update_status(i.id,"Success",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                             else:
                                 for i in charge:
                                    ledgerModelService.update_status(i.id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                                
                         elif response.json()["status"]=="PENDING":
                             ledgerModelService.update_status(id,"Pending",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                             
                             ServiceThread().start()
                         else:
                             charge = Ledger_model_services.Ledger_Model_Service.fetch_by_linked_id(ledgerModelService.payout_trans_id)
                             for i in charge:
                                    ledgerModelService.update_status(i.id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                             
                             ledgerModelService.update_status(id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                         print("Service Done")
                
                
                thread=ServiceThread().start()
                
                
             else:
                 charge = Ledger_model_services.Ledger_Model_Service.fetch_by_linked_id(ledgerModelService.payout_trans_id)
                 for i in charge:
                                    ledgerModelService.update_status(i.id,"Failed",client_ip_address_temp,"Merchant :: "+str(merchant_id_temp))
                             
                 ledgerModelService.update_status(id,"Failed",self.client_ip_address,"Merchant :: "+str(self.merchant_id))
             thread2 = ServiceThread2().start()           
                 
             return ["Payout Done",{"orderId":ledgerModelService.customer_ref_no,"amount":ledgerModelService.amount,"status": "PROCESSING","requestedDatetime": str(datetime.now()).split(".")[0]},True]
             
            else:
             return [message,{},False]
        except Exception as e:
              import traceback
              print(traceback.format_exc())
              print(e.args)
              return [e.args,{},False]
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