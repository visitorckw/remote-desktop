import socket
import struct
import time
import cv2
HOST = '127.0.0.1'
PORT = 8000

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

import win32gui, win32ui, win32con, win32api
def window_capture(filename):
    hwnd = 0 # 視窗的編號，0號表示當前活躍視窗
    # 根據視窗控制代碼獲取視窗的裝置上下文DC（Divice Context）
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 根據視窗的DC獲取mfcDC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # mfcDC建立可相容的DC
    saveDC = mfcDC.CreateCompatibleDC()
    # 建立bigmap準備儲存圖片
    saveBitMap = win32ui.CreateBitmap()
    # 獲取監控器資訊
    MoniterDev = win32api.EnumDisplayMonitors(None, None)
    w = MoniterDev[0][2][2]
    h = MoniterDev[0][2][3]
    w = 1920
    h = 1080 #螢幕大小問題
    # print w,h　　　#圖片大小
    # 為bitmap開闢空間
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
    # 高度saveDC，將截圖儲存到saveBitmap中
    saveDC.SelectObject(saveBitMap)
    # 擷取從左上角（0，0）長寬為（w，h）的圖片
    saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)
    saveBitMap.SaveBitmapFile(saveDC, filename)
def resizePic(originFile, filename):
    pic = cv2.imread(originFile)
    pic = cv2.resize(pic, (960, 540), interpolation=cv2.INTER_CUBIC)
    cv2.imwrite(filename, pic)
def sendPic(filename):
    f = open(filename, 'rb')
    send_msg(sock, f.read())
    f.close()

sock = socket.socket()
sock.connect((HOST, PORT))
window_capture("screenshot.png")
while True:
    t = time.time()
    window_capture("screenshot.png")
    resizePic("screenshot.png", "screenshot2.png")
    sendPic('screenshot2.png')
    t = time.time() - t
    print(t)
