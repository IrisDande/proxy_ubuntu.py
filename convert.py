#!/usr/bin/python
#convert string to hex
from __future__ import print_function
import sys
import os
import getopt
import shutil
import fileinput
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
	if response == 0:
		e = kapt+user+':'+nchar+papt
		e1 = kapt1+user+':'+nchar+papt1+'\n'+kapt2+user+':'+nchar+papt1+'\n\n'
		print ("Writing to file")
		files = open('/etc/apt/apt.conf', 'w')
		files.write(e)
		files.close()

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
	else:
		print ("Nothing to change")

def seachremove():
	files = '/etc/environment'
	fopen = open(files)
	fouput = []
	for line in fopen:
		if not 'proxy.smartosc.com' in line:
			fouput.append(line)
			print ("Removing old proxy to set new one")
	fopen.close()
	fopen = open(files, 'w')
	fopen.writelines(fouput)
	fopen.close()
	
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