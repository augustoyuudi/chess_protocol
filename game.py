import chess
import random
import sys
from helpers import encodeAction, decodeAction
# f2f3 e7e5 g2g4 d8h4

class Game:
  players = ()
  board = None
  id = None
  starter = None

  def __init__(self, player, id):
    self.players = (player,)
    self.board = chess.Board()
    self.id = id
    self.defineStartingPlayer()

  def setNewPlayer(self, player):
    self.players += (player,)

  def getPlayers(self):
    return self.players

  def getConnection(self, player):
    return self.players[player]['connection']

  def getBoard(self):
    return self.board

  def getId(self):
    return self.id

  def defineStartingPlayer(self):
    self.starter = random.randint(0, 1)

  def getPlayersTurn(self):
    nonTurn = abs(self.starter - 1)
    return self.starter, nonTurn

  def getTurnBoards(self, turn):
    turnBoard = self.board.unicode()
    nonTurnBoard = self.board.mirror().unicode()

    if turn != self.starter:
      turnBoard, nonTurnBoard = nonTurnBoard, turnBoard

    return turnBoard, nonTurnBoard

  def handleGameOutcome(self, turn, nonTurn):
    turnConnection = self.getConnection(turn)
    nonTurnConnection = self.getConnection(nonTurn)

    if self.board.outcome().winner == None:
      sendData = encodeAction('end', 'Draw')
      turnConnection.send(sendData)
      nonTurnConnection.send(sendData)
    else:
      turnConnection.send(encodeAction('end', 'You win'))
      nonTurnConnection.send(encodeAction('end', 'You lose'))

  def onGameStart(self):
    print(f'Game #{self.getId()} started.\n')
    turn, nonTurn = self.getPlayersTurn()
    board = self.getBoard()

    while True:
      try:
        turnConnection = self.getConnection(turn)
        nonTurnConnection = self.getConnection(nonTurn)
        turnConnection.send(encodeAction('move'))
        nonTurnConnection.send(encodeAction('wait'))

        turnData = turnConnection.recv(512)
        turnAction, turnMove = decodeAction(turnData)
        move = chess.Move.from_uci(turnMove)

        if move in board.legal_moves:
          board.push(move)
          turnBoard, nonTurnBoard = self.getTurnBoards(turn)
          turnConnection.send(encodeAction('print', turnBoard))
          nonTurnConnection.send(encodeAction('print', nonTurnBoard))
          turnConnection.recv(32)
          nonTurnConnection.recv(32)

          if board.outcome():
            self.handleGameOutcome(turn, nonTurn)
            print(f'Game #{self.getId()} ended.\n')
            sys.exit()

          turn, nonTurn = nonTurn, turn
        else:
          turnConnection.send(encodeAction('print', 'Invalid move. Try again.'))
          nonTurnConnection.send(encodeAction('wait'))
          turnConnection.recv(32)

      except Exception as e:
        if 'is not in list' in e.args[0]:
          turnConnection.send(encodeAction('print', 'Invalid move. Try again.'))
          nonTurnConnection.send(encodeAction('wait'))
          turnConnection.recv(32)

class Games:
  games = []

  def newGame(self, player):
    gameId = len(self.games) + 1
    game = Game(player, gameId)
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
