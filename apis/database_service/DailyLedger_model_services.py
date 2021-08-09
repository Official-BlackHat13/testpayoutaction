from ..database_models.DailyLedgerModel import DailyLedgerModel

class DailyLedger_Model_Service:
    @staticmethod
    def fetch_by_date_and_merchant_id(merchant_id,date):
        dailyledger=DailyLedgerModel.objects.filter(merchant_id=merchant_id,date=date)
        if len(dailyledger)==0:
            return None
        return dailyledger