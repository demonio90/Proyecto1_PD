import socket
import threading
from itertools import count

import mysql.connector
import json

from mysql.connector import cursor


class Server():
    def __init__(self):
        self.sock = socket.socket()
        self.sock.bind(("localhost", 9999))
        self.sock.listen(1)
        self.conec = mysql.connector.connect(host="localhost", user="root", passwd="1112771855", database="supermercado")
        self.cursor = self.conec.cursor()

        self.conexion, direccion = self.sock.accept()

        self.iniciar_sesion()

        while True:
            msj = self.conexion.recv(1024)
            self.data = json.loads(msj.decode())

            if len(self.data) == 6:
                self.guardar_datos()
                self.conexion.send("\nUsuario creado con exito\n".encode())

            try:
                if len(self.validar_usuario()) > 0:
                    self.conexion.send(str("\nBienvenido "+self.data["usuario"]+"\n\n"+
                                           "1. Crear usuarios.\n"+
                                           "2. Ver clientes.\n"+
                                           "3. Ver ventas.\n"+
                                           "0. Cerrar sesion.\n").encode())

                    msj = self.conexion.recv(1024)
                    opcion = msj.decode()

                    if opcion == "1":
                        self.crear_usuario()

                else:
                    self.conexion.send("\nUsuario y/o contraseña incorrecto\n".encode())
            except:
                pass


    def iniciar_sesion(self):
        mensaje = "\n.::Iniciar sesión::.\n"
        self.conexion.send(mensaje.encode())

    def crear_usuario(self):
        self.conexion.send("1".encode())

    def guardar_datos(self):
        query = "insert into usuarios(nombre, identificacion, telefono, usuario, password, tipo) values(%s, %s, %s, %s, %s, %s)"
        self.cursor.execute(query, (self.data["nombre"], self.data["identificacion"], self.data["telefono"], self.data["usuario"], self.data["password"], self.data["tipo"]))
        self.conec.commit()

    def validar_usuario(self):
        query = "select id from usuarios where usuario = %s and password = %s"
        self.cursor.execute(query, (self.data["usuario"], self.data["pass"]))
        result = self.cursor.fetchall()

        return result

server = Server()