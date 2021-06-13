class PayoutRequestModel:
    def __init__(self,userName=None,password=None,payeeFirstName=None,payeeLastName=None,payeeMob=None,payeeEmail=None,txnAmount=None,returnUrl=None,creditAccountNumber=None,ifscCode=None,bankBranch=None,accountHolderName=None,clientTransactionId=None,udf1=None,udf2=None,udf3=None,udf4=None,udf5=None,udf6=None,udf7=None,udf8=None,udf9=None,udf10=None,van=None,clientPaymode=None,environment=None):
        self.userName=userName
        self.password=password
        self.payeeFirstName=payeeFirstName
        self.payeeLastName=payeeLastName
        self.payeeMob=payeeMob
        self.payeeEmail=payeeEmail
        self.txnAmount=txnAmount
        self.returnUrl=returnUrl
        self.creditAccountNumber=creditAccountNumber
        self.ifscCode=ifscCode
        self.bankBranch=bankBranch
        self.accountHolderName=accountHolderName
        self.clientTransactionId=clientTransactionId
        self.udf1=udf1
        self.udf2=udf2
        self.udf3=udf3
        self.udf4=udf4
        self.udf5=udf5
        self.udf6=udf6
        self.udf7=udf7
        self.udf8=udf8
        self.udf9=udf9
        self.udf10=udf10
        self.van=van
        self.clientPaymode=clientPaymode
        self.environment=environment
    @staticmethod
    def from_json(json):
        requestModel=PayoutRequestModel()
        try:
            if json['userName']=="":
             return [None,False,"Username is missing"]
            else:
             requestModel.userName=json["userName"]
            if json['password']=="":
                return [None,False,"Password is missing"]
            else:
             requestModel.password=json["password"]
            if json["payeeFirstName"]=="":
                return [None,False,"Payee First Name is missing"]
            else:
             requestModel.payeeFirstName=json["payeeFirstName"]
            if json['payeeLastName']=="":
                return [None,False,"Payee Last Name is missing"]
            else:
             requestModel.payeeLastName=json["payeeLastName"]
            if json["payeeMob"]=="":
                return [None,False,"Payee Mobile Number is missing"]
            else:
              requestModel.payeeMob=json["payeeMob"]
            if json['payeeEmail']=="":
             return [None,False,"Payee Email is missing"]
            else:
                requestModel.payeeEmail=json["payeeEmail"]
            if json['txnAmount']=="":
                return [None,False,"Transaction amount is missing"]
            else:
             requestModel.txnAmount=json["txnAmount"]
            if json['returnUrl']=="":
                return [None,False,"Return Url is missing"]
            else:
             requestModel.returnUrl=json["returnUrl"]
            if json["creditAccountNumber"]=="":
                return [None,False,"Credit Account Number is missing"]
            else:
             requestModel.creditAccountNumber=json["creditAccountNumber"]
            if json['ifscCode']=="":
                 return [None,False,"IFSC is missing"]
            else:
             requestModel.ifscCode=json["ifscCode"]
            if json['bankBranch']=="":
                return [None,False,"Bank Branch is missing"]
            else:
             requestModel.bankBranch=json["bankBranch"]
            if json['accountHolderName']=="":
                return [None,False,"Account Holder Name is missing"]
            else:
             requestModel.accountHolderName=json["accountHolderName"]
            if json['clientTransactionId']=="":
                return [None,False,"Client Transaction Id is missing"]
            else:
             requestModel.clientTransactionId=json["clientTransactionId"]
            if "udf1" in json:
             requestModel.udf1=json["udf1"]
            else:
                requestModel.udf1=""
            if "udf2" in json:

             requestModel.udf2=json["udf2"]
            else:
                requestModel.udf2=""
            if "udf3" in json:
             requestModel.udf3=json["udf3"]
            else:
                requestModel.udf3=""
            if "udf4" in json:
             requestModel.udf4=json["udf4"]
            else:
                requestModel.udf4=""
            if "udf5" in json:
             requestModel.udf5=json["udf5"]
            else:
                requestModel.usd6=""
            if "udf6" in json:
             requestModel.udf6=json["udf6"]
            else:
                requestModel.udf6=""
            if "udf7" in json:
             requestModel.udf7=json["udf7"]
            else:
                requestModel.udf7=""
            if "udf8" in json:
             requestModel.udf8=json["udf8"]
            else:
                requestModel.udf8=""
            if "udf9" in json:
             requestModel.udf9=json["udf9"]
            else:
                requestModel.udf9=""
            if "udf10" in json:
             requestModel.udf10=json["udf10"]
            else:
                requestModel.udf10=""
            if "van" in json:
             requestModel.van=json["van"]
            else:
                requestModel.van=""
            if "clientPaymode" in json:
                 
             requestModel.clientPaymode=json['clientPaymode']
            else:
                requestModel.clientPaymode=""
            if "environment" in json:
             requestModel.environment=json["environment"]
            else:
                requestModel.clientPaymode=""
            return [requestModel,True,"Fine"]
        except Exception as e:
            print(e.args)
            return [e,False,"Exception Raised"]
    @staticmethod
    def to_json(payoutrequestmodel):
        json={}
        json['userName']=payoutrequestmodel.userName
        json['password']=payoutrequestmodel.password
        json['payeeFirstName']=payoutrequestmodel.payeeFirstName
        json['payeeLastName']=payoutrequestmodel.payeeLastName
        json['payeeMob']=payoutrequestmodel.payeeMob
        json['payeeEmail']=payoutrequestmodel.payeeEmail
        json['txnAmount']=payoutrequestmodel.txnAmount
        json['returnUrl']=payoutrequestmodel.returnUrl
        json['creditAccountNumber']=payoutrequestmodel.creditAccountNumber
        json['ifscCode']=payoutrequestmodel.ifscCode
        json['bankBranch']=payoutrequestmodel.bankBranch
        json['accountHolderName']=payoutrequestmodel.accountHolderName
        json['clientTransactionId']=payoutrequestmodel.clientTransactionId
        json['udf1']=payoutrequestmodel.udf1
        json['udf2']=payoutrequestmodel.udf2
        json['udf3']=payoutrequestmodel.udf3
        json['udf4']=payoutrequestmodel.udf4
        json['udf5']=payoutrequestmodel.udf5
        json['udf6']=payoutrequestmodel.udf6
        json['udf7']=payoutrequestmodel.udf7
        json['udf8']=payoutrequestmodel.udf8
        json['udf9']=payoutrequestmodel.udf9
        json['udf10']=payoutrequestmodel.udf10
        json['van']=payoutrequestmodel.van
        json['clientPaymode']=payoutrequestmodel.clientPaymode
        json['environment']=payoutrequestmodel.environment
        return json

















        










