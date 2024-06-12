from netmiko import ConnectHandler
import time
from difflib import Differ 
import filecmp
import os
import shutil
import re
# Define your network devices


sdwan_router_ips= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\routers_ip_csh.txt", "r")

commands=['show running-config', 'show ip route', 'show ip interface brief']

temp3 = []
string1=[]
for router_ips in sdwan_router_ips:
    router_ips= router_ips.strip()
    device_details= {
        'ip': router_ips,
        'username': 'admin',
        'password': 'cisco',
        'device_type':'cisco_ios',
        'secret':False
    }

    router_ips=str(router_ips)
    ssh= ConnectHandler(**device_details)

    diff_migration_1=open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\{}_diff.txt".format(router_ips), "w")
    post_output= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\{}_post_output.txt".format(router_ips), "w")
    #####################################

    for k in commands:
          
        if k=='show ip route vrf 10' or k=='show ip route':
            
            ssh.enable()
            base_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_post0.txt".format(router_ips,k), "w")
            post_output= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\{}_post_output.txt".format(router_ips), "a")
            details=ssh.send_command(k,read_timeout=20)
            base_path.write(k + "\n" + details + "\n")
            
            post_output.write(k + "\n" + details + "\n")

            base_path.close()
            open_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_post0.txt".format(router_ips,k), "r")
            write_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_post.txt".format(router_ips,k), "w")
            
            new_string=""
            new_list=[]
            
            while True:
                
                x=0
                read_line= open_path.readline()      

                if not read_line:
                    break        
                
                list_string= list(read_line)
                
                while x < len(read_line):
                    if list_string[x] != ",":

                        new_list.append(list_string[x])

                    elif list_string[x] ==",":
                         
                        new_list.append("")

                        y=0
                        y=x+1

                        z=len(read_line)-1
                        while list_string[y]!="," and y<z:

                            new_list.append("") 
                            y=y+1
                            x=y
                        
                    x=x+1
                new_string="".join(new_list)   

                write_path.write(new_string+"\n")
                new_list=[]
                new_string=""
            write_path.close()
            open_path.close()
            #time.sleep(10)
        else:
            
            ssh.enable()
            post_output= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\{}_post_output.txt".format(router_ips), "a")
            write_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_post.txt".format(router_ips,k), "w")    
            rest_commands=ssh.send_command(k,read_timeout=20)
            write_path.write("\n"+ k + "\n" + rest_commands + "\n")
            post_output.write("\n"+ k + "\n" + rest_commands + "\n")
            #time.sleep(10)


        write_path.close()



        pre_migration_1= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_pre.txt".format(router_ips,k), "r")
        post_migration_1=open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_post.txt".format(router_ips,k), "r")
        
        
        pre_migration= pre_migration_1.readlines()
        pre_migration = [x.strip() for x in pre_migration]
        pre_migration=list(pre_migration)
        
        post_migration= post_migration_1.readlines()
        post_migration = [x.strip() for x in post_migration]
        post_migration=list(post_migration)
        
        #time_pattern = re.compile(r'\d{1,2}:\d{2}:\d{2}|\d+[wdhms]')
             
        print("\n\n"+k)

        diff_migration_1.write("\n"+k+"\n\n<-------New Config------->\n")

        for element in post_migration:

                if element not in pre_migration:

                        
                        diff_migration_1.write("\n"+element+ "\n")
                        
                        #time_values= time_pattern.search(element)
                        #print(time_values)
                        print(element)
                        print("\n")
        


        diff_migration_1.write("\n"+"<-------Deleted Config------->\n")

        for element in pre_migration:

                if element not in post_migration:

                        
                        diff_migration_1.write("\n"+element+ "\n")
                        
                        print(element)
                        print("\n")
        diff_migration_1.write("\n---------------------------End of Command output-------------------------------------\n")

   # pre_migration_1.close()
   # post_migration_1.close()

   # diff_migration_1.close()

#time.sleep(35)

sdwan_router_ips.close()
pre_migration_1.close()
post_migration_1.close()
diff_migration_1.close()


#os.chmod(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files", 0o777)

#for router_ipss in sdwan_router_ips:
 #   for y in commands:
  #      location= r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files"
   #    path= os.path.join(location,"{}{}_post.txt".format(router_ipss,y))
    #    os.remove(path)
        #os.remove(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_post.txt".format(router_ipss,y))
        #os.remove(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_pre.txt".format(router_ipss,y))

#shutil.rmtree(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files")

