import subprocess
def runJavaCode(data,key):
    subprocess.call("cd java_code",shell=True)
    return str(subprocess.call("java EncryptData.java "+data+" "+key,shell=True))[2:]
    
    # print(str(subprocess.check_output("dir",shell=True))[2:])
# runJavaCode("","")