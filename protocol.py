import threading
from game import *
from helpers import *
from socket import *

games = Games()
host = ''
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, serverPort))
serverSocket.listen(1)

def main():
  print('Server running...\n')
  while True:
    connection, addr = serverSocket.accept()
    clientData = connection.recv(512)
    action, data = decodeAction(clientData)

    if action == 'register':
      print(f'Registered {data}')
      player = {
        'name': data,
        'connection': connection,
      }
      game = games.registerPlayer(player)
      if len(game.getPlayers()) > 1:
        x = threading.Thread(target=game.onGameStart)
        x.start()
        continue

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(e)
    serverSocket.close()
