#coding:utf-8
import base64
import os
import time
print (base64.b32encode(os.urandom(20)))

print (time.strftime('%Y-%m-%d %H:%M:%S'))