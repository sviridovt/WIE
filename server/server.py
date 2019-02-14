import socket

HOST = '127.0.0.1'
PORT = 4444
certificate = 'starbucks '

# init socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind to the host and the port
s.bind((HOST, PORT))

# setting a back long for data size
s.listen()

# accepting incomming connection
conn, addr = s.accept()

# printing connected address
print('Connected by', addr)

# reading all of the data from the socket
def readData(conn):
        data = conn.recv(1024).decode('utf-8')
        if not data:
                conn.close()
                raise ValueError()
        return data

# if data is read, print
print('Recieved', readData(conn))

# send certificate
conn.send(certificate.encode('utf-8'))

# read if acknowledged
print('Recieved', readData(conn))

while True:
        data = conn.recv(1024).decode('utf-8')
        if not data: break
        print('Recieved', data)
        conn.send(data)




conn.close()
