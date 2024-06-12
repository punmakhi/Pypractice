from netmiko import ConnectHandler
import time
import os
# Define your network devices


sdwan_router_ips= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\routers_ip_csh.txt", "r")

os.mkdir(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files")

commands=['show running-config', 'show ip route', 'show ip interface brief']
k=1
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
    
    ssh.enable()
    #####################################

    for x in commands:
          
        if x=='show ip route vrf 10' or x=='show ip route':
            
            ssh.enable()
            base_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_pre0.txt".format(router_ips,x), "w")
            details=ssh.send_command(x, read_timeout=20)
            base_path.write(x+ "\n" + details+ "\n")
            
            base_path.close()
    
            open_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_pre0.txt".format(router_ips,x), "r")
            write_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_pre.txt".format(router_ips,x), "w")
            
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

                write_path.write(new_string+ "\n")

                new_list=[]
                new_string=""
            

            write_path.close()
            open_path.close()
            #time.sleep(10)
        
        else:
        
            print(x+"\n")
            write_path= open(r"C:\Users\punmakhi\OneDrive - Cisco\Desktop\Scripts\Scripts\multifile\Temp files\{}{}_pre.txt".format(router_ips,x), "w")    
            ssh.enable()
            rest_commands=ssh.send_command(x,read_timeout=20)
            write_path.write("\n"+x + "\n" + rest_commands+"\n")
            
            #time.sleep(10)



        write_path.close()


sdwan_router_ips.close()

