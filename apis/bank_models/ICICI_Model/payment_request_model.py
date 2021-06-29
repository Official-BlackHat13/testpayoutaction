# HttpURLConnection con = (HttpURLConnection) object.openConnection();
# 		con.setDoOutput(true);
# 		con.setDoInput(true);
# 		con.setRequestProperty("Content-Type", "application/json");
# 		con.setRequestProperty("Accept", "application/json");
# 		con.setRequestMethod("POST");
# 		con.setRequestProperty("Username", userName.trim());
# 		log.info("Username::" + userName);

# 		String pass = ENCRYPTION.encryptInstaPaymnentData(PassWord.trim(), key);

# 		con.setRequestProperty("Password", pass.trim());
# 		log.info("Password:::" + PassWord);

# 		log.info("passsss::" + pass);
# 		log.info("conn::" + con.getRequestProperty("Password"));

# 		JSONObject mainObject = new JSONObject(); // Host object
# 		JSONObject requestObject = new JSONObject(); // Included object

# 		try {

# 			requestObject.put("IFSCCode", IFSCCode);
# 			log.info("IFSCCode:" + IFSCCode);
# 			requestObject.put("remiMobileNumber", RemiMobileNumber);
# 			log.info("RemiMobileNumber:" + RemiMobileNumber);
# 			requestObject.put("remarks", "test");

# 			mainObject.put("AdditionalDetails", requestObject);

# 			mainObject.put("customerID", CustomerID.trim());
# 			log.info("CustomerID:" + CustomerID);
# 			mainObject.put("customerReferenceNumber", CustomerReferenceNumber.trim());
# 			log.info("CustomerReferenceNumber:" + CustomerReferenceNumber);
# 			mainObject.put("debitAccountNumber", ENCRYPTION.encryptInstaPaymnentData(DebitAccountNumber.trim(), key));
# 			log.info("DebitAccountNumber:" + DebitAccountNumber);
# 			mainObject.put("creditAccountNumber", ENCRYPTION.encryptInstaPaymnentData(CreditAccountNumber.trim(), key));
# 			log.info("CreditAccountNumber:" + CreditAccountNumber);
# 			mainObject.put("transactionAmount", ENCRYPTION.encryptInstaPaymnentData(TransactionAmount.trim(), key));

# 		} catch (JSONException e) {
# 			log.info(e);
# 		}
# class 

from bank_api import run_java,icici
class Header_Request:
    def __init__(self,Username="",Password=""):
        self.Username=Username
        self.Password=Password
    def to_Json(self):
        return {
            "Username":self.Username,
            "Password":run_java.runJavaCode(self.Password.strip(),icici.key())
        }


class Body_Request:
    def __init__(self,IFSCCode="",remiMobileNumber="",remarks="",customerID="",customerReferenceNumber="",debitAccountNumber="",creditAccountNumber="",transactionAmount=""):
        self.IFSCCode=IFSCCode
        self.remiMobileNumber=remiMobileNumber
        self.remarks=remarks
        self.customerID=customerID
        self.customerReferenceNumber=customerReferenceNumber
        self.debitAccountNumber=debitAccountNumber
        self.creditAccountNumber=creditAccountNumber
        self.transactionAmount=transactionAmount
    def to_json(self):
        return {
            "AdditionalDetails":{
                "IFSCCode":self.IFSCCode,
                "remiMobileNumber":self.remiMobileNumber,
                "remarks":self.remarks
            },
            "customerID":self.customerID,
            "customerReferenceNumber":self.customerReferenceNumber,
            "debitAccountNumber":run_java.runJavaCode(self.debitAccountNumber.strip(),icici.key()),
            "creditAccountNumber":run_java.runJavaCode(self.creditAccountNumber.strip(),icici.key()),
            "transactionAmount":run_java.runJavaCode(self.transactionAmount.strip(),icici.key())
        }

