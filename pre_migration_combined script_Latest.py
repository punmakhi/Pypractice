from netmiko import ConnectHandler
import os

# Define your network devices IP address in "sdwan_router_ips" text file

sdwan_router_ips= open(r"DEFINE FILE PATH WHERE DEVICE IP ADDRESSES ARE STORED\routers_ip_csh.txt", "r")

os.mkdir(r"DEFINE PATH WHERE YOU WANT TO CREATE TEMPORARY FOLDER")

#Pre-defined CLIs to fetch desired output
commands=['show running-config', 'show ip route', 'show ip interface brief']
k=1

# To connect and fetch desired CLI output from each device
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
#Capture output of each command via loop
    for x in commands:
          
        if x=='show ip route vrf 10' or x=='show ip route':
            
            ssh.enable()
            base_path= open(r"DEFINE FILE PATH WHERE TEMPORARY OUTPUT OF "SHOW IP ROUTE" CLI WILL BE CAPTURED\{}{}_pre0.txt".format(router_ips,x), "w")
            details=ssh.send_command(x, read_timeout=20)
            base_path.write(x+ "\n" + details+ "\n")
            
            base_path.close()
    
            open_path= open(r"DEFINE FILE PATH OF "BASE PATH" FILE TO READ ITS CONTENT\{}{}_pre0.txt".format(router_ips,x), "r")
            write_path= open(r"DEFINE FILE PATH TO CAPTURE PARSED OUTPUT OF ANY VARIENT OF 'SHOW IP ROUTE' CLI\{}{}_pre.txt".format(router_ips,x), "w")

            #Define variables to capture parsed output
            
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
            
        else:
        
            print(x+"\n")
            write_path= open(r"DEFINE FILE PATH TO CAPTURE PARSED OUTPUT OF ANY VARIENT 'SHOW IP ROUTE' CLI\{}{}_pre.txt".format(router_ips,x), "w")    
            ssh.enable()
            rest_commands=ssh.send_command(x,read_timeout=20)
            write_path.write("\n"+x + "\n" + rest_commands+"\n")

        write_path.close()


sdwan_router_ips.close()

