printDebug = True

def sendData(socket, message):
  if printDebug:
    print('\n\nSending the following message:')
    print('message length =', len(message))
    print('--------------------------------------------------------------------------------')
    print(message, end='\n\n')
  socket.send(message.encode('utf-8'))
  '''
  # iterate through the entire size of the string
  while true:
    # if the message is less than 512 just send it
    if len(message) < 512:
      socket.send(message.encode('utf-8')
      break
    # if its not, sed substring and delete the substring from message
    else:
      submess = message[0:512]
      socket.send(submess.encode('utf-8'))
      # remove substring from message
      message.replace(submess, '', 1)
  '''
# reading all of the data from the socket
def readData(socket):
  # keeps track of the entire packet contents
  message = ''
  # keeps track of the total message size
  recvd = 0

  while True:
    # recieves a message of size 512
    submess = socket.recv(512).decode('utf-8')
    # appends the message to packet
    message += submess
    # appends the size of the message recieved
    recvd += len(submess)
    # if the message size is less than 512 break
    if len(submess) < 512:
        break
  if printDebug:
    print('\n\nRecieved the following message:')
    print('message length =', recvd)
    print('--------------------------------------------------------------------------------')
    print(message, end='\n\n')
  return message
