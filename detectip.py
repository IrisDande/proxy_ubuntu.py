import urllib2
def detectip():
	myip = urllib2.urlopen("http://myip.dnsdynamic.org/").read()
	print ("Your WAN IP Address is: " + myip)