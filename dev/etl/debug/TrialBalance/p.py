#!/home/bgroves@BUSCHE-CNC.COM/anaconda3/bin/python
import os

print('p - The message is:', os.environ['MESSAGE'])
os.environ["MESSAGE"] = "PYMESSAGE"
