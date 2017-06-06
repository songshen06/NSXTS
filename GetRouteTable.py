#!/usr/bin/python
#-*- coding:utf-8 -*-
import paramiko
import time
import re
from ConfigParser import ConfigParser
def GetEdgeList(nsxm_host,nsxm_user,nsxm_pass):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(nsxm_host,22,nsxm_user,nsxm_pass)
        ssh_conn = ssh.invoke_shell()
        print "=============connected to nsxmanager %s" %nsxm_host
        time.sleep(1)
        ssh_conn.send('show edge all\n')
        time.sleep(1)
        output = ssh_conn.recv(10000)
        print output
        edge_Id_list = []
        for x in output.splitlines():
                if 'edge-' in x:
                        edge_Id_list = [re.split('\s*',x)[0]] + edge_Id_list
        command_route_list = ['show edge '+x + ' ip route\n' for x in edge_Id_list]
        for command in command_route_list:
                #print command
                ssh_conn.send(command)
                time.sleep(2)
                #stdin ,stdout, stderr = ssh.exec_command(command)
                #time.sleep(1)
                #print stdout.read()
        output = ssh_conn.recv(10000)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        print output
        f = open(timestr,'w+')
        f.write(output)
        f.close()
        ssh.close()

def main():
        filename = 'info.ini'
        config = ConfigParser()
        config.read(filename)
        nsxm_user = config.get("nsxm","nsxm_user")
        nsxm_host = config.get("nsxm","nsxm_host")
        nsxm_pass = config.get("nsxm","nsxm_pass");
        print time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        GetEdgeList(nsxm_host,nsxm_user,nsxm_pass)

if __name__ == "__main__":
   main()
