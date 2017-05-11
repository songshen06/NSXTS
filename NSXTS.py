#!/usr/bin/python
#-*- coding:utf-8 -*-
import paramiko
from sys import argv
from ConfigParser import ConfigParser
import time
import re

def controller(nsxc_host,nsxc_user,nsxc_password):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(nsxc_host,22,nsxc_user,nsxc_password)
	print "show control-cluster logical-routers instance all\n"
	stdin ,stdout, stderr = ssh.exec_command('show control-cluster logical-routers instance all')
	print stdout.read()
	print "show control-cluster logical-routers bridges all all\n"
	stdin ,stdout, stderr = ssh.exec_command('show control-cluster logical-routers bridges all all')
	print stdout.read()
	print "show control-cluster logical-routers bridge-mac all all\n"
	stdin ,stdout, stderr = ssh.exec_command('show control-cluster logical-routers bridge-mac all all')
	print stdout.read()
	ssh.close()
def esxi(esxi_hosts,esxi_user,esxi_password):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(esxi_hosts,22,esxi_user,esxi_password)
	print "esxcli network ip connection list |grep 5671 \n"
	stdin ,stdout, stderr = ssh.exec_command('esxcli network ip connection list |grep 5671')
	print stdout.read()
	print "esxcli network ip connection list |grep 1234 \n"
	stdin ,stdout, stderr = ssh.exec_command('esxcli network ip connection list |grep 1234 ')
	print stdout.read()
	print "/usr/lib/vmware/vm-support/bin/dump-vdr-info.sh \n"
	stdin ,stdout, stderr = ssh.exec_command('/usr/lib/vmware/vm-support/bin/dump-vdr-info.sh ')
	print stdout.read()
	print "/usr/lib/vmware/vm-support/bin/dump-vxlan-info.py \n"
	stdin ,stdout, stderr = ssh.exec_command('/usr/lib/vmware/vm-support/bin/dump-vxlan-info.py ')
	print stdout.read()
	ssh.close()
def nsxm(nsxm_host,nsxm_user,nsxm_pass):
	ssh = paramiko.SSHClient()
	#ssh.load_system_host_keys()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(nsxm_host,22,nsxm_user,nsxm_pass)
	ssh_conn = ssh.invoke_shell()
	ssh_conn.send('show logical-router list all\n')
	time.sleep(1)
	ssh_conn.send('show controller list all\n')
	time.sleep(1)
	ssh_conn.send('show logical-switch list all\n')
	time.sleep(1)
	output = ssh_conn.recv(5000)
	print output 
	ssh.close()
def GetVNIList(nsxm_host,nsxm_user,nsxm_pass):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(nsxm_host,22,nsxm_user,nsxm_pass)
	ssh_conn = ssh.invoke_shell()
	ssh_conn.send('show logical-switch list all\n')
	time.sleep(1) 
	output = ssh_conn.recv(5000)
	print output
	#vni_list = [re.split('\s*',x)[2] for x in output.splitlines()[4:-2]]
	vni_list =[]
	for x in output.splitlines()[3:-2]:
		if 'VNI' not in x:
			vni_list = [re.split('\s*',x)[2]] + vni_list
	ssh.close()
	return vni_list

def GetVNITable(nsxc_host,nsxc_user,nsxc_password,vni_list):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(nsxc_host,22,nsxc_user,nsxc_password)
	command_vtep_list = ['show control-cluster logical-switches vtep-table '+x for x in vni_list] 
	for command in command_vtep_list:
		print command
		stdin ,stdout, stderr = ssh.exec_command(command)
		time.sleep(1)
		print stdout.read()
	command_mac_list = ['show control-cluster logical-switches mac-table '+x for x in vni_list]	
	for command in command_mac_list:
		print command
		stdin ,stdout, stderr = ssh.exec_command(command)
		time.sleep(1)
		print stdout.read()
	command_arp_list = ['show control-cluster logical-switches arp-table '+x for x in vni_list]
	for command in command_arp_list:
		print command
		stdin ,stdout, stderr = ssh.exec_command(command)
		time.sleep(1)
		print stdout.read()
	ssh.close()
def GetRouterList(nsxc_host,nsxc_user,nsxc_password):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(nsxc_host,22,nsxc_user,nsxc_password)
	ssh_conn = ssh.invoke_shell()
	print "=============connected to controller %s" %nsxc_host
	time.sleep(1)
	ssh_conn.send('show control-cluster logical-routers instance all\n')
	time.sleep(1)
	output = ssh_conn.recv(5000)
	router_Id_list = []
	for x in output.splitlines():
		if '0x' in x:
			router_Id_list = [re.split('\s*',x)[0]] + router_Id_list
	ssh.close()
	return router_Id_list
def GetRouteTable(nsxc_host,nsxc_user,nsxc_password,RouterIDList):	
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	ssh.connect(nsxc_host,22,nsxc_user,nsxc_password)
	command_route_list = ['show control-cluster logical-routers routes '+x for x in RouterIDList] 
	for command in command_route_list:
		print command
		stdin ,stdout, stderr = ssh.exec_command(command)
		time.sleep(1)
		print stdout.read()
def main():	
	script,filename = argv	
	config = ConfigParser()
	config.read(filename)
	nsxc_hosts = config.get("controller","nsxc_hosts")
	nsxc_user = config.get("controller","nsxc_user")
	nsxc_password = config.get("controller","nsxc_password")
	esxi_hosts = config.get("esxi","esxi_hosts")
	esxi_user = config.get("esxi","esxi_user")
	esxi_password = config.get("esxi","esxi_password")
	nsxm_user = config.get("nsxm","nsxm_user")
	print nsxm_user
	nsxm_host = config.get("nsxm","nsxm_host")
	print nsxm_host
	nsxm_pass = config.get("nsxm","nsxm_pass")
	print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
	
	print "===========Collecting NSXM info====================="
	nsxm(nsxm_host,nsxm_user,nsxm_pass)
	print "===========Collecting controller info==============  "
	for nsxc_host in nsxc_hosts.split(','):
		print nsxc_host
		controller(nsxc_host,nsxc_user,nsxc_password)
	print "===========Collecting esxi host info==============  "
	for esxi_host in esxi_hosts.split(','):
		print "=========================%s==================" %esxi_host
		esxi(esxi_host,esxi_user,esxi_password)
	
	vni_list = GetVNIList(nsxm_host,nsxm_user,nsxm_pass)
	print vni_list 
	for nsxc_host in nsxc_hosts.split():
		print "==========================%s======================" %nsxc_host
		RouterIDList = GetRouterList(nsxc_host,nsxc_user,nsxc_password)
		print RouterIDList
		GetRouteTable(nsxc_host,nsxc_user,nsxc_password,RouterIDList)	
		GetVNITable(nsxc_host,nsxc_user,nsxc_password,vni_list)
		
if __name__ == "__main__":
   main()
