import random
ran="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
def randomString(length=16):
    s=""
    for i in range(length):
      no=random.randint(0,len(ran)-1)
      s=s+ran[no]
    return s

def randomNumber(length=16):
    s=""
    for i in range(length):
      no=random.randint(0,9)
      s=s+str(no)
    return s


