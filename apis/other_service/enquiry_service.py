from apis import const
from http import client
import json
import math
import re
from rest_framework import status
from sabpaisa import auth
from datetime import datetime
from apis.database_service import Log_model_services
from ..database_service import Client_model_service
from rest_framework.permissions import AND
from ..models import LedgerModel
from django.db import connection

class ICICI_service:
    def fetch_by_van(self,van):
        ledgerModels=LedgerModel.objects.filter(van=van)
        return ledgerModels
    def deleteLedger(self, id):
        LedgerModel.objects.filter(id=id).delete()
        return True
    def getBalance(self,clientCode):
        cursors = connection.cursor()
        cursors.execute("getBalance("+clientCode+",@balance)")
        cursors.execute("select @balance")
        value = cursors.fetchall()
        cursors.close()
        return value

    def fetchAll(clientCode,createdBy,ip):
        clientModel = Client_model_service.Client_Model_Service.fetch_by_clientcode(client_ip_address=ip, client_code=clientCode, created_by=createdBy)
        authKey=clientModel.auth_key
        authIV=clientModel.auth_iv
        ledgerModel = LedgerModel.objects.filter(status=True)
        if(len(ledgerModel) == 0):
            return "0"
        resp = str(list(ledgerModel.values()))
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp

    def deleteById(id, deletedBy):
        ledger = LedgerModel.objects.filter(id=id)
        print("service ledger = ", ledger)
        if(len(ledger) > 0):
            ledgermodel = LedgerModel()
            ledgerModel = ledger[0]
            print("service     ", ledgerModel)
            ledgerModel.status = False
            ledgerModel.deletedBy = deletedBy
            ledgerModel.deleted_at = datetime.now()
            ledgerModel.save()
            return True
        return False
     
    def findByTransTimeService(startTranstime, endTransTime, merchant, created_by, client_ip_address):
        startYear = int(startTranstime[0:4])
        startMonth = int(startTranstime[5:7])
        startDay = int(startTranstime[8:10])
        startHours = int(startTranstime[11:13])
        startMinute = int(startTranstime[14:16])

        endYear = int(endTransTime[0:4])
        endMonth = int(endTransTime[5:7])
        endDay = int(endTransTime[8:10])
        endHours = int(endTransTime[11:13])
        endMinute = int(endTransTime[14:16])

        dt = datetime.now()
        start = dt.replace(year=startYear, day=startDay, month=startMonth, hour=startHours, minute=startMinute, second=0, microsecond=0)
        end = dt.replace(year=endYear, day=endDay, month=endMonth,hour=endHours, minute=endMinute, second=0, microsecond=0)
        Ledger = LedgerModel.objects.filter(trans_time__range=[start, end])

        clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=created_by, client_ip_address=client_ip_address)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        if(len(Ledger) == 0):
                return "0"
        resp = str(list(Ledger.values()))
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp

    
    def fetchLedgerByParams(merchant, created_by, page,length,client_ip_address, client_code=None, customer_ref_no=None, startTime=None, endTime=None, trans_type=None):
        print("fect.................")
        log_service = Log_model_services.Log_Model_Service(log_type="fetch", table_name="apis_ledgermodel", remarks="fetching records in apis_ledgermodel table",
                                                           client_ip_address=client_ip_address, server_ip_address=const.server_ip, created_by=created_by)
        log_service.save()
        print("fect.................")
        resp = list()
        query = str()
        if(merchant==None):
            return "-1"
        elif(client_code != None and merchant != None and customer_ref_no!=None and trans_type != None):
            resp = LedgerModel.objects.filter(merchant=merchant,client_code=client_code,customer_ref_no=customer_ref_no,trans_type=trans_type).values()
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=created_by, client_ip_address=client_ip_address)
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            #start
            if(len(resp) == 0):
                return "0"
            if(length == "all"):
                return str(resp)
            if(int(length) > len(resp)):
                return "-2"

            if(int(length)>=len(resp) and int(page)>1):
                return "-2"
            length = int(length)
            splitlen = math.ceil(len(resp)/length)
            split_list = []
            for i in range(splitlen):
                split_list.append(resp[length*i:length*(i+1)])
            json = {
                "data": str(split_list[int(page)-1]),
                "splitlen": str(splitlen)
            }
            respJson = str(json)
            # print("response..... ", respJson)
            #return split_list[int(page)-1]
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchant, created_by=created_by,client_ip_address=client_ip_address)
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            string = str(resp)
            encResp = auth.AESCipher(authKey, authIV).encrypt(respJson)
            return respJson
            #end
        elif(client_code != None and merchant != None):
            query = "call fet(\""+client_code+"\","+merchant+");"
        elif(customer_ref_no != None and merchant != None):
            query = "call fet(\""+customer_ref_no+"\","+merchant+");"
        elif(trans_type != None and merchant != None):
            query = "call fet(\""+trans_type+"\","+merchant+");"
        elif(merchant!=None):
            resp = LedgerModel.objects.filter(merchant=merchant).values()
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
            id=merchant, created_by=created_by, client_ip_address=client_ip_address)
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            #start
            if(len(resp) == 0):
                return "0"
            if(length == "all"):
                return str(resp)
            if(int(length) > len(resp)):
                return "-2"

            if(int(length)>=len(resp) and int(page)>1):
                return "-2"
            length = int(length)
            splitlen = math.ceil(len(resp)/length)
            split_list = []
            for i in range(splitlen):
                split_list.append(resp[length*i:length*(i+1)])
            json = {
                "data": str(split_list[int(page)-1]),
                "splitlen": str(splitlen)
            }
            respJson = str(json)
            # print("response..... ", respJson)
            #return split_list[int(page)-1]
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchant, created_by=created_by,client_ip_address=client_ip_address)
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            string = str(resp)
            encResp = auth.AESCipher(authKey, authIV).encrypt(respJson)
            return respJson
            #end
        elif(startTime!=None and endTime!=None  and merchant!=None):
            startYear = int(startTime[0:4])
            startMonth = int(startTime[5:7])
            startDay = int(startTime[8:10])
            startHours = int(startTime[11:13])
            startMinute = int(startTime[14:16])

            endYear = int(endTime[0:4])
            endMonth = int(endTime[5:7])
            endDay = int(endTime[8:10])
            endHours = int(endTime[11:13])
            endMinute = int(endTime[14:16])

            dt = datetime.now()
            start = dt.replace(year=startYear, day=startDay, month=startMonth,
                            hour=startHours, minute=startMinute, second=0, microsecond=0)
            end = dt.replace(year=endYear, day=endDay, month=endMonth,
                            hour=endHours, minute=endMinute, second=0, microsecond=0)
            resp = LedgerModel.objects.filter(trans_time__range=[start, end])
            #start
            if(len(resp) == 0):
                return "0"
            if(length == "all"):
                return str(resp)
            if(int(length) > len(resp)):
                return "-2"

            if(int(length)>=len(resp) and int(page)>1):
                return "-2"
            length = int(length)
            splitlen = math.ceil(len(resp)/length)
            split_list = []
            for i in range(splitlen):
                split_list.append(resp[length*i:length*(i+1)])
            json = {
                "data": str(split_list[int(page)-1]),
                "splitlen": str(splitlen)
            }
            respJson = str(json)
            # print("response..... ", respJson)
            #return split_list[int(page)-1]
            clientModel = Client_model_service.Client_Model_Service.fetch_by_id(
                id=merchant, created_by=created_by,client_ip_address=client_ip_address)
            authKey = clientModel.auth_key
            authIV = clientModel.auth_iv
            string = str(resp)
            encResp = auth.AESCipher(authKey, authIV).encrypt(respJson)
            return encResp
            #end
        for l in LedgerModel.objects.raw(query):
                d = {
                    'payoutTransactionId':l.payout_trans_id,
                    'amount': l.amount,
                    'transType': l.trans_type,
                    'statusType': l.type_status,
                    'bankRefNo': l.bank_ref_no,
                    'orderId': l.customer_ref_no,
                    'beneficiaryAccountName': l.bene_account_name,
                    'beneficiaryAccountNumber': l.bene_account_number,
                    'beneficiaryIFSC': l.bene_ifsc,
                    'transStatus': l.trans_status,
                    'mode': l.mode
                }
                resp.append(d)
        # print("length = ", int(length), " and ", len(resp))
        # if(len(resp) == 0):
        #     return "0"
        # if(length == "all"):
        #     return str(resp)
        # if(int(length) > len(resp)):
        #     return "-2"

        # if(int(length)>=len(resp) and int(page)>1):
        #     return "-2"
        # length = int(length)
        # splitlen = math.ceil(len(resp)/length)
        # split_list = []
        # for i in range(splitlen):
        #     split_list.append(resp[length*i:length*(i+1)])
        # json = {
        #     "data": str(split_list[int(page)-1]),
        #     "splitlen": str(splitlen)
        # }
        # respJson = str(json)
        # print("response..... ", respJson)
        #return split_list[int(page)-1]
        return d