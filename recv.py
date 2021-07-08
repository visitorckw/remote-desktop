import pygame
import time
import sys
from pygame.locals import QUIT
import socket
# import base64
import struct
HOST = '127.0.0.1'
PORT = 8080

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

serv = socket.socket()
serv.connect((HOST, PORT))
print('connect to server')

# screen = pygame.display.set_mode((1196,790),0,32)   #窗口大小
screen = pygame.display.set_mode((960,540))
while True:   #循环刷新
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit() 
    data = recv_msg(serv)

    f = open('save.png', 'wb')
    f.write(data)
    f.close()
    background = pygame.image.load(r"save.png")  #圖片位置
    screen.blit(background,(0,0))  #對齊的座標
    pygame.display.update()   #顯示內容