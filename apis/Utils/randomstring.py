import random
ran="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
def randomString():
    s=""
    for i in range(17):
      no=random.randint(0,len(ran))
      s=s+ran[no]
    return s

