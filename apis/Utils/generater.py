import random
from datetime import datetime

def generate_token():
    payout_txnid=str(datetime.now()).replace("-","")+str(random.randint(10,50))
    payout_txnid=payout_txnid.replace(" ","").replace(":","").replace(".","")
    return payout_txnid