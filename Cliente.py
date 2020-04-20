#cliente

from socket import *
import time
from _thread import *

#funciones
#obtener host y puerto
def ini():
    host = input("Direccion del server: ")
    port = int(input("Puerto del servidor: "))
    return host, port

def crearSocket():
    s = socket(AF_INET, SOCK_STREAM)
    return s

def conectarse (host, port, s):
    s.connect((host, port))

def intentoConexion(host, port, s):

        while True:
            print("\nIntentando conectar en el host: ", host + " de puerto " + str(port))
            try:
                conectarse(host, port, s)
                break
            except:
                print("No hay ningun host activo en", host + ":" + str(port))
                print("Intentando de nuevo en 5 segundos\n")
                time.sleep(5)

def enviar(s):

    while True:

        global exit

        try:
            msg = input("")
            msg = client +":" + msg
            if msg == client+":salir":
                exit = True
                msg = "el "+client+" se desconecto"
                s.send(msg.encode("UTF-8"))
                s.close
                break
            else:
                s.send(msg.encode("UTF-8"))
                start_new_thread(recibir,(s,))


        except:
            print("Hubo un error\n")
            print("Intentando en 5 segundos")
            time.sleep(5)

def recibir(s):
    while True:

        try:
          reply = s.recv(2048)
          print(reply.decode("UTF-8"))
          break


        except:
            print("No se puede recibir respuesta\n")
            print("Intentando en 5 segundos")
            time.sleep(5)

def recibirEspecial(s):
    global client
    client = s.recv(2048).decode("UTF-8")

#######################################################################
##                          VARIABLES GLOBALES                       ##
#######################################################################

exit=False      # Si el cliente envia salir, exit se pone en true y el
                # el programa termina
client = ""

#######################################################################
##                                MAIN                               ##
#######################################################################

def main():

    host, port = ini()
    s = crearSocket()
    intentoConexion(host,port,s)
    recibirEspecial(s)
    print("\nSe ha establecido la conexion al servidor ", host+":"+str(port)+"\n")
    print("Escribe tu mensaje, para salir solo escribe salir\n")
    start_new_thread(enviar,(s,))

    while exit!=True:   # Necesarios para que los hilos no mueran
        pass

    print("\nSe ha perdido la conexion al servidor")
    print("Cerrando la ventana en 10 segundos.")
    time.sleep(10)

main()


