from datetime import datetime
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
             #end for today


        except Exception as e:
            print(e.args)
            return False            


