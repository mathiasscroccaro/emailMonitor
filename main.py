import emailLib

def main():
    fileObj = open('/home/mathias/emailMonitor/credentials','r')
    credentials = fileObj.read().split(':')
    user = credentials[0]
    password = credentials[1][:-1]

    emailLib.emailLib(user,password)

if __name__ == "__main__":
    main()
