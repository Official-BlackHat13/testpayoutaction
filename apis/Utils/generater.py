import random
from datetime import datetime

def generate_token():
    payout_txnid="SAB"+str(datetime.now)+str(random.randint(10,50))
    return payout_txnid