import socket
import sys

def receive_from(ip,port,filename):
	print("Requesting",filename,"from",ip,"on port",port)
	try:
		server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server.connect((ip,port))
	except:
		print("Could not connect.")
		return
	print("Receiving file...")
	out_f = open(filename,"wb")
	try:
		data = server.recv(1024*1024*50)
		while len(data):
			out_f.write(data)
			data = server.recv(1024*1024*50)
	except:
		print("Something went wrong")
	out_f.close()
	print("File transfer complete")

def send_to(ip,port,filename):
	print("Attempting to share",filename,"on",ip+":"+str(port))
	try:
		server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		server.bind((ip,port))
		server.listen(1)
	except:
		print("Could not bind to the specified address.")
		return
	print("Waiting for receiver on",ip+":"+str(port))
	client,addr = server.accept()
	print("Got connection from",str(addr))
	try:
		send_f = open(filename,"rb")
	except:
		print("Could not open",filename)
		print("Aborting")
		return
	try:
		print("Sending file...")
		client.send(send_f.read())
	except:
		print("Something went wrong")
	send_f.close()
	print("File transfer complete")

def menu():
	print("EasyShare V1.0.0\n")
	print("1) Send File")
	print("2) Receive File")
	option = int(input())
	if option == 1:
		send_to(input("Enter ip address to share on: "),int(input("Enter port to share on: ")),input("Enter filename(Full path or local file): ").strip())
	else:
		receive_from(input("Enter ip to receive from: "),int(input("Enter port to receive from: ")),input("Enter filename(Full path or local file): ").strip())
while 1:
	menu()