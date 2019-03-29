import socket
import json
import threading

class Client():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.connect(("localhost", 9999))
        self.usuarios = {"nombre": "", "identificacion": "", "telefono": "", "usuario": "", "password": "", "tipo": ""}
        self.datos = {"usuario": "", "pass": ""}

        self.iniciar_sesion()

        while True:
            res = input(">> ")
            self.sock.send(res.encode())
            
            msj = self.sock.recv(1024)
            print(msj.decode())

            if msj.decode() == "1":
                for i in self.usuarios:
                    res = input(">> ")
                    self.usuarios[i] = res

                data = json.dumps(self.usuarios)
                self.sock.send(data.encode())


    def iniciar_sesion(self):
        msj = self.sock.recv(1024)
        print(msj.decode())

        for i in self.datos:
            res = input(">> ")
            self.datos[i] = res

        data = json.dumps(self.datos)
        self.sock.send(data.encode())

client = Client()
