import paramiko
import time
import re
from pprint import pprint
import creds

##Adding stuff I don't want

####WARNING
#slow ACS server responds breaks program.  Additional checks should be implmented


#######TO DO###################
##add date/time to file name

##add config rotation

##Add logging

##set hostname


##NOTES

####Cisco terminal width is only 512, so config lines longer than that
####will wrap to the next line which will cause parsing issues...update
##it seems that it doesn't cause an issue.. not sure why..

#is it better to have each line of the output in a list, or just one big single string?
#it seems that having it in a list will make it easier to iterate through and use
#regex ^ character.  UPDATE.  I'm trying the list

#on the other hand, I will need to append the file instead of just writing a new
#file each time, not the case, writelines() takes a list.. no for loop needed



###for the regex parsing, I might need to convert byte to utf-8 first!!!!


ip = '100.123.57.6'
user = creds.username
password = creds.password
recv_buffer = 100000


class NetworkDevice:
    def __init__(self,ip,user,password,recv_buffer=100000):
        self.ip = ip
        self.user = user
        self.password = password
        self.recv_buffer = recv_buffer

        self.sh_config = ''
        self.sh_ver = ''
        self.sh_cdp_neighbors = ''
        self.config = ''
        self.ver = ''
        self.cdp_neighbors_list = []
        self.shell = None
        
    def connect(self):
        '''
        Takes IP, user and password
        Returns shell object
        '''
        remote_connection = paramiko.SSHClient()
        remote_connection.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        remote_connection.connect(ip, username=self.user,password=self.password)

        
        self.shell = remote_connection.invoke_shell()
        self.shell.send("term length 0\n")
        time.sleep(1)
        self.shell.recv(1000) #This clears out the "term length" output


    def get_config(self):
        self.shell.send("show run \n")
        time.sleep(2)
        #might need to sanitize longer than 512bytes lines
        self.sh_config = self.shell.recv(recv_buffer)

        output_list = dev.sh_config.decode("utf-8").splitlines(True)#keep \n character
        
        with open(self.ip+'_config.txt','w') as f:
            f.writelines(output_list)

    def get_version(self):
        self.shell.send("show ver \n")
        time.sleep(2)
        self.sh_version = self.shell.recv(recv_buffer)

        output_list = dev.sh_version.decode("utf-8").splitlines(True)#keep \n character
        
        with open(self.ip+'_version.txt','w') as f:
            f.writelines(output_list)

        pattern = re.compile(', Version (\d+\.\d+\(\w*\)\w\w\w+)')
        for line in output_list:
            mo = pattern.search(line)
            if mo != None:
                self.version = mo.group(1)

    def get_cdp_neighbors(self):
        self.shell.send("show cdp neigh detail  \n")
        time.sleep(2)
        self.sh_cdp_neighbors = self.shell.recv(recv_buffer)

        #Write 'cdp neighbors' output to file

        output_list = dev.sh_cdp_neighbors.decode("utf-8").splitlines(True)#keep \n character
        
        with open(self.ip+'_cdp_neighbors.txt','w') as f:
            f.writelines(output_list)

        #Create new CdpNeighbor object and populate it with data
        #Append each object to cdpneighbor list

        neigh_dev_id_pattern = re.compile('Device ID: (.*)')
        neigh_platform_pattern = re.compile('Platform: (.*),')  
        neigh_ip_pattern = re.compile('IP address: (.*)')
        neigh_interf_pattern = re.compile('Interface: (.*),')

        dev_list = dev.sh_cdp_neighbors.decode("utf-8").split('-------------------------')

        #pprint(dev_list[2])



        for device in dev_list[1:]:  #slice off show command 
            neighbor = CdpNeighbor()
        
            neigh_dev_id_mo = neigh_dev_id_pattern.search(device)
            neigh_platform_mo = neigh_platform_pattern.search(device)
            neigh_ip_mo = neigh_ip_pattern.search(device)
            neigh_interf_mo = neigh_interf_pattern.search(device)



            if neigh_dev_id_mo != None:
                 neighbor.device_id = neigh_dev_id_mo.group(1)


            if neigh_platform_mo != None:
                 neighbor.platform = neigh_platform_mo.group(1)


            if neigh_ip_mo != None:
                 neighbor.ip = neigh_ip_mo.group(1)

            if neigh_interf_mo != None:
                 neighbor.interf = neigh_interf_mo.group(1)

            self.cdp_neighbors_list.append(neighbor)



##take the 'show cdp neigh details' output, split on '-------------------------'
            
                
class CdpNeighbor:
    def __init__(self):

        self.device_id = ''
        self.platform = ''
        self.ip = ''
        self.interf = ''
    


def writetoexcel(single_network_device_object):
    #pass this function a network device object
    #each network device will have things like ip, hostname, a list of cdp neighbors
    #this write columns for each interface (probably up to 28)
    #and populate the columns with a device id when it finds something on that interface
    ##how do I keep track of the row?
    pass


    
##for device in listofdevices():
##    writetoexcel(device)
    

dev = NetworkDevice(ip,user,password)
dev.connect()

dev.get_version()
dev.get_config()
dev.get_cdp_neighbors()

#print(dev.cdp_neighbors['device_id'])
#print(len(dev.cdp_neighbors_list))
#print(dev.cdp_neighbors_list[1].ip)

print('**************************************')
print('Device IP: ', dev.ip)
print('Device version: ', dev.version)
print('CDP Neighbors: ')

for neigh_device in dev.cdp_neighbors_list:
    print('-------------------')
    print(neigh_device.device_id)
    print(neigh_device.platform)
    print(neigh_device.ip)
    print(neigh_device.interf)

print('**************************************')





########legacy code##############

##output_list = dev.config.decode("utf-8").splitlines(True)#keep \n character

#output= dev.config.decode("utf-8")

#pprint(output_list)

##with open(ip+'_config.txt','w') as f:
##    f.writelines(output_list)
##    #for line in output_list:
##        #print(line)
##        #f.writelines(line)
##
##    
##



#print(dev.version)
#print(dev.config)
#print(dev.cdp_neighbors)
