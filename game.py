import chess
import random
import sys
from helpers import encodeAction, decodeAction
# f2f3 e7e5 g2g4 d8h4

class Game:
  players = ()
  board = None

  def __init__(self, player):
    self.players = (player,)
    self.board = chess.Board()

  def setNewPlayer(self, player):
    self.players += (player,)

  def getPlayers(self):
    return self.players

  def getConnection(self, player):
    return self.players[player]['connection']

  def getBoard(self):
    return self.board

class Games:
  games = []

  def newGame(self, player):
    game = Game(player, )
    self.games.append(game)
    return game

  def getEmptyGame(self):
    for game in self.games:
      if len(game.getPlayers()) <= 1:
        return game
    return None

  def registerPlayer(self, player):
    game = self.getEmptyGame()
    if game == None:
      return self.newGame(player)
    game.setNewPlayer(player)
    return game

def onGameStart(game: Game):
  turn = random.randint(0, 1)
  nonTurn = abs(turn - 1)
  board = game.getBoard()

  while True:
    try:
      turnConnection = game.getConnection(turn)
      nonTurnConnection = game.getConnection(nonTurn)
      turnConnection.send(encodeAction('move'))
      nonTurnConnection.send(encodeAction('wait'))

      turnData = turnConnection.recv(512)
      turnAction, turnMove = decodeAction(turnData)
      move = chess.Move.from_uci(turnMove)

      if move in board.legal_moves:
        board.push(move)
        turnConnection.send(encodeAction('print', board.unicode(invert_color = True)))
        nonTurnConnection.send(encodeAction('print', board.mirror().unicode()))
        turnConnection.recv(32)
        nonTurnConnection.recv(32)

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
        turnConnection.send(encodeAction('print', 'Movimento inválido. Tente novamente.'))
        nonTurnConnection.send(encodeAction('wait'))
        turnConnection.recv(32)

    except Exception as e:
      if 'is not in list' in e.args[0]:
        turnConnection.send(encodeAction('print', 'Movimento inválido. Tente novamente.'))
        nonTurnConnection.send(encodeAction('wait'))
        turnConnection.recv(32)
