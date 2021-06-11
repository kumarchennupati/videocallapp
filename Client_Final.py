#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket
import cv2
import pickle
import struct 
import threading

s=socket.socket()
serverip="4.tcp.ngrok.io"
serverport=13255
s.connect((serverip,serverport))


# In[2]:


def send(s,serverip):
    connection = s.makefile('wb')
    cam = cv2.VideoCapture("http://192.168.1.2:8080/video")
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    while True:
        ret, frame = cam.read()
        frame=cv2.resize(frame,(900,600))
        result, frame = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)
        s.sendall(struct.pack(">L", size) + data)
    cam.release()


# In[3]:


def receive(s,serverip):
    data = b""
    payload_size = struct.calcsize(">L")
    while True:
        while len(data) < payload_size:
            data += s.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += s.recv(4096)
            
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        cv2.imshow('ImageWindow',frame)
        if cv2.waitKey(1) == 27:
            break
    cv2.destroyAllWindows()


# In[4]:


t1=threading.Thread(target=receive,args=(s,serverip))
t2=threading.Thread(target=send,args=(s,serverip))
t2.start()
t1.start()


# In[ ]:





# In[ ]:




