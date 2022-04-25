import threading
from game import *
from helpers import *
from socket import *

games = Games()
host = '127.0.0.1'
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, serverPort))
serverSocket.listen(1)

def main():
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
        x = threading.Thread(target=onGameStart, args=(game, onGameEnd))
        x.start()
        continue

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(e)
    serverSocket.close()
