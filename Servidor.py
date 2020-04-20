from socket import *
from _thread import *
import time
import sys
import mysql.connector

#funciones de mysql
dbConnect = {
    'host':'127.0.0.1',
    'user':'root',
    'password':'1234',
    'database':'python'
}

def guardar(mensaje,emisor):
    conexion = mysql.connector.connect(**dbConnect)
    cursor = conexion.cursor()
    sql = "insert into mensajes(mensaje,envio,fecharegistro)values(%s,%s,now())"
    cursor.execute(sql,(mensaje,emisor))
    conexion.commit()
    cursor.close()
    conexion.close()


#funciones
def ini():
    host = input("IP de host: ")
    port = int(input("Puerto: "))
    return host, port

def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def ligarSocket(s, host, port):
    while True:
        try:
            s.bind((host, port))
            break
        except error as e:
            print("ERROR:", e)

def conexiones(s):
    conn, addr = s.accept()
    print("\nConexion establecida.\nEl cliente es:", addr[0] + ":" + str(addr[1])+"\n")
    return conn, addr

def enviar(conn):
        msg = input("")
        mensaje = msg
        msg = "Servidor: " + msg
        try:
            conn.send(msg.encode("UTF-8"))
            guardar(mensaje,"servidor")
        except:
            print("\nHubo un error")
            print("Tratando de nuevo en 5 segundos\n")
            time.sleep(5)

def enviar2(conn):
        msg = input("")
        mensaje = msg
        msg = "Servidor: " + msg
        try:
            conn.send(msg.encode("UTF-8"))
            guardar(mensaje,"servidor")
        except:
            print("\nHubo un error")
            print("Tratando de nuevo en 5 segundos\n")
            time.sleep(5)

def recibir(conn):
    while True:
        global bandera
        try:
            reply = conn.recv(2048)
            reply = reply.decode("UTF-8")
            if reply[0] == "1":
                print("Cliente ", reply)
                guardar(reply,"Cliente 1")
                start_new_thread(enviar, (conn,))
            elif reply[0] == "2":
                print("Cliente ", reply)
                guardar(reply,"Cliente 2")
                start_new_thread(enviar2, (conn,))
            else:
                lista_de_clientes.append(reply[3])
                print("\nEl cliente "+reply[3]+" se desconecto")
                bandera = True
                break
        except:
            print("\nNo se puede recibir una respuesta")
            print("Tratando de nuevo en 5 segundos\n")
            time.sleep(5)


def enviarEspecial(conn):
    global lista_de_clientes,client
    client = lista_de_clientes.pop()
    conn.send(client.encode("UTF-8"))

#variables globales

bandera = False      # Utilizada en la desconexion/conexion de clientes

lista_de_clientes = ["2","1"]   # El servidor le asigna un numero a los
                                # clientes segun esta lista

client = ""     # Numero del cliente

#main

def main():

    global bandera
    host,port = ini()
    s = crearSocket()
    ligarSocket(s, host,port)
    s.listen(2)     # Espero 2 clientes

    print("\nAdvertencia:No escribir en el servidor al menos que haya una"
        "peticion recibida, ya que esta se acumulara y podra provocar un error")
    print("\nEsperando clientes")

    conn,addr = conexiones(s)
    enviarEspecial(conn)               # Espero conexion del 1 cliente
    start_new_thread(recibir,(conn,))

    conn2,addr2 = conexiones(s)
    enviarEspecial(conn2)              # Espero conexion del 2 cliente
    start_new_thread(recibir,(conn2,))

    while True: # Necesario para que los hilos no mueran

        if bandera != True:     # En caso de desconectarse un cliente,
                                # esperara a que otro vuelve a conectarse
            conn3,addr3 = conexiones(s)
            enviarEspecial(conn3)
            start_new_thread(recibir,(conn3,))
            bandera = False


main()
