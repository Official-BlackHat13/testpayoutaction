from rest_framework import status
from sabpaisa import auth
from datetime import datetime

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

    def fetchAll(clientCode):
        clientModelService = Client_model_service.Client_Model_Service()
        clientModel = clientModelService.fetch_by_clientcode(clientCode)
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
    
    def findById(id):
        ledger = LedgerModel.objects.filter(id=id)
        if(len(ledger) > 0):
            return True
        else:
            return False
    
    def findByClientCodeService(clientCode):
        clientModelService = Client_model_service.Client_Model_Service()
        clientModel = clientModelService.fetch_by_clientcode(clientCode)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        ledgerModel = LedgerModel.objects.filter(client_code = clientCode)
        if(len(ledgerModel)==0):
            return "0"
        resp = str(list(ledgerModel.values()))
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp
    
    def findByClientIdService(clientId, clientCode):
        clientModelService = Client_model_service.Client_Model_Service()
        clientModel = clientModelService.fetch_by_clientcode(clientCode)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        ledgerModel = LedgerModel.objects.filter(client=clientId)
        if(len(ledgerModel) == 0):
            return "0"
        resp = str(list(ledgerModel.values()))
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp
    
    def findByTransTimeService(startTranstime, endTransTime,clientCode):
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

        clientModelService = Client_model_service.Client_Model_Service()
        clientModel = clientModelService.fetch_by_clientcode(clientCode)
        authKey = clientModel.auth_key
        authIV = clientModel.auth_iv
        if(len(Ledger) == 0):
                return "0"
        resp = str(list(Ledger.values()))
        encResp = auth.AESCipher(authKey, authIV).encrypt(resp)
        return encResp