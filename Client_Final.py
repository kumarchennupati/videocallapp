import socket
import sys
import cv2
import pickle
import numpy as np
import struct
import zlib
import io
import time
import threading



def send(s,serverip):
    connection = s.makefile('wb')
    cam = cv2.VideoCapture(0)

    cam.set(3, 320);
    cam.set(4, 240);

    img_counter = 0


    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    while True:
        ret, frame = cam.read()
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        #    data = zlib.compress(pickle.dumps(frame, 0))
        data = pickle.dumps(frame, 0)
        size = len(data)


        print("{}: {}".format(img_counter, size))
        s.sendall(struct.pack(">L", size) + data)
        img_counter += 1

    cam.release()



def receive(s,serverip):
    data = b""
    payload_size = struct.calcsize(">L")
    print("payload_size: {}".format(payload_size))
    while True:
        while len(data) < payload_size:
            print("Recv: {}".format(len(data)))
            data += s.recv(4096)

        print("Done Recv: {}".format(len(data)))
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        print("msg_size: {}".format(msg_size))
        while len(data) < msg_size:
            data += s.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow',frame)
        cv2.waitKey(1)


import socket
s=socket.socket()
serverip="192.168.1.7"
serverport=2222
s.connect((serverip,serverport))
t1=threading.Thread(target=receive,args=(s,serverip))
t2=threading.Thread(target=send,args=(s,serverip))
t2.start()
t1.start()





