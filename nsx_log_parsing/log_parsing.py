#!/usr/bin/env python
# coding: utf-8

# In[66]:



import os
import fnmatch 
import re
import sys
try:
    import markup
except:
    print __doc__
    sys.exit( 1 )
from markup import oneliner as e


# In[67]:

# ## define a function to get file list

# In[32]:

def get_file_list(path,file_name):
    file_list = []
    for root,dirs,files in os.walk(path):
        for file in fnmatch.filter(files,file_name):
            file_list.append(os.path.join(root,file))
    if not file_list:

        print "I didn't find %s" %file_name
    return file_list


# ## List useful vmk info，return list[hostname,mgmt_vmk,vxlan_vmk]

# In[33]:

def get_vmk_info(vmk_file):
    print('-' * 80) 
    #path_name = vmk_file.split('/')[:-2] 
    f=open(vmk_file)
    lines=f.readlines()
    for line in lines:
        if re.search(r'vmk0.*IPv4',line):
            #print line.split()
            mgmt_vmk = 'mgmt ' + line.split()[0] +' :'+ line.split()[-9]
            print mgmt_vmk
        if re.search(r'IPv4.*vxlan',line):
            vxlan_vmk = 'vxlan ' + line.split()[0] +' :'+ line.split()[-9]
            print vxlan_vmk
    f.close()
    return mgmt_vmk,vxlan_vmk


# ## list vxlan and controller mapping and return a dict

# In[34]:

def get_vxlan_info(vxlan_file):
    re_vds = re.compile(r'VXLAN VDS:*')
    re_vxlan = re.compile(r'VXLAN network:.*\d')
    re_controller = re.compile(r'^\sController:.*\d.*')
    vxlan_controller_dict = {}
    #print vxlan_file.split('/')[1]
    with open(vxlan_file) as myfile:
        for num,line in enumerate(myfile, 1):
            if re_vds.match(line):
                print line
                    #print num
            if re_vxlan.match(line):
                vxlan_num = num
                c_line_num = num + 2 
                f=open(vxlan_file)
                lines=f.readlines()
                if re_controller.match(lines[c_line_num]):
                        #print lines[c_line_num-3]   # why -3 ? 
                        #print lines[c_line_num]
                        #print lines[c_line_num-3].split()[2]
                    key_dict = lines[c_line_num-3].split()[2] #print vxlan network number
                        #print lines[c_line_num].split()[1]
                    value_dict = lines[c_line_num].split()[1:]#print controller ip 
                    vxlan_controller_dict[key_dict]=value_dict
        #print vxlan_controller_dict
    
    return vxlan_controller_dict


# In[35]:

def get_vds_name(vxlan_file):
    re_vds = re.compile(r'VXLAN VDS:*')
    f=open(vxlan_file)
    lines=f.readlines()
    for line in lines:
        if re_vds.match(line):
            vds_name = line.split()[2]
    return vds_name


# In[36]:

def get_vtep_table(vxlan_file,vds_name,vxlan_number):
    pattern = 'Executing:: net-vdl2 -M vtep -s'+' '+vds_name+' -n '+vxlan_number
    #print pattern
    re_pattern = re.compile(pattern)
    with open(vxlan_file) as myfile:
        for num,line in enumerate(myfile, 1):
            if re_pattern.match(line):
                start_num = num 
                #print 'start_num is %s\n' %start_num
                f=open(vxlan_file)
                lines=f.readlines()
                #print lines[start_num]
                count = lines[start_num].split(':')[1]
                count_num = int(count)
                #print count_num
                #print type(count_num)
                end_num = start_num+(count_num*3)
                #print end_num
                vtep_table_list = lines[start_num-1:end_num+1]
    return vtep_table_list
               


# In[37]:

def get_mac_table(vxlan_file,vds_name,vxlan_number):
    pattern = 'Executing:: net-vdl2 -M mac -s'+' '+vds_name+' -n '+vxlan_number
    #print pattern
    re_pattern = re.compile(pattern)
    with open(vxlan_file) as myfile:
        for num,line in enumerate(myfile, 1):
            if re_pattern.match(line):
                start_num = num 
                #print 'start_num is %s\n' %start_num
                f=open(vxlan_file)
                lines=f.readlines()
                #print lines[start_num]
                count = lines[start_num].split(':')[1]
                count_num = int(count)
                #print count_num
                #print type(count_num)
                end_num = start_num+(count_num*4)
                #print end_num
                mac_table_list = lines[start_num-1:end_num+1]
                #print mac_table_list
    return mac_table_list


# In[38]:

def get_arp_table(vxlan_file,vds_name,vxlan_number):
    pattern = 'Executing:: net-vdl2 -M arp -s'+' '+vds_name+' -n '+vxlan_number
    #print pattern
    re_pattern = re.compile(pattern)
    with open(vxlan_file) as myfile:
        for num,line in enumerate(myfile, 1):
            if re_pattern.match(line):
                start_num = num 
                #print 'start_num is %s\n' %start_num
                f=open(vxlan_file)
                lines=f.readlines()
               # print lines[start_num]
                count = lines[start_num].split(':')[1]
                #print count
                count_num = int(count)
                #print count_num
                #print type(count_num)
                end_num = start_num+(count_num*3)
                #print end_num
                vtep_table_list = lines[start_num-1:end_num+1]
    return vtep_table_list


# In[45]:


# In[68]:

def get_nsx_version(path):
    file_list = []
    re_version = re.compile(r'System Version:*')
    for root,dirs,files in os.walk(path):
        for file in fnmatch.filter(files,'sys_info'):
            file_list.append(os.path.join(root,file))
    if len(file_list) == 0:
        print "I didn't find %s" %file_name
    elif len(file_list) > 1 :
        print "more than one nsx bundle in this %s" %path
    else :
        with open(file_list[0]) as fp:
            for line in fp:
                if re_version.match(line):
                    version = line
                    nsx_version = version.split(':')[1]
                    return nsx_version


# In[ ]:




# In[69]:

def get_nsx_ip(path):
    file_list = []
    re_pattern = re.compile(r'mgmt')
    for root,dirs,files in os.walk(path):
        for file in fnmatch.filter(files,'sys_net'):
            file_list.append(os.path.join(root,file))
    if len(file_list) == 0:
        print "I didn't find %s" %file_name
    elif len(file_list) > 1 :
        print "more than one nsx bundle in this %s" %path
    else :
        #print (file_list[0])
        with open(file_list[0]) as fp:
            for num,line in enumerate(fp,1):
                if re_pattern.match(line):
                    f=open(file_list[0])
                    lines=f.readlines()
                    ip = lines[num].split()[1]
                    f.close()
    nsx_ip = ip.split(':')[1]
    return nsx_ip


# In[70]:

def use_count(path):
    host_name = os.uname()[1]
    if gss in host_name :
        f = open('/users/home10/shensong/shared/td_use_times', 'w+')
        f.write(path+'\n')  # python will convert \n to os.linesep
        f.close()  # you can omit in most cases as the destructor will call it


# In[71]:

def get_vc_ip(vpxa_cfg):
    with open(vpxa_cfg) as fp:
            for line in fp:
                if 'serverIp' in line:
                    ip = re.sub('<[^>]*>', '',line)
    return ip


# In[72]:

def get_vc_version(path):
    file_list = []
    for root,dirs,files in os.walk(path):
        for file in fnmatch.filter(files,'vpxd-[0-9]*[0-9].log'):
            file_list.append(os.path.join(root,file))
    if len(file_list) == 0:
        print "I didn't find vpxd log in this %s" %path
    elif len(file_list) > 1 :
        print "more than one vc log bundle in this %s" %path
    else :
        f=open(file_list[0])
        lines=f.readlines()
        vc_version_list = lines[0].split(',')[-3:-1]
        vc_version = ''.join(vc_version_list)
        vc = re.sub('=',' ',vc_version)
        return vc    


# In[73]:

def main():
    path = os.getcwd()
    use_count
    print('-' * 80) 
    NSX_Version = get_nsx_version(path)
    print 'NSX version is %s \n' %NSX_Version
    NSX_IP = get_nsx_ip(path)
    print 'NSX manager IP is %s \n' %NSX_IP
    
    vpxa_cfg_list = get_file_list(path,"vpxa.cfg")
    vpxa_cfg = vpxa_cfg_list[0]
    VC_ip = get_vc_ip(vpxa_cfg)
    VC_version = get_vc_version(path)
    print 'vCenter IP is  %s  \n' %VC_ip
    print 'vCenter version is %s \n' %VC_version
    print 'Please check product matrix \n'
    print 'https://www.vmware.com/resources/compatibility/sim/interop_matrix.php \n'
    
    vdr_info_list = get_file_list(path,"dump-vdr-info.sh.txt")
    vxlan_info_list = get_file_list(path,"dump-vxlan-info.py.txt")
    vmk_info_list = get_file_list(path,"esxcfg-vmknic_-l.txt")
    ## Get VC IP from esxi bundle
    vpxa_cfg_list = get_file_list(path,"vpxa.cfg")
    if len(vpxa_cfg_list) > 0:
        get_vc_ip(vpxa_cfg_list[0])
    num_file = len(vdr_info_list)
   

    for i in range(num_file):
        page = markup.page( )
        page.init( title="NSX log ", 
                   header="NSX vxlan info ", 
                   footer="I will develop more ....." )
        page.style("""
                    body {
                            background-color: AliceBlue ;
                        }

                        table {
                                font-family: arial, sans-serif;
                                border-collapse: collapse;
                                width: 70%;
                                }

                        td, th {
                                    border: 1px solid #dddddd;
                                    text-align: left;
                                    padding: 8px;
                                }

            tr:nth-child(even) {
                                background-color: #dddddd;
                                }
                        p {
                            font-family: verdana;
                            font-size: 20px;
                            }
                    """)
        page.h1
        esx_info = get_vmk_info(vmk_info_list[i])   # esxi_info is a list  [hostname,vmk0,vxlan_vmk]
        
        page.br()
        page.p(esx_info)
        page.br()
        
        controller_mapping_dict = get_vxlan_info(vxlan_info_list[i]) # this is a dict
        
        for vxlan,controller in controller_mapping_dict.items():
            print('{} {}'.format(vxlan,controller))
        print('-' * 80)
        # create table for vxlan mapping to controller 
        page.div(style="overflow-x:auto;")
        page.table(border="1")
        page.tr()
        page.th('vxlan')
        page.th('controller')
        page.th('status')
        page.tr.close()
        for vxlan,controller in controller_mapping_dict.items():
            page.tr()
            page.td(vxlan)
            page.td(controller)
            page.tr.close()
        page.table.close()
        
        vxlan_list = controller_mapping_dict.keys()    # this a vlxan list
        # create vxlan link table 
        page.br()
        page.table(border="1")
        page.tr()
        page.th('vxlan')
        page.th('vtep')
        page.th('arp')
        page.th('mac')
        page.tr.close()
        for vxlan in vxlan_list:
            page.tr()
            page.td(vxlan)
            page.td(e.a(vxlan+'_vtep',href='#'+vxlan+'_vtep'))
            page.td(e.a(vxlan+'_arp',href='#'+vxlan+'_arp'))
            page.td(e.a(vxlan+'_mac',href='#'+vxlan+'_mac'))
            page.tr.close()
        page.table.close()
    
        vds_name = get_vds_name(vxlan_info_list[i])
       
        for vxlan_num in vxlan_list:
            VTEP = get_vtep_table(vxlan_info_list[i],vds_name,vxlan_num) # this is a list 
            ARP = get_arp_table(vxlan_info_list[i],vds_name,vxlan_num)
            MAC = get_mac_table(vxlan_info_list[i],vds_name,vxlan_num)
            #create vtep,arp,mac
            name_vtep = vxlan_num + '_vtep'
            page.br()
            page.h2(e.a(id=name_vtep))
            page.p(VTEP)
            page.br()
            page.h2(e.a(id=vxlan_num+'_arp'))
            page.p(ARP)
            page.br()
            page.h2(e.a(id=vxlan_num+'_mac'))
            page.p(MAC)
            page.br()
        filename = esx_info[0] +'.html'
    
        h = open(filename,'w')
        h.write(str(page))
        h.close()


# In[46]:


# In[74]:

if __name__ == "__main__":
    main()


# In[ ]:




# In[ ]:



