import random
ran="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
def randomString():
    s=""
    for i in range(16):
      no=random.randint(0,len(ran)-1)
      s=s+ran[no]
    return s

