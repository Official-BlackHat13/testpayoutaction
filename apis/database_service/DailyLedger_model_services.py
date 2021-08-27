from ..database_models.DailyLedgerModel import DailyLedgerModel
from django.db import connection
class DailyLedger_Model_Service:
    @staticmethod
    def fetch_by_date_and_merchant_id(merchant_id,date):
        dailyledger=DailyLedgerModel.objects.filter(merchant_id=merchant_id,date=date)
        if len(dailyledger)==0:
            return None
        return dailyledger
    @staticmethod
    def fetch(page,length,merchant_id,start,end):
        merchant_id_temp=merchant_id
        start_temp=start
        if merchant_id=="all":
            merchant_id_temp="merchant_id"
        if start=="all" and end!="all" or start!="all" and end!="all":
            raise Exception("date time is not in format")
        if start=="all":
           

            dailyledger=DailyLedgerModel.objects.raw("select * from apis_dailyledgermodel inner join apis_merchantmodel on  apis_dailyledgermodel.merchant_id=apis_merchantmodel.id where date=DATE_SUB(CURDATE(), INTERVAL 1 DAY) and apis_dailyledgermodel.merchant_id="+merchant_id_temp+" limit "+str((page-1)*length)+","+str(length)+"")
        else:
            dailyledger=DailyLedgerModel.objects.raw("select * from apis_dailyledgermodel inner join apis_merchantmodel on  apis_dailyledgermodel.merchant_id=apis_merchantmodel.id where date=DATE_SUB(CURDATE(), INTERVAL 1 DAY) and apis_dailyledgermodel.merchant_id="+merchant_id_temp+" date between '"+str(start)+"' and '"+str(end)+"' limit "+str((page-1)*length)+","+str(length)+"")
        def mapit(vals):
            temp_c=vals.today_charges
            temp_credit=vals.closing_credit
            temp_balance=vals.closing_balance
            if vals.today_charges==None:
                temp_c=0
            if vals.closing_credit==None:
                temp_credit=0
            if vals.closing_balance==None:
                temp_balance=0
            return {"date":vals.date,"merchant_id":vals.merchant_id,"client_username":vals.client_username,"credit_amount":vals.closing_credit,"bank_charges":temp_c,"total_credit":temp_credit-temp_c,"balance":temp_balance}
        return list(map(mapit,dailyledger))
        # if len(dailyledger)==0:
        #     return None
        # return dailyledger
    @staticmethod
    def callDailyLedger():
        cursors = connection.cursor()
        cursors.execute("call getDailyBalance()")
        return True