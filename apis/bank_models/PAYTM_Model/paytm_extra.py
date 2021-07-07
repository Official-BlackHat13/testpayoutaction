import datetime
purpose_list = ["SALARY_DISBURSEMENT","REIMBURSEMENT","BONUS","INCENTIVE","OTHERS"]
def generate_order_id():
    return "SAB"+str(datetime.datetime.now()).replace("-","")
