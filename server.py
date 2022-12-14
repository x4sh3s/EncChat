import socket
import threading
import sys
from time import sleep
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP


IP= sys.argv[1]
PORT= sys.argv[2]
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connections = []
# sock.bind((socket.gethostbyname(''), 10005))
sock.bind((IP, int(PORT)))

print(socket.gethostbyname(''))
sock.listen(1)

session_key = get_random_bytes(16)
cipher_aes = AES.new(session_key, AES.MODE_EAX)
getpk = ""


def dec_aes_data(data, session_key, nonce):
    d_cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    return d_cipher_aes.decrypt(data)


def handler(c, a):
    getpbk = c.recv(2048)
    print(getpbk)
    server_public_key = RSA.importKey(getpbk)
    cipher_rsa = PKCS1_OAEP.new(server_public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)
    sleep(1)
    if getpbk:
        # c.send("YES".encode("utf-8"))
        sleep(1)
        c.send(enc_session_key)
        c.send(cipher_aes.nonce)
    while True:
        data = c.recv(1024)
        # print(dec_aes_data(data, session_key, cipher_aes.nonce).decode())
        decodedD = dec_aes_data(data, session_key, cipher_aes.nonce).decode()
        print("DECODED D:", decodedD)
        if decodedD.split()[-1] == "Bye":
            print("GoodBye!")
            print(str(a[0]) + ':' + str(a[1]), "disconnected")
            connections.remove(c)
            c.close()
            break
        for connection in connections:
            if connection != c:
                connection.send(data)
        if not data:
            print(str(a[0]) + ':' + str(a[1]), "disconnected")
            connections.remove(c)
            c.close()
            break


def run():

    while True:
        c, a = sock.accept()
        cThread = threading.Thread(target=handler, args=(c, a))
        cThread.daemon = True
        cThread.start()
        connections.append(c)
        print(str(a[0]) + ':' + str(a[1]), "connected")


run()
