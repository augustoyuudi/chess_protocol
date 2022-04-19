import random
import threading
import sys
from game import *
from helpers import *
from socket import *

# f3 e5 g4 Qh4

games = Games()
host = '127.0.0.1'
serverPort = 12345
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((host, serverPort))
serverSocket.listen(1)

def main():
  def onGameStart(game: Game):
    turn = random.randint(0, 1)
    nonTurn = abs(turn - 1)
    board = game.getBoard()

    while True:
      turnConnection = game.getConnection(turn)
      nonTurnConnection = game.getConnection(nonTurn)
      turnConnection.send(encodeAction('move'))
      nonTurnConnection.send(encodeAction('wait'))

      turnData = turnConnection.recv(1024)
      _, turnMove = decodeAction(turnData)
      parsedMove = board.parse_san(turnMove)

      if parsedMove in board.legal_moves:
        board.push_san(turnMove)
        turnConnection.send(encodeAction('print', board.unicode(invert_color = True)))
        nonTurnConnection.send(encodeAction('print', board.mirror().unicode()))
        turnConnection.recv(8)
        nonTurnConnection.recv(8)

        if board.outcome():
          winner = board.outcome().winner
          if winner == None:
            sendData = encodeAction('end', 'Draw')
          else:
            sendData = encodeAction('end', f'{"White" if winner else "Black"} wins')
          turnConnection.send(sendData)
          nonTurnConnection.send(sendData)
          # clear game
          sys.exit()

        turn, nonTurn = nonTurn, turn
      else:
        # TODO wait for valid move
        pass


  while True:
    connection, addr = serverSocket.accept()
    clientData = connection.recv(1024)
    action, data = decodeAction(clientData)

    print(action)

    if action == 'register':
      player = {
        'name': data,
        'connection': connection,
      }
      game = games.registerPlayer(player)
      if len(game.getPlayers()) > 1:
        x = threading.Thread(target=onGameStart, args=(game,))
        x.start()
        continue

if __name__ == "__main__":
  try:
    main()
  except Exception as e:
    print(e)
    serverSocket.close()
