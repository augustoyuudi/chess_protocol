from socket import *
from helpers import *

serverName='127.0.0.1'
serverPort= 12345
client = socket(AF_INET, SOCK_STREAM)
client.connect((serverName, serverPort))
client.send(encodeAction('register', 'player1'))

while True:
  serverData, addr = client.recvfrom(1024)
  action, data = decodeAction(serverData)

  if action == 'wait':
    print('Wait opponent move:\n')
    continue

  if action == 'move':
    move = input("Move: ")
    client.send(encodeAction('move', move))

  if action == 'print':
    print(data)
    print('\n')
    client.send(encodeAction('print'))

  if action == 'end':
    print(data)
    client.shutdown(SHUT_RDWR)
    client.close()
    break
