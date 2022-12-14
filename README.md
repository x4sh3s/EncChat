# EncChat
an encrypted server/client chat in python using RSA and AES.

### How to use it:

1. `git clone https://github.com/x4sh3s/EncChat`
2. `python -m pip install -r requirements.txt`
3. On the server side: `python server.py $IP $PORT`
4. On the client side: `python client.py $IP $PORT $name`

### How It Works?:

1. The server generate a random 16 bytes to use it as a symmetric aes key
2. The Client first generate a public/private key pair for RSA, and send it (the public key) to the server
3. The server encrypt the session key ( created in 1 ) with the user's public key
4. the user decrypt it with his private key
5. The communication is now encrypted with AES.

> Same with the other clients!


### Example:

![2022-12-14 11_18_26-EncChat mp4 - VLC media player](https://user-images.githubusercontent.com/65988560/207570361-1a03954f-3ce7-4370-9521-a46a4cdf4fb8.png)


### Demo: 

https://user-images.githubusercontent.com/65988560/207570608-abc6d815-30d0-4c14-a17c-d3a604efd3d0.mp4

