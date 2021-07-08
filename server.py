import socket
# import base64
import struct
HOST = '127.0.0.1'
PORT_recv = 8000
PORT_send = 8080

def recv_msg(sock_recv, sock_send):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock_recv, sock_send, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    # return recvall(sock_recv, sock_send, msglen)
    recvall(sock_recv, sock_send, msglen)

def recvall(sock_recv, sock_send, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock_recv.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
        sock_send.sendall(packet)
    return data

serv_send = socket.socket()
serv_send.bind((HOST, PORT_send))
serv_send.listen(1)
serv_recv = socket.socket()
serv_recv.bind((HOST, PORT_recv))
serv_recv.listen(1)
print('server is waiting for connect')
while True:
    con_socket_recv, con_address_recv = serv_recv.accept()
    print('connect success for recv')
    con_socket_send, con_address_send = serv_send.accept()
    print('connect success for send')
    while True:
        # data = recv_msg(con_socket_recv)
        # send_msg(con_socket_send, data)
        # send_msg(con_socket_send, recv_msg(con_socket_recv))
        recv_msg(con_socket_recv, con_socket_send)