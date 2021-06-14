from datetime import date, datetime
from sabpaisa import auth
from ..database_service import Client_model_service,Ledger_model_services
from ..Utils import splitString
from ..bank_models.IDFC_Request_Model import payment_request_model
from ..RequestModels.payoutrequestmodel import PayoutRequestModel

class PayoutService:
    def __init__(self,client_code,encrypted_code):
        self.client_code=client_code
        self.encrypted_code=encrypted_code
    def excute(self):
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
             #end for today


        except Exception as e:
            print(e.args)
            return False            


