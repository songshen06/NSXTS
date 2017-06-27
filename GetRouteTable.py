#!/usr/bin/python
#-*- coding:utf-8 -*-
import paramiko
import time
import re
from ConfigParser import ConfigParser
#idea from https://stackoverflow.com/questions/752308/split-list-into-smaller-lists
def split_list(arr, size):
	arrs = []
	while len(arr) > size:
		pice = arr[:size]
		arrs.append(pice)
		arr   = arr[size:]
	arrs.append(arr)
	return arrs	
def GetEdgeList(nsxm_host,nsxm_user,nsxm_pass,nsxm_enpass):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(nsxm_host,22,nsxm_user,nsxm_pass)
        ssh_conn = ssh.invoke_shell()
        print "=============connected to nsxmanager %s" %nsxm_host
        time.sleep(1)
	ssh_conn.send('en\n')
	time.sleep(1)
	ssh_conn.send(nsxm_enpass+'\n')
	time.sleep(1)
	ssh_conn.send('terminal length 0\n')
	time.sleep(1)
	ssh_conn.send('disable\n')
	time.sleep(1)
        ssh_conn.send('show edge all\n')
        time.sleep(1)
        output = ssh_conn.recv(90000)
        print output
        edge_Id_list = []
        for x in output.splitlines():
                if 'edge-' in x:
                        edge_Id_list = [re.split('\s*',x)[0]] + edge_Id_list
		#splite huge edge list to small list ,ecac list have 4 edge 

        new_edge_list = split_list(edge_Id_list, 4)
        for eachList in new_edge_list:
            #print eachList
            command_route_list = ['show edge '+x + ' ip route\n' for x in eachList]
            for command in command_route_list:
                #print command
                ssh_conn.send(command)
                time.sleep(3)
                #stdin ,stdout, stderr = ssh.exec_command(command)
                #time.sleep(1)
                #print stdout.read()		
	    output = ssh_conn.recv(90000)
	    print output
	    timestr = time.strftime("%Y%m%d-%H%M%S")
		# cut mins and secons 
	    newTimeStr = timestr[:-4]
	    f = open('route_table_'+newTimeStr,'a+')
	    f.write(output)
	    f.close()
        #timestr = time.strftime("%Y%m%d-%H%M%S")
        #print output
        #f = open(timestr,'w+')
        #f.write(output)
        #f.close()
        ssh.close()
# leave this for backup		
def GetEdgeListFile(nsxm_host,nsxm_user,nsxm_pass,nsxm_enpass):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(nsxm_host,22,nsxm_user,nsxm_pass)
        ssh_conn = ssh.invoke_shell()
        print "=============connected to nsxmanager %s" %nsxm_host
        time.sleep(1)
	ssh_conn.send('en\n')
	time.sleep(1)
	ssh_conn.send(nsxm_enpass+'\n')
	time.sleep(1)
	ssh_conn.send('terminal length 0\n')
	time.sleep(1)
	ssh_conn.send('disable\n')
	time.sleep(1)
        ssh_conn.send('show edge all\n')
        time.sleep(4)
        output = ssh_conn.recv(10000)
        print output
        f = open('tmp','w')
        f.write(output)
        f.close()
        ssh.close()
	lines = open('tmp').readlines()
	open('edge-all', 'w').writelines(lines[12:-1])

	
def main():
        filename = 'info.ini'
        config = ConfigParser()
        config.read(filename)
        nsxm_user = config.get("nsxm","nsxm_user")
        nsxm_host = config.get("nsxm","nsxm_host")
        nsxm_pass = config.get("nsxm","nsxm_pass")
	nsxm_enpass = config.get("nsxm","nsxm_enpass")
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        GetEdgeList(nsxm_host,nsxm_user,nsxm_pass,nsxm_enpass)

if __name__ == "__main__":
   main()
