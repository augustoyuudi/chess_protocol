import chess

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
