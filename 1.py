#coding=utf-8
import sys
import re
import os
import urllib
import md5
import time
import netaddr
import cidrize
class SearchIP():
	def __init__(self):
		self.cidr=[]
		self.cidr_str=""
	def percent(self,a,b,c):
		per=100.0*a*b/c
		if per > 100:
			per=100
		print '%.2f%%\r' %per,

	def update(self):
		urllib.urlretrieve('https://o0z9oq5sk.qnssl.com/qqwry.dat','qqwry.dat',self,percent)

	def check_file(self):
		if os.path.exists('qqwry.dat'):
			pass
		else:
			print 'qqwry.dat does not exist!Downloading....'
			self.update()
			
	def search(self,key):
		ip_list={}
		self.final_list=[]
		arglong=len(sys.argv)-1
		filename=''
		count=0
		for i in range(0,arglong):
			ip_list[i]=[]
			arg=sys.argv[i+1]
			filename+=arg+'-'
			ipcount=0
			if i == 0:
				count+=1
				print 'Processing %s'%arg
				for ip in open("qqwry.dat").readlines():
					ip=ip.strip('\n')
					key1=re.search(arg,ip)
					if key1:
						ipcount+=1
						print 'Found %s\r' %ipcount,
						ip_list[i].append(ip)
				if count == arglong:
					for ip in ip_list[i]:
						ip2=re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}',ip)
						self.final_list.append('%s\t%s'%(ip2[0],ip2[1]))
					self.filename=filename.rstrip('-')+'.txt'
			else:
				count+=1
				print '\nProcessing %s'%arg
				for ip in ip_list[i-1]:
					key2=re.search(arg,ip)
					if key2:
						ipcount+=1
						print 'Found %s\r' %ipcount,
						ip_list[i].append(ip)
				if count == arglong:
					for ip in ip_list[i]:
						ip2=re.findall('(?:[0-9]{1,3}\.){3}[0-9]{1,3}',ip)
						self.final_list.append('%s\t%s'%(ip2[0],ip2[1]))
					self.filename=filename.rstrip('-')+'.txt'
					
	def optimize_network(self):
		print ('\nOptimizing network...')
		lines=""
		for ip in self.final_list:
			ip=ip.strip('\n')
			startip = ip.split('\t')[0]
			endip = ip.split('\t')[1]
			cidrs = netaddr.iprange_to_cidrs(startip, endip)
			for k, cidr in enumerate(cidrs):
				self.cidr.append(cidr)
		for line in self.cidr:
			lines += str(line)+","
		lines=lines.rstrip(",")
		obj=cidrize.optimize_network_range(lines)
		f=open(self.filename,'a')
		for new_cidr in cidrize.output_str(obj).split(", "):
			ip=netaddr.IPNetwork(new_cidr)
			start=str(netaddr.IPAddress(ip.first)).strip('\n')
			end=str(netaddr.IPAddress(ip.last)).strip('\n')
			f.write('%s\t%s\n'%(start,end))
		f.close()
		print ('Saved %d results as:%s'%(len(cidrize.output_str(obj).split(", ")),self.filename))
if __name__ == '__main__':
	run=SearchIP()
	key=sys.argv
	run.check_file()
	run.search(key)
	run.optimize_network()