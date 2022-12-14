import socket
import threading
import sys
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
from colorama import Fore, Style
import random

colors = list(vars(Fore).values())
myColor = random.choice(colors)


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

key = RSA.generate(2048)
private_key = RSA.import_key(key.exportKey())  # READY
public_key = key.publickey().exportKey()
cipher_rsa = PKCS1_OAEP.new(private_key)

# hash_object = hashlib.sha1(public_key)
# hex_digest = hash_object.hexdigest()

name = sys.argv[3]
port = sys.argv[2]
address = sys.argv[1]
sock.connect((address, int(port)))

sent = False
session_key = ""
nonce = ''


def enc_aes_data(data, session_key, nonce=nonce):
  #   print(f""" ENCRYPTION : Data = {data}
                # Session Key = {session_key}""")
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    # print(f"NONCE = {cipher_aes.nonce}")
    encData = cipher_aes.encrypt(bytes(data, 'utf-8'))
    # print("ENCRYPTED DATA :", cipher_aes.encrypt(bytes(data, 'utf-8')))
    return encData


def dec_aes_data(data, session_key, nonce):
  #   print(f""" DECRYPTION : Data = {data}
                # Session Key = {session_key}
                # Nonce = {nonce}""")

    d_cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    return d_cipher_aes.decrypt(data)


def sendMsg():
    while True:
        global sent
        global session_key
        global nonce
        if not sent:
            print("[ ] Sending The Public Key ...")
            sock.send(public_key)
            print("[X] Sent!")
            # confirm = sock.recv(1024)
            sent = True
            print("[ ] Receiving Session Key ...")
            sk = sock.recv(256)
            print("[X] Received!")
            # print("ENCRYPTED SESSION KEY", sk)
            nonce = sock.recv(256)
            session_key = cipher_rsa.decrypt(sk)
            # print(session_key)
            # print(nonce)

            continue
        data = '> ' + myColor + \
            name + '\033[0m' + ': ' + input("")
        enc_data = enc_aes_data(data, session_key, nonce)
        sock.send(enc_data)


iThread = threading.Thread(target=sendMsg)
iThread.daemon = True
iThread.start()
#################################################


# sock.send(public_key)
while True:
    if session_key:
        data = sock.recv(1024)
        data = dec_aes_data(data, session_key, nonce)

        if not data:
            break
        print(data.decode("utf-8"))
