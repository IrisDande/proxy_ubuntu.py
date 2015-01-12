#!/usr/bin/python
#convert string to hex
from __future__ import print_function
import sys
import os
import getopt
import shutil
import fileinput
import os.path

def toHex(s):
    lst = []
    for ch in s:
        hv = hex(ord(ch)).replace('0x', '')
        if len(hv) == 1:
            hv = '0'+hv
        lst.append(hv)
    
    return reduce(lambda x,y:x+y, lst)

#convert hex repr to string
def toStr(s):
    return s and chr(atoi(s[:2], base=16)) + toStr(s[2:]) or ''

#############run as normal user#####
def usrun():
	line=sys.stdin.readline()[:-1]
	[user,password]=line.split(' ')
	charactertohex = toHex(password)
	listpass = list(password)
	percent = "%"
	nchar = ""
	for xnumber in listpass:
		if xnumber.isalpha():
			nchar = nchar + xnumber
		else:
			if xnumber.isdigit():
				nchar = nchar + str(xnumber)
				#print n
			else:	
				jchar = percent+toHex(xnumber)
				nchar = nchar + jchar
	kapt = 'Acquire::http::proxy "http://'
	kapt1 = 'http_proxy="http://'
	kapt2 = 'HTTP_PROXY="http://'
	papt = '@proxy.smartosc.com:3128/";'
	papt1 = '@proxy.smartosc.com:3128/"' 
	print ("Checking proxy is set or not")
	seachremove()
	hostname = "proxy.smartosc.com"
	response = os.system("ping -c 1 " + hostname)
	#Set proxy for apt-get
	if response == 0:
		print ("set proxy for apt")
		e = kapt+user+':'+nchar+papt
		e1 = kapt1+user+':'+nchar+papt1+'\n'+kapt2+user+':'+nchar+papt1+'\n\n'
		e = kapt+user+':'+nchar+papt+'\n'
		print ("Writing to file")
		files = open('/etc/apt/apt.conf', 'w')
		files.write(e)
		files.close()
		
		print ("Setting proxy into environment")
		Lenvironment = list()
		fenvironment = open('/etc/environment', 'r')
		for line in fenvironment.readlines():
			Lenvironment.append(line)
		Lenvironment.insert(0,e1)
		fenvironment.close()

		fenvironment2 = open('/etc/environment', 'w')
		for line in xrange(len(Lenvironment)):
			fenvironment2.write(Lenvironment[line])
		fenvironment2.close()
		gsettings()
		chromesettings()
		firefoxsettings()
	else:
		print ("Nothing to change")
	start = 1
	while True:
		if start != 1:        
			do_run = raw_input('Restart computer to take effect? (y/n):')
			if do_run == 'y':
				os.system("shutdown -r 01")
			elif do_run == 'n':
				break
			else: 
				print ("Invalid input")
				continue
		if start == 1:
			start = 0

def seachremove():
	files = '/etc/environment'
	fopen = open(files)
	fouput = []
	for line in fopen:
		if not 'proxy.smartosc.com' in line:
			fouput.append(line)
			print ("Removing old proxy to set new one")
		if not '\n' in line:
			fouput.append(line)
	fopen.close()
	fopen = open(files, 'w')
	fopen.writelines(fouput)
	fopen.close()
	
def gsettings():
	os.system("gsettings set org.gnome.system.proxy autoconfig-url 'http://wpad.smartosc.com/proxy.pac'")
	os.system("gsettings set org.gnome.system.proxy mode 'auto'")	

def chromesettings():
	print ("############################\nChecking if Google Chrome is installed")
	if os.path.isfile("/usr/share/applications/google-chrome.desktop"):
		print ("Google Chrome is installed")
		os.system("google-chrome --version")
		print ("Setting proxy for Google Chrome")
		fchrome = '/usr/share/applications/google-chrome.desktop'
		fopenchrome = open(fchrome)
		foutputchrome = []
		for line in fopenchrome:
			if not 'Exec' in line:
				foutputchrome.append(line)
			if 'Exec' in line:
				foutputchrome.append(line.strip()+" --proxy-auto-detect" + "\n")
		fopenchrome.close()
		fopenchrome = open(fchrome, 'w')
		fopenchrome.writelines(foutputchrome)
		fopenchrome.close()
		print ("Google Chrome is setting to Auto-detect proxy settings for this network")
		print ("Done!")
	else:
		print ("Google Chrome is not installed, no proxy is set")
	
def firefoxsettings():
	print ("############################\nChecking if Firefox is installed")
	if os.path.isfile("/usr/share/applications/firefox.desktop"):
		print ("Firefox is installed")
		os.system("firefox -version")
		print ("Setting proxy for firefox")
		ffirefox = '/etc/firefox/syspref.js'
		Lfirefox = list()
		Ffirefox = open(ffirefox, 'r')
		fvalue = 'pref("network.proxy.type", 4);\n'
		for line in Ffirefox.readlines():
			Lfirefox.append(line)
		Lfirefox.insert(0,fvalue)
		Ffirefox.close()

		Ffirefox2 = open(ffirefox, 'w')
		for line in xrange(len(Lfirefox)):
			Ffirefox2.write(Lfirefox[line])
		Ffirefox2.close()
		print ("Firefox Proxy is setting to Auto-detect proxy settings for this network")
		print ("Done!")
	else:
		print ("Firefox is not installed on this machine, no proxy is set")
		
def main(argv):
	try:
		opts, args = getopt.getopt(argv,"hio")
	except getopt.GetoptError:
		print ('convert.py -i runas normal -h help menu')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('convert.py -a <autorun>')
			sys.exit()
		elif opt == '-i':
			usrun()
if __name__ == "__main__":
	main(sys.argv[1:])
usrun()