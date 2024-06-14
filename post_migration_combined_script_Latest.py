from netmiko import ConnectHandler
import shutil
#
# Define your network device IP address in "sdwan_router_ips" text file.
sdwan_router_ips= open(r"DEFINE FILE PATH WHERE DEVICE IP ADDRESSES ARE STORED/routers_ip_csh.txt", "r")

#Pre-defined CLIs to fetch desired output
commands=['show running-config', 'show ip route', 'show ip interface brief']

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

    #Define variable for the files
    diff_migration_1=open(r"DEFINE FILE PATH WHERE THE DIFFERENCE OUTPUT WILL BE CAPTURED\{}_diff.txt".format(router_ips), "w")
    post_output= open(r"DEFINE FILE PATH WHERE OUTPUT OF ALL CLIs WILL BE CAPTURED\{}_post_output.txt".format(router_ips), "w")
    #####################################

    #To capture output of each command via loop
    for k in commands:
          
        if k=='show ip route vrf 10' or k=='show ip route':
            
            ssh.enable()
            base_path= open(r"DEFINE FILE PATH WHERE TEMPORARY OUTPUT OF "SHOW IP ROUTE" CLI WILL BE CAPTURED\{}{}_post0.txt".format(router_ips,k), "w")
            post_output= open(r"DEFINE FILE PATH WHERE OUTPUT OF ALL CLIs WILL BE CAPTURED\{}_post_output.txt".format(router_ips), "a")
            details=ssh.send_command(k,read_timeout=20)
            base_path.write(k + "\n" + details + "\n")
            
            post_output.write(k + "\n" + details + "\n")

            base_path.close()
            open_path= open(r"DEFINE FILE PATH OF THE "BASE PATH" FILE TO READ ITS CONTENT\{}{}_post0.txt".format(router_ips,k), "r")
            write_path= open(r"DEFINE FILE PATH TO CAPTURE PARSED OUTPUT OF ANY VARIENT 'SHOW IP ROUTE' CLI\{}{}_post.txt".format(router_ips,k), "w")

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

                write_path.write(new_string+"\n")
                new_list=[]
                new_string=""
            write_path.close()
            open_path.close()
            
        else:
            
            ssh.enable()
            post_output= open(r"DEFINE FILE PATH WHERE OUTPUT OF ALL CLIs WILL BE CAPTURED\{}_post_output.txt".format(router_ips), "a")
            write_path= open(r"DEFINE FILE PATH TO CAPTURE PARSED OUTPUT OF ANY VARIENT 'SHOW IP ROUTE' CLI\{}{}_post.txt".format(router_ips,k), "w")    
            rest_commands=ssh.send_command(k,read_timeout=20)
            write_path.write("\n"+ k + "\n" + rest_commands + "\n")
            post_output.write("\n"+ k + "\n" + rest_commands + "\n")
        

        write_path.close()



        pre_migration_1= open(r"DEFINE FILE PATH TO TEMPORARY CAPTURE OUTPUT SHOW CLIs BEFORE THE CHANGE\{}{}_pre.txt".format(router_ips,k), "r")
        post_migration_1=open(r"DEFINE FILE PATH TO TEMPORARY CAPTURE OUTPUT SHOW CLIs AFTER THE CHANGE\{}{}_post.txt".format(router_ips,k), "r")
        
        
        pre_migration= pre_migration_1.readlines()
        pre_migration = [x.strip() for x in pre_migration]
        pre_migration=list(pre_migration)
        
        post_migration= post_migration_1.readlines()
        post_migration = [x.strip() for x in post_migration]
        post_migration=list(post_migration)
        
             
        print("\n\n"+k)

        diff_migration_1.write("\n"+k+"\n\n<-------New Config------->\n")

        for element in post_migration:

                if element not in pre_migration:
                    
                        diff_migration_1.write("\n"+element+ "\n")
                        print(element)
                        print("\n")
        
        diff_migration_1.write("\n"+"<-------Deleted Config------->\n")

        for element in pre_migration:

                if element not in post_migration:

                        diff_migration_1.write("\n"+element+ "\n")
                        print(element)
                        print("\n")
        diff_migration_1.write("\n---------------------------End of Command output-------------------------------------\n")

sdwan_router_ips.close()
pre_migration_1.close()
post_migration_1.close()
diff_migration_1.close()

shutil.rmtree(r"DEFINE THE PATH OF TEMPORARY FOLDER WHICH WILL HOLD PRE AND POST MIGRATION OUTPUTs")

