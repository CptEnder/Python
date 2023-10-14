"""
Created on Tue 14 Mar 16:30 2023
Finished on
@author: Cpt.Ender

Implemented:
Draw due to Insufficient material
Stalemate Draw
50-move Rule Draw
Check and Check Mate
Piece Pinning
enPassant
Correct Castling (not through attacks and when king is under check)
Pawn Promotions
HalfMove Counter
FullMove Counter
Show Previous Move
Save up to 8 Games
See the previous game
Pause Menu (Draw, Resign, back to Main Menu)

To Do:
Threefold repetition Draw
Player left
Player username
General clean up and makeover
Adding Sound
                                  """
import socket
import threading
import pygame


def create_thread(target):
    thread = threading.Thread(target=target)
    # thread.daemon = True
    thread.start()
    return thread


class Board:
    def __init__(self, name: str, winS: list):
        """
        A method for the initialization of a Board
        """
        pygame.init()
        self.gameS = winS
        self.square = [winS[0] / 8, winS[1] / 8]
        self.windowS = [self.gameS[0], self.gameS[1]]
        self.name = name
        pygame.display.set_caption(self.name)
        self.scrn = pygame.display.set_mode(self.windowS)
        pygame.mouse.set_visible(True)
        self.clock = pygame.time.Clock()

        self.threads = []
        self.user = ''

        self.playerServer = ''
        self.connectionEst = False
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host, self.port = '127.0.1.1', '1111'
        self.conn, self.addr = '', ''

        self.black = [0] * 3
        self.white = [255] * 3
        self.red = [255, 0, 0]
        self.orange = [255, 140, 0]
        self.green = [34, 139, 34]
        self.green2 = [118, 150, 86]
        self.white2 = [238, 238, 210]
        self.gray = [214, 214, 188]
        self.yellow = [247, 247, 106]
        self.path = 'Chess/Images/'

        self.font = pygame.font.Font('freesansbold.ttf', 28)
        self.font2 = pygame.font.Font('freesansbold.ttf', 15)
        self.keyPressed = ''
        self.pieces = self._loadSprites()
        self.buttons = self._createButtons()
        self.currentS = 1

        self.activeC = 'w'
        self.colorC = ''
        self.piecePl = ''
        self.castlingR = ''
        self.enPassant = ''
        self.halfMoveC = 0
        self.fullMoveC = 0
        self.moves = {'p': self._pawnMoves, 'n': self._nightMoves, 'b': self._bishopMoves,
                      'r': self._rookMoves, 'q': self._queenMoves, 'k': self._kingMoves}
        self.promotions = {'White': [[pygame.transform.scale(pygame.image.load(self.path + 'w' + p + '.png'),
                                                             [self.square[0] / 2, self.square[1] / 2]),
                                      pygame.Rect(self.square[0] * 4, i * self.square[1] / 2 + self.square[1],
                                                  self.square[1] / 2, self.square[1] / 2), p]
                                     for i, p in enumerate(['Q', 'B', 'N', 'R'])],
                           'Black': [[pygame.transform.scale(pygame.image.load(self.path + 'b' + p + '.png'),
                                                             [self.square[0] / 2, self.square[1] / 2]),
                                      pygame.Rect(self.square[0] * 4, i * self.square[1] / 2 + self.square[1],
                                                  self.square[1] / 2, self.square[1] / 2), p]
                                     for i, p in enumerate(['Q', 'B', 'N', 'R'])]}
        self.gameHistory = {i: {} for i in range(8)}
        self.gameNo = -1
        self.gameHiSelection = 0
        self.gameHiMove = 0
        self.gameHiColor = 'W'
        self.promotion = []
        self.pr = False
        self.move = []
        self.myPiecesPos = []
        self.myMoves = {}
        self.enemyPiecesPos = []
        self.enemyMoves = {}
        self.previousMove = ['--', '--']
        self.board = [['' for _ in range(8)] for __ in range(8)]
        self.selectedC = []
        self.checkedBy = []

        self.info = ['', self.black]

    def _createButtons(self):
        """
        Method for creating all the buttons and info blocks in the game
        :return: [[button, button rectangle, screen it is visible in]]
        """
        serverB = self.font.render('Create Lobby', True, self.black)
        serverB_rect = serverB.get_rect()
        serverB_rect.center = [self.gameS[0] // 2, self.gameS[1] // 4]

        clientB = self.font.render('Connect to Lobby', True, self.black)
        clientB_rect = clientB.get_rect()
        clientB_rect.center = [self.gameS[0] // 2, 2 * self.gameS[1] // 4]

        back = self.font.render('Back', True, self.black)
        back_rect = back.get_rect()
        back_rect.bottomleft = [0, self.gameS[1]]

        playAsB = self.font.render('Play As:', True, self.black)
        playAsB_rect = playAsB.get_rect()
        playAsB_rect.center = [self.gameS[0] // 2, 3 * self.gameS[1] // 5]

        portInput = self.font.render(str(self.port) + ' ', True, self.black)
        portInput_rect = portInput.get_rect()
        portInput_rect.center = [self.gameS[0] // 2, self.gameS[1] // 2]

        connectB = self.font.render('Connect', True, self.black)
        connectB_rect = connectB.get_rect()
        connectB_rect.center = [self.gameS[0] // 2, 3 * self.gameS[1] // 5]

        whiteB = self.pieces['wK']
        whiteB_rect = pygame.Rect(self.square[0] * 3, self.square[1] * 5, self.square[0], self.square[1])
        blackB = self.pieces['bK']
        blackB_rect = pygame.Rect(self.square[0] * 4, self.square[1] * 5, self.square[0], self.square[1])

        startB = self.font.render('Start', True, self.black)
        startB_rect = startB.get_rect()
        startB_rect.center = [self.gameS[0] // 2, 8 * self.gameS[1] // 10]

        pauseScreen = pygame.Surface((self.square[0] * 6, self.gameS[1]))
        pauseScreen.set_alpha(240)
        pauseScreen.fill(self.white)
        pauseScreen2 = pygame.Surface(self.gameS)
        pauseScreen2.set_alpha(150)
        pauseScreen2.fill(self.white)

        endScreenL1 = self.font.render('Check Mate', True, self.black)
        endScreenL1_rect = endScreenL1.get_rect()
        endScreenL1_rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]

        endScreenL2 = self.font.render("It's a Draw", True, self.black)
        endScreenL2_rect = endScreenL2.get_rect()
        endScreenL2_rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2 + self.square[0]]

        history = self.font.render("Game History", True, self.black)
        history_rect = history.get_rect()
        history_rect.center = [self.gameS[0] // 2, 3 * self.gameS[1] // 4]

        resignB = self.font.render("Resign", True, self.black, self.red)
        resignB_rect = resignB.get_rect()
        resignB_rect.center = [self.gameS[0] // 2, self.gameS[1] // 2]

        mainMenuB = self.font.render("Back to Main Menu", True, self.black, self.white2)
        mainMenuB_rect = mainMenuB.get_rect()
        mainMenuB_rect.center = [self.gameS[0] // 2, self.gameS[1] // 2 + self.square[1]]

        drawB = self.font.render("Draw", True, self.black, self.green)
        drawB_rect = drawB.get_rect()
        drawB_rect.center = [self.gameS[0] // 2, self.gameS[1] // 2 - self.square[1]]

        drawText = self.font.render("Enemy is offering a Draw", True, self.black)
        drawText_rect = drawText.get_rect()
        drawText_rect.center = [self.gameS[0] // 2, self.gameS[1] // 2 - self.square[1]]

        yesB = self.font.render("Accept", True, self.black, self.green)
        yesB_rect = yesB.get_rect()
        yesB_rect.center = [self.gameS[0] // 2 - self.square[0], self.gameS[1] // 2]

        noB = self.font.render("Reject", True, self.black, self.red)
        noB_rect = noB.get_rect()
        noB_rect.center = [self.gameS[0] // 2 + self.square[0], self.gameS[1] // 2]

        returnDict = {'pH': [back, back_rect, '-'], 'pauseScreen': [pauseScreen, (self.square[1], 0), '123689'],
                      'serverB': [serverB, serverB_rect, '1'], 'clientB': [clientB, clientB_rect, '1'],
                      'back': [back, back_rect, '236'], 'playAsB': [playAsB, playAsB_rect, '2'],
                      'portInput': [portInput, portInput_rect, '3'], 'connectB': [connectB, connectB_rect, '3'],
                      'whiteB': [whiteB, whiteB_rect, '2'], 'blackB': [blackB, blackB_rect, '2'],
                      'startB': [startB, startB_rect, '2'], 'pauseScreen2': [pauseScreen2, (0, 0), '5'],
                      'endScreenL2': [endScreenL2, endScreenL2_rect, '5'], 'gameH': [history, history_rect, '1'],
                      'resignB': [resignB, resignB_rect, '8'], 'mainMenuB': [mainMenuB, mainMenuB_rect, '8'],
                      'drawB': [drawB, drawB_rect, '8'], 'endScreenL1': [endScreenL1, endScreenL1_rect, '5'],
                      'yesB': [yesB, yesB_rect, '9'], 'noB': [noB, noB_rect, '9'],
                      'drawT': [drawText, drawText_rect, '9']}

        for i in range(8):
            gameNo = self.font.render("Game No." + str(i + 1), True, self.black)
            gameNo_rect = gameNo.get_rect()
            gameNo_rect.center = [self.gameS[0] // 2, self.square[1] * i + self.square[1] // 2]
            returnDict['gameNoButton' + str(i + 1)] = [gameNo, gameNo_rect, '-']

        return returnDict

    def _loadSprites(self):
        """
        Loads the png images for all the pieces
        :return: a dictionary of pieces and their images
        """
        pieces = {}
        for c in 'wb':
            for p in ['K', 'Q', 'B', 'N', 'R', 'P']:
                pieces[c + p] = (pygame.transform.scale(pygame.image.load(self.path + c + p + '.png'), self.square))
        return pieces

    def _loadFEN(self, fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0'):
        """
        Method to unpack any FEN given into the correct variables
        :param fen: current FEN position
        """
        [self.piecePl, self.activeC, self.castlingR, self.enPassant, halfMoveC, fullMoveC] = fen.split(
            ' ')[0:6]
        # self.piecePl = 'r1bk3r/p2pBpNp/n3Pn2/1p1NP2P/6P1/1p1P4/P1P1K3/q5b1'
        # fen='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0'
        # fen='r1bk3r/p2pBpNp/n3Pn2/1p1NP2P/6P1/1p1P4/P1P1K3/q5b1 w KQkq - 0 0'

        if self.colorC == 'Black':
            self.piecePl = self.piecePl[::-1]
        self.myPiecesPos = []
        self.enemyPiecesPos = []
        self.myMoves = {}
        self.enemyMoves = {}
        self.checkedBy = []
        self.board = [['' for _ in range(8)] for __ in range(8)]
        self.fullMoveC = int(fullMoveC)
        self.halfMoveC = int(halfMoveC)
        for i, row in enumerate(self.piecePl.split('/')):
            j = 0
            for p in row:
                if p in '12345678':
                    j += int(p)
                else:
                    self.board[i][j] = p
                    if [not p.isupper(), p.isupper()][self.colorC == 'White']:
                        self.myPiecesPos.append([j, i])
                    else:
                        self.enemyPiecesPos.append([j, i])
                    j += 1

        # All the enemies possible moves
        for j, i in self.enemyPiecesPos:
            p = self.board[i][j]
            temp = self.moves[p.lower()]([7 - j, 7 - i], [l[::-1] for l in self.board[::-1]])
            self.enemyMoves[p + str(i) + str(j)] = [[7 - a[0], 7 - a[1], a[2], a[3]] for a in temp]

        # Find if I am being checked
        for p in self.enemyMoves.keys():
            for m in self.enemyMoves[p]:
                if m[2] == 1 and self.board[m[1]][m[0]].lower() == 'k':
                    self.checkedBy.append([p, m])

        # All of my possible moves
        for j, i in self.myPiecesPos:
            p = self.board[i][j]
            if p.lower() == 'k':
                self.myKing = [i, j]
            self.myMoves[p + str(i) + str(j)] = self.moves[p.lower()]([j, i], self.board)

        # Remove all the illegal moves
        self._removeIllegalMoves()

    def _array2FEN(self):
        """
        Method to transform the board array into a string
        :return: the FEN string
        """
        fen = ''
        for row in self.board:
            i = 0
            for c in row:
                if c:
                    if i:
                        fen += str(i)
                    fen += c
                    i = 0
                else:
                    i += 1
            if i:
                fen += str(i)
            fen += '/'
        return fen[:-1]

    @staticmethod
    def _chessPos2arrInd(c, pos):
        return ['abcdefgh'[::{'W': 1, 'B': -1}[c]].index(pos[0]), '12345678'[::{'W': -1, 'B': 1}[c]].index(pos[1])]

    @staticmethod
    def _arrInd2ChessPos(c, indexes):
        return 'abcdefgh'[::{'W': 1, 'B': -1}[c]][indexes[0]] + '12345678'[::{'W': -1, 'B': 1}[c]][indexes[1]]

    def server(self):
        self.playerServer = 'Server'
        for port in range(1111, 2000):
            self.port = port
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.bind((self.host, self.port))
                self.sock.listen()
                print(port)
                try:
                    while self.playerServer:
                        conn, addr = self.sock.accept()
                        if not self.user:
                            self.conn, self.addr = conn, addr
                            self.conn.send(self.playerServer.encode())
                            self.user = self.conn.recv(1024).decode()
                            self.connectionEst = True
                            print(self.conn, self.addr)
                            print(f'Connection established with {self.addr} on port {self.port}')
                            self.info = [f'Connection established with {self.addr} on port {self.port}', self.green]
                        else:
                            conn.close()
                    # break
                except OSError as e:
                    print(e)
                    break
            except OSError:
                print(f"Port {port} already in use")
                self.info = [f"Port {port} already in use", self.orange]
        print(123)

    def client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(3)
        if self.port:
            port = int(self.port)
            if port < 65535:
                try:
                    try:
                        self.playerServer = 'Client'
                        self.sock.connect((self.host, int(port)))
                        self.user = self.sock.recv(1024).decode()
                        if self.user:
                            self.conn = self.sock
                            print(f'Connected on port {port}')
                            self.info = [f'Connected on port {port}', self.green]
                            self.sock.send(self.playerServer.encode())
                            self.connectionEst = True
                        else:
                            self.playerServer = ''
                            self.sock.close()
                            print('Connection not established')
                            self.info = ['Connection not established', self.red]
                    except ConnectionRefusedError as e:
                        print(e)
                        self.playerServer = ''
                        print(f'Port {port} is not in use')
                        self.info = [f'Port {port} is not in use', self.orange]
                except OSError as e:
                    self.playerServer = ''
                    print("Socket closed", e)
                    self.info = [f"Socket closed due to '{e}' error", self.red]
            else:
                print("Valid ports are 0 - 65535")
                self.info = ["Valid ports are 0 - 65535", self.red]
        else:
            print("Cant connect to empty port")
            self.info = ["Cant connect to empty port", self.red]
        print(234)

    def _closeConnections(self):
        """
        Method for closing all the connections and setting everything back to default
        """
        self.playerServer = ''
        self.connectionEst = False
        self.info[0] = ''
        self.conn = ''
        self.user = ''
        self.sock.close()

    def _gameInit(self):
        self.currentS = 4
        self.info[0] = ''
        self.piecePl = ''
        self.previousMove = ['--', '--']
        self.gameNo += 1
        self.gameHistory[self.gameNo % 8] = {0: 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0 ----'}
        self.buttons = self._createButtons()
        self.currentS = 4

    def logig(self):
        """
        Method for the logic of the board
        """
        mousePos = pygame.mouse.get_pos()
        message = 'Connection established'
        if self.currentS == 1:
            # Main Menu Screen
            self._closeConnections()
            self.colorC = ''
            if pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['serverB'][1].collidepoint(mousePos) \
                    and not self.playerServer:
                # Go to Create Lobby Screen and Start a server
                self.threads.append(create_thread(self.server))
                self.currentS = 2
                return
            elif pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['clientB'][1].collidepoint(mousePos) \
                    and not self.playerServer:
                # Got to Join Lobby Screen
                self.currentS = 3
                return
            elif pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['gameH'][1].collidepoint(mousePos) \
                    and not self.playerServer:
                self.currentS = 6
        elif self.currentS == 2:
            # Lobby Creation Screen
            if pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['whiteB'][1].collidepoint(mousePos) \
                    and self.colorC != 'White':
                self.colorC = 'White'
            elif pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['blackB'][1].collidepoint(mousePos) \
                    and self.colorC != 'Black':
                self.colorC = 'Black'
            elif pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['startB'][1].collidepoint(mousePos) \
                    and self.colorC and self.conn:
                # Start Button pressed
                self._gameInit()
                message = self.colorC
        elif self.currentS == 3:
            # Connect to Lobby Screen
            self.port = str(self.port)
            if self.keyPressed and self.keyPressed in '1234567890':
                self.port += self.keyPressed
            self.buttons['portInput'][0] = self.font.render(self.port + ' ', True, self.black)
            portInput_rect = self.buttons['portInput'][0].get_rect()
            portInput_rect.center = [self.gameS[0] // 2, self.gameS[1] // 2]
            self.buttons['portInput'][1] = portInput_rect

            if pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['connectB'][1].collidepoint(mousePos) \
                    and not self.playerServer:
                # Pressing the Connect Button
                print('Trying to Connect to port ' + self.port)
                self.info = ['Trying to Connect to port ' + self.port, self.black]
                self.threads.append(create_thread(self.client))
                return
        elif self.currentS == 4:
            # Game Screen
            if not self.piecePl:
                self._loadFEN()
            self._checkPosition()
            if self.activeC == self.colorC[0].lower():
                self._chessLogig(mousePos)
                message = self.piecePl
                # print(self.piecePl)
                if self.colorC == 'Black':
                    message = self.piecePl[::-1]
                message += ' '.join(['', self.activeC, self.castlingR, self.enPassant,
                                     str(self.halfMoveC), str(self.fullMoveC),
                                     self.previousMove[0] + self.previousMove[1]])
                self.gameHistory[self.gameNo][
                    [self.fullMoveC * 2 + 1, self.fullMoveC * 2][self.activeC == 'w']] = message
        elif self.currentS == 5:
            # Game Ended Screen
            if not any(self.myMoves.values()):
                message = 't'
                if self.checkedBy:
                    message = 'm'
        elif self.currentS == 6:
            # Game History Gallery Screen
            for i in range(7):
                if self.gameHistory[i]:
                    self.buttons['gameNoButton' + str(i + 1)][2] = '6'
                    if pygame.mouse.get_pressed(3) == (1, 0, 0) and \
                            self.buttons['gameNoButton' + str(i + 1)][1].collidepoint(mousePos):
                        self.currentS = 7
                        self.gameHiSelection = i
        elif self.currentS == 8:
            # Pause Menu Screen
            if pygame.mouse.get_pressed(3) == (1, 0, 0):
                if self.buttons['resignB'][1].collidepoint(mousePos) or \
                        self.buttons['mainMenuB'][1].collidepoint(mousePos):
                    self.buttons['endScreenL1'][0] = self.font.render('You Resigned', True, self.black)
                    rect = self.buttons['endScreenL1'][0].get_rect()
                    rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]
                    self.buttons['endScreenL1'][1] = rect
                    self.buttons['endScreenL2'][0] = self.font.render(
                        ['Black', 'White'][self.colorC == 'Black'] + ' won',
                        True, self.black)
                    rect = self.buttons['endScreenL2'][0].get_rect()
                    rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2 + + self.square[0]]
                    self.buttons['endScreenL2'][1] = rect
                    self.currentS = 5
                    if self.buttons['mainMenuB'][1].collidepoint(mousePos):
                        self.currentS = 1
                    message = 'r'
                elif self.buttons['drawB'][1].collidepoint(mousePos):
                    message = 'q'
        elif self.currentS == 9:
            if pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['yesB'][1].collidepoint(mousePos):
                self.buttons['endScreenL1'][0] = self.font.render("", True, self.black)
                self.currentS = 5
                message = 'd'
            if pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['noB'][1].collidepoint(mousePos):
                self.currentS = 4
                message = 'n'

        if str(self.currentS) in '236':
            # Pressing the BACK Button
            if pygame.mouse.get_pressed(3) == (1, 0, 0) and self.buttons['back'][1].collidepoint(mousePos):
                self.currentS = 1
                return

        if self.playerServer and self.conn:
            try:
                self.connectionEst = True
                self.conn.send(message.encode())
                data = self.conn.recv(1024).decode()
                # print(data)
                if data and data in 'WhiteBlack' and not self.colorC:
                    self.colorC = ['Black' if data == 'White' else 'White'][0]
                    print(self.colorC)
                    self._gameInit()
                elif data and self.currentS == 4 and '/' in data:
                    self._loadFEN(data[:-5])
                    self.previousMove = [data[-4:-2], data[-2:]]
                elif data and self.currentS in range(4, 10, 1) and data in 'mqdtrn':
                    print(data)
                    # Game has ended
                    if data == 't':
                        # StaleMate
                        self.buttons['endScreenL1'][0] = self.font.render('StaleMate, enemy has no legal moves', True,
                                                                          self.black)
                        rect = self.buttons['endScreenL1'][0].get_rect()
                        rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]
                        self.buttons['endScreenL1'][1] = rect
                        self.currentS = 5
                    elif data == 'r':
                        # Enemy Resigned
                        self.buttons['endScreenL1'][0] = self.font.render('Enemy Resigned', True, self.black)
                        rect = self.buttons['endScreenL1'][0].get_rect()
                        rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]
                        self.buttons['endScreenL1'][1] = rect
                        self.buttons['endScreenL2'][0] = self.font.render(
                            ['Black', 'White'][self.colorC == 'White'] + ' won',
                            True, self.black)
                        rect = self.buttons['endScreenL2'][0].get_rect()
                        rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2 + + self.square[0]]
                        self.buttons['endScreenL2'][1] = rect
                        self.currentS = 5
                    elif data == 'q':
                        # Asking for draw
                        self.currentS = 9
                    elif data == 'd':
                        self.buttons['endScreenL1'][0] = self.font.render("", True, self.black)
                        self.currentS = 5
                    elif data == 'n':
                        # Draw was rejected
                        self.currentS = 4
                    else:
                        # CheckMate
                        self.buttons['endScreenL2'][0] = self.font.render(
                            ['Black', 'White'][self.colorC == 'White'] + ' won',
                            True, self.black)
                        rect = self.buttons['endScreenL2'][0].get_rect()
                        rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2 + + self.square[0]]
                        self.buttons['endScreenL2'][1] = rect
                        self.currentS = 5
            except (ConnectionAbortedError, ConnectionResetError, socket.timeout) as e:
                # Connection broke
                self._closeConnections()
                if self.currentS == 2:
                    self.threads.append(create_thread(self.server))
                print(e, 'error')
                self.info = [str(e)[17:] if str(e) != 'timed out' else str(e), self.red]

    def _removeIllegalMoves(self):
        """
        Method for checking if any of the available moves are illegal
        """
        illegalMoves = []
        for piece in self.myMoves.keys():
            for move in self.myMoves[piece]:
                tempBoard, _, _ = self._applyMove(self.board, move, [int(piece[2]), int(piece[1])])
                # Find the new enemy positions
                nextEnemyPiecesPos = [[i, j] for i, row in enumerate(tempBoard) for j, p in enumerate(row)
                                      if [p.isupper(), not p.isupper()][self.colorC == 'White'] and p]
                # Find the new enemy moves
                newEnemyMoves = {}
                for i, j in nextEnemyPiecesPos:
                    p = tempBoard[i][j]
                    temp = self.moves[p.lower()]([7 - j, 7 - i], [l[::-1] for l in tempBoard[::-1]])
                    newEnemyMoves[str(p) + str(i) + str(j)] = [[7 - a[0], 7 - a[1], a[2], a[3]] for a in temp]

                # Find if the enemy attacks the king in the new position
                attacked = False
                for p in newEnemyMoves.keys():
                    for m in newEnemyMoves[p]:
                        if m[2] == 1 and tempBoard[m[1]][m[0]].lower() == 'k':
                            illegalMoves.append([piece, move])
                            attacked = True
                            break
                    if attacked:
                        break

        for piece, move in illegalMoves:
            self.myMoves[piece] = [t for t in self.myMoves[piece] if t != move]

    def _checkPosition(self):
        """
        Method for checking if the current position is a CheckMate or some kind of Draw
        """
        if not any(self.myMoves.values()):
            # If the player doesn't have any legal moves then it's either a Stalemate or a CheckMate
            if self.checkedBy:
                print('Check Mate\n' + ['Black', 'White'][self.colorC == 'Black'] + ' won')
                self.buttons['endScreenL2'][0] = self.font.render(['Black', 'White'][self.colorC == 'Black'] + ' won',
                                                                  True, self.black)
                rect = self.buttons['endScreenL2'][0].get_rect()
                rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2 + + self.square[0]]
                self.buttons['endScreenL2'][1] = rect
            else:
                print("StaleMate, you have no legal move\n It's a Draw")
                self.buttons['endScreenL1'][0] = self.font.render('StaleMate, you have no legal moves', True,
                                                                  self.black)
                rect = self.buttons['endScreenL1'][0].get_rect()
                rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]
                self.buttons['endScreenL1'][1] = rect
            self.currentS = 5
        elif not any([p[0].lower() in ['r', 'q', 'p'] for p in self.myMoves.keys()]) and \
                not any([p[0].lower() in ['r', 'q', 'p'] for p in self.enemyMoves.keys()]):
            # If the player and the enemy don't any have queens,rooks and pawns
            # then we need to check if it's a draw due to insufficient material
            myB1 = myB2 = enB1 = enB2 = 0
            for i, j in [[int(p[1]), int(p[2])] for p in self.myMoves.keys() if p[0].lower() == 'b']:
                if (i - j) % 2:
                    myB2 += 1
                else:
                    myB1 += 1
            for i, j in [[int(p[1]), int(p[2])] for p in self.enemyMoves.keys() if p[0].lower() == 'b']:
                if (i - j) % 2:
                    enB2 += 1
                else:
                    enB1 += 1
            bSum = myB1 + myB2 + enB1 + enB2
            kSum = sum(p[0].lower() == 'n' for p in list(self.myMoves.keys()) + list(self.enemyMoves.keys()))
            if (bSum == 0 and kSum == 1) or (kSum == 0 and not ((myB1 > 0 or enB1 > 0) and (myB2 > 0 or enB2 > 0))):
                print("Draw due to Insufficient Material\n It's a Draw")
                self.buttons['endScreenL1'][0] = self.font.render('Draw due to Insufficient Material', True,
                                                                  self.black)
                rect = self.buttons['endScreenL1'][0].get_rect()
                rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]
                self.buttons['endScreenL1'][1] = rect
                self.currentS = 5
        elif self.halfMoveC == 100:
            # If no capture or pawn has moved in the last 100 moves (50 moves each)
            # Then it's a draw
            print("Draw due to 50-move Rule\n It's a Draw")
            self.buttons['endScreenL1'][0] = self.font.render('Draw due to 50-move Rule', True,
                                                              self.black)
            rect = self.buttons['endScreenL1'][0].get_rect()
            rect.midbottom = [self.gameS[0] // 2, self.gameS[1] // 2]
            self.buttons['endScreenL1'][1] = rect
            self.currentS = 5

    def _applyMove(self, tempBoard, move, originPos):
        """
        Method for applying a move to the input board
        :param tempBoard: the input board
        :param move: the move that will be applied
                     [x,y, - just moving/ 1 capturing/ 2 enPassant/ 3 castling, -/ enPassant position]
        :param originPos: the position of the piece
        :return: new updated board,
                 if a pawn was captured or not,
                 the applied move as array showing origin and destination in chess format
        """
        destinationPos = move[0:2]
        pawnCapture = 0
        board = [row[::] for row in tempBoard]
        currentPiece = board[originPos[1]][originPos[0]]

        if board[destinationPos[1]][destinationPos[0]].lower() or currentPiece.lower() == 'p':
            pawnCapture = 1
        board[destinationPos[1]][destinationPos[0]] = currentPiece
        if move[2] == 2:
            # EnPassant
            board[destinationPos[1] + 1][destinationPos[0]] = ''
        elif move[2] == 3:
            # Castling
            if destinationPos[0] >= 4:
                board[7][destinationPos[0] - 1] = ['r', 'R'][currentPiece.isupper()]
                board[7][7] = ''
            else:
                board[7][destinationPos[0] + 1] = ['r', 'R'][currentPiece.isupper()]
                board[7][0] = ''

        board[originPos[1]][originPos[0]] = ''
        return board, pawnCapture, [self._arrInd2ChessPos(self.colorC[0], originPos),
                                    self._arrInd2ChessPos(self.colorC[0], destinationPos)]

    def _chessLogig(self, mousePos):
        """
        Method for handling all the events and logic related to chess
        :param mousePos: the current position of the mouse
        """
        cellPos = [int(mousePos[0] // self.square[0]), int(mousePos[1] // self.square[1])]

        if pygame.mouse.get_pressed(3) == (1, 0, 0):
            if not self.promotion:
                if cellPos in self.myPiecesPos:
                    p = self.board[cellPos[1]][cellPos[0]]
                    self.selectedC = [cellPos[0], cellPos[1], p + str(cellPos[1]) + str(cellPos[0])]
                    self.availablePos = self.myMoves[p + str(cellPos[1]) + str(cellPos[0])]
                elif self.selectedC and cellPos in [av[0:2] for av in self.myMoves[self.selectedC[2]]]:
                    i = [av[0:2] for av in self.myMoves[self.selectedC[2]]].index(cellPos)
                    self.move = self.myMoves[self.selectedC[2]][i]

                    self.enPassant = self.move[3]
                    currentPiece = self.board[self.selectedC[1]][self.selectedC[0]]
                    if currentPiece.lower() == 'k':
                        # If the king moves remove all castling rights of that color
                        s = list(self.castlingR)
                        while currentPiece in s or ['q', 'Q'][currentPiece.isupper()] in s:
                            s.pop([-1, 0][currentPiece.isupper()])
                        self.castlingR = ''.join(s)
                    elif currentPiece.lower() == 'r':
                        # If a rook moves remove the castling right of that rook for that color
                        if self.selectedC[0] == [0, 7][currentPiece.isupper()] and \
                                ['k', 'K'][currentPiece.isupper()] in self.castlingR:
                            s = list(self.castlingR)
                            s.pop(s.index(['k', 'K'][currentPiece.isupper()]))
                            self.castlingR = ''.join(s)
                        elif self.selectedC[0] == [7, 0][currentPiece.isupper()] and \
                                ['q', 'Q'][currentPiece.isupper()] in self.castlingR:
                            s = list(self.castlingR)
                            s.pop(s.index(['q', 'Q'][currentPiece.isupper()]))
                            self.castlingR = ''.join(s)
                    if self.selectedC[2][:2].lower() != 'p1':
                        self.board, pawnCapt, self.previousMove = self._applyMove(self.board, self.move, self.selectedC)
                        self.activeC = {'w': 'b', 'b': 'w'}[self.activeC]
                        self.selectedC = []
                        self.halfMoveC = [self.halfMoveC + 1, 0][pawnCapt]
                        self.fullMoveC += [0, 1][self.colorC == 'Black']
                        self.piecePl = self._array2FEN()
                    else:
                        self.promotion = self.promotions[self.colorC]
                        self.pr = False
                else:
                    self.selectedC = []
            else:
                if self.pr:
                    temp = []
                    for _, rect, p in self.promotion:
                        temp.append(rect.collidepoint(mousePos))
                    if any(temp):
                        p = self.promotion[temp.index(True)][2]
                        print({'White': p, 'Black': p.lower()}[self.colorC])
                        self.board[self.selectedC[1]][self.selectedC[0]] = {'White': p, 'Black': p.lower()}[self.colorC]
                        self.board, pawnCapt, self.previousMove = self._applyMove(self.board, self.move, self.selectedC)
                        self.activeC = {'w': 'b', 'b': 'w'}[self.activeC]
                        self.selectedC = []
                        self.promotion = []
                        self.halfMoveC = [self.halfMoveC + 1, 0][pawnCapt]
                        self.fullMoveC += [0, 1][self.colorC == 'Black']
                        self.piecePl = self._array2FEN()
                    else:
                        self.promotion = []
        else:
            if self.promotion and not self.pr:
                self.pr = True

    def _pawnMoves(self, cellPos: list, board: list):
        """
        availablePos = [x,y, capture or not (1,0) and 2 for enPassant, enPassant(only for pawns)]
        :param cellPos: the current position of the pawn
        :return: the available positions for the selected pawn
        """
        available = []
        current = board[cellPos[1]][cellPos[0]]
        if cellPos[1] > 0:
            # Check if it can move forward
            if not board[cellPos[1] - 1][cellPos[0]]:
                available.append([cellPos[0], cellPos[1] - 1, 0, '-'])
            # Check if it can capture anything
            for i in [-1, 1]:
                if 0 <= cellPos[0] + i <= 7:
                    temp = board[cellPos[1] - 1][cellPos[0] + i]
                    if temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                        available.append([cellPos[0] + i, cellPos[1] - 1, 1, '-'])

        # Checks if enPassant is possible
        if self.enPassant != '-' and cellPos[1] == 3:
            i = 'abcdefgh'[::{'White': 1, 'Black': -1}[self.colorC]].index(self.enPassant[0])
            if abs(cellPos[0] - i) == 1:
                available.append([i, cellPos[1] - 1, 2, '-'])
        # Check if it can move forward twice
        if cellPos[1] == 6:
            if not board[cellPos[1] - 2][cellPos[0]] and not board[cellPos[1] - 1][cellPos[0]]:
                available.append([cellPos[0], cellPos[1] - 2, 0,
                                  'abcdefgh'[::{'White': 1, 'Black': -1}[self.colorC]][cellPos[0]] +
                                  '45'[{'White': 0, 'Black': 1}[self.colorC]]])
        return available

    @staticmethod
    def _nightMoves(cellPos: list, board: list):
        """
        availablePos = [x,y, capture or not (1,0), enPassant(only for pawns)]
        :param cellPos: the current position of the knight
        :return: the available positions for the selected knight
        """
        available = []
        current = board[cellPos[1]][cellPos[0]]
        for i, j in [[-1, -2], [-1, 2], [-2, -1], [-2, 1], [1, -2], [1, 2], [2, -1], [2, 1]]:
            if 0 <= cellPos[1] + i < 8 and 0 <= cellPos[0] + j < 8:
                temp = board[cellPos[1] + i][cellPos[0] + j]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    pass
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] + j, cellPos[1] + i, 1, '-'])
                else:
                    available.append([cellPos[0] + j, cellPos[1] + i, 0, '-'])
        return available

    @staticmethod
    def _rookMoves(cellPos: list, board: list):
        """
        availablePos = [x,y, capture or not (1,0), enPassant(only for pawns)]
        :param cellPos: the current position of the rook
        :return: the available positions for the selected rook
        """
        available = []
        current = board[cellPos[1]][cellPos[0]]
        U, D, L, R = True, True, True, True
        for i in range(1, 8):
            if U and cellPos[1] - i >= 0:
                temp = board[cellPos[1] - i][cellPos[0]]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    U = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0], cellPos[1] - i, 1, '-'])
                    U = False
                else:
                    available.append([cellPos[0], cellPos[1] - i, 0, '-'])
            if D and cellPos[1] + i <= 7:
                temp = board[cellPos[1] + i][cellPos[0]]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    D = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0], cellPos[1] + i, 1, '-'])
                    D = False
                else:
                    available.append([cellPos[0], cellPos[1] + i, 0, '-'])
            if L and cellPos[0] - i >= 0:
                temp = board[cellPos[1]][cellPos[0] - i]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    L = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] - i, cellPos[1], 1, '-'])
                    L = False
                else:
                    available.append([cellPos[0] - i, cellPos[1], 0, '-'])
            if R and cellPos[0] + i <= 7:
                temp = board[cellPos[1]][cellPos[0] + i]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    R = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] + i, cellPos[1], 1, '-'])
                    R = False
                else:
                    available.append([cellPos[0] + i, cellPos[1], 0, '-'])
        return available

    @staticmethod
    def _bishopMoves(cellPos: list, board: list):
        """
        availablePos = [x,y, capture or not (1,0), enPassant(only for pawns)]
        :param cellPos: the current position of the bishop
        :return: the available positions for the selected bishop
        """
        available = []
        current = board[cellPos[1]][cellPos[0]]
        LU, RU, LD, RD = True, True, True, True
        for i in range(1, 8):
            if min(cellPos) - i >= 0 and LU:
                temp = board[cellPos[1] - i][cellPos[0] - i]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    LU = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] - i, cellPos[1] - i, 1, '-'])
                    LU = False
                else:
                    available.append([cellPos[0] - i, cellPos[1] - i, 0, '-'])
            if max(cellPos) + i <= 7 and RD:
                temp = board[cellPos[1] + i][cellPos[0] + i]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    RD = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] + i, cellPos[1] + i, 1, '-'])
                    RD = False
                else:
                    available.append([cellPos[0] + i, cellPos[1] + i, 0, '-'])
            if cellPos[1] - i >= 0 and cellPos[0] + i <= 7 and LD:
                temp = board[cellPos[1] - i][cellPos[0] + i]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    LD = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] + i, cellPos[1] - i, 1, '-'])
                    LD = False
                else:
                    available.append([cellPos[0] + i, cellPos[1] - i, 0, '-'])
            if cellPos[0] - i >= 0 and cellPos[1] + i <= 7 and RU:
                temp = board[cellPos[1] + i][cellPos[0] - i]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    RU = False
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] - i, cellPos[1] + i, 1, '-'])
                    RU = False
                else:
                    available.append([cellPos[0] - i, cellPos[1] + i, 0, '-'])
        return available

    def _queenMoves(self, cellPos: list, board: list):
        """
        availablePos = [x,y, capture or not (1,0), enPassant(only for pawns)]
        :param cellPos: the current position of the queen
        :return: the available positions for the selected queen
        """
        available = self._rookMoves(cellPos, board)
        available += self._bishopMoves(cellPos, board)
        return available

    def _kingMoves(self, cellPos: list, board: list):
        """
        availablePos = [x,y, capture or not (1,0) or 3 for castling, enPassant(only for pawns)]
        :param cellPos: the current position of the king
        :return: the available positions for the selected king
        """
        available = []
        current = board[cellPos[1]][cellPos[0]]
        for i, j in [[-1, -1], [-1, 0], [-1, 1], [1, -1], [1, 0], [1, 1], [0, -1], [0, 1]]:
            if 0 <= cellPos[1] + i < 8 and 0 <= cellPos[0] + j < 8:
                temp = board[cellPos[1] + i][cellPos[0] + j]
                if temp and [not temp.isupper(), temp.isupper()][current.isupper()]:
                    pass
                elif temp and [temp.isupper(), not temp.isupper()][current.isupper()]:
                    available.append([cellPos[0] + j, cellPos[1] + i, 1, '-'])
                else:
                    available.append([cellPos[0] + j, cellPos[1] + i, 0, '-'])

        if not self.checkedBy:
            kSide = [board[7][1:3], board[7][5:7]][current.isupper()]
            kSideN = [[2, 7], [5, 7]][current.isupper()] not in [m[:2] for ms in self.enemyMoves.values() for m in ms]
            qSide = [board[7][4:7], board[7][1:4]][current.isupper()]
            qSideN = [[4, 7], [3, 7]][current.isupper()] not in [m[:2] for ms in self.enemyMoves.values() for m in ms]
            if current in self.castlingR and not any(kSide) and kSideN:
                available.append([[1, 6][current.isupper()], 7, 3, '-'])
            if ['q', 'Q'][current.isupper()] in self.castlingR and not any(qSide) and qSideN:
                available.append([[5, 2][current.isupper()], 7, 3, '-'])
        return available

    def draw(self):
        """ A method to draw the board on the screen """
        # Drawing the board
        for i in range(9):
            for j in range(4):
                if not i % 2:
                    pygame.draw.rect(self.scrn, self.white2,
                                     [i * self.square[0], j * 2 * self.square[1], self.square[0], self.square[1]])
                    pygame.draw.rect(self.scrn, self.green2,
                                     [i * self.square[0], (j * 2 + 1) * self.square[1], self.square[0], self.square[1]])
                else:
                    pygame.draw.rect(self.scrn, self.white2,
                                     [i * self.square[0], (j * 2 + 1) * self.square[1], self.square[0], self.square[1]])
                    pygame.draw.rect(self.scrn, self.green2,
                                     [i * self.square[0], j * 2 * self.square[1], self.square[0], self.square[1]])

        if self.currentS < 4:
            for i, p in enumerate(self.pieces.values()):
                self.scrn.blit(p, [self.square[0] * (i % 6), i // 6 * self.square[1]])
        elif self.currentS in [4, 5, 8] and self.piecePl:
            # Draw previous move
            for pos in self.previousMove:
                if pos != '--':
                    pos = self._chessPos2arrInd(self.colorC[0], pos)
                    rect = pygame.Surface(self.square)
                    rect.set_alpha(180)
                    rect.fill(self.yellow)
                    self.scrn.blit(rect, [pos[0] * self.square[0], pos[1] * self.square[1]])

            # Draw Selected Piece
            if self.selectedC:
                rect = pygame.Surface(self.square)
                rect.set_alpha(180)
                rect.fill(self.yellow)
                self.scrn.blit(rect, [self.selectedC[0] * self.square[0], self.selectedC[1] * self.square[1]])

            # Draw pieces
            for i, row in enumerate(self.piecePl.split('/')):
                j = 0
                for p in row:
                    if p in '12345678':
                        j += int(p)
                    else:
                        if p.isupper():
                            self.scrn.blit(self.pieces['w' + p], [j * self.square[0], i * self.square[1]])
                        else:
                            self.scrn.blit(self.pieces['b' + p.upper()], [j * self.square[0], i * self.square[1]])
                        j += 1

            # Draw available positions for the selected cell
            if self.selectedC:
                for c in self.myMoves[self.selectedC[2]]:
                    rect = pygame.Surface(self.square)
                    rect.set_alpha(40)
                    rect.fill(self.gray)
                    if not c[2]:
                        pygame.draw.circle(rect, self.black, [self.square[0] // 2, self.square[1] // 2],
                                           self.square[0] // 5)
                    else:
                        pygame.draw.circle(rect, self.black, [self.square[0] // 2, self.square[1] // 2],
                                           self.square[0] // 2, 6)
                    self.scrn.blit(rect, [c[0] * self.square[0], c[1] * self.square[1]])

            for p, b, _ in self.promotion:
                self.scrn.blit(p, b)
        elif self.currentS == 7:
            # Draw previous move
            game = self.gameHistory[self.gameHiSelection][self.gameHiMove]
            fen = game.split(' ')[0][::[1, -1][self.gameHiColor == 'B']]
            prevMove = [game[-4:-2], game[-2:]]
            for pos in prevMove:
                if pos != '--':
                    pos = self._chessPos2arrInd(self.gameHiColor, pos)
                    rect = pygame.Surface(self.square)
                    rect.set_alpha(180)
                    rect.fill(self.yellow)
                    self.scrn.blit(rect, [pos[0] * self.square[0], pos[1] * self.square[1]])

            # Draw pieces
            for i, row in enumerate(fen.split('/')):
                j = 0
                for p in row:
                    if p in '12345678':
                        j += int(p)
                    else:
                        if p.isupper():
                            self.scrn.blit(self.pieces['w' + p], [j * self.square[0], i * self.square[1]])
                        else:
                            self.scrn.blit(self.pieces['b' + p.upper()],
                                           [j * self.square[0], i * self.square[1]])
                        j += 1

        # Drawing the numbers and letters of squares
        if self.colorC == 'Black':
            for i, l in enumerate('8h7g6f5e4d3c2b1a'):
                if not i // 2 % 2:
                    color = self.white2
                else:
                    color = self.green2
                n = self.font2.render(l, True, color)
                n_rect = n.get_rect()
                if not i % 2:
                    n_rect.topleft = [0, self.square[1] * (7 - (i // 2))]
                else:
                    n_rect.bottomright = [self.square[0] * (i // 2 + 1), 8 * self.square[1]]
                self.scrn.blit(n, n_rect)
        else:
            for i, l in enumerate('1a2b3c4d5e6f7g8h'):
                if not i // 2 % 2:
                    color = self.white2
                else:
                    color = self.green2
                n = self.font2.render(l, True, color)
                n_rect = n.get_rect()
                if not i % 2:
                    n_rect.topleft = [0, self.square[1] * (7 - (i // 2))]
                else:
                    n_rect.bottomright = [self.square[0] * (i // 2 + 1), 8 * self.square[1]]
                self.scrn.blit(n, n_rect)

        for button in self.buttons.values():
            if str(self.currentS) in button[2]:
                self.scrn.blit(button[0], button[1])

        if self.currentS == 2:
            # Create Lobby Screen
            lines = ["Waiting for 2nd Player ", f"to connect on port {self.port}"]
            if self.connectionEst:
                lines = ["2nd Player Connected"]
            if self.colorC:
                lines.append(f'You are playing with {self.colorC}')
            for i, line in enumerate(lines):
                waitText = self.font.render(line, True, self.black)
                waitText_rect = waitText.get_rect()
                waitText_rect.center = [self.gameS[0] // 2, self.gameS[1] // 3 + i * 40]
                self.scrn.blit(waitText, waitText_rect)

        # Displaying info text:
        infoT = self.font2.render(self.info[0], True, self.info[1], self.white2)
        self.scrn.blit(infoT, infoT.get_rect())

        pygame.display.update()

    def running(self):
        self.keyPressed = ''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN:
                self.keyPressed = event.unicode
                if event.key == pygame.K_ESCAPE:
                    if self.currentS in [2, 3, 5, 6, 7]:
                        self.currentS = 1
                    elif self.currentS == 1:
                        self.quit()
                    elif self.currentS == 4:
                        self.currentS = 8
                    elif self.currentS == 8:
                        self.currentS = 4
                elif event.key == pygame.K_BACKSPACE and self.currentS == 3:
                    self.port = self.port[:-1]
                elif event.key == pygame.K_RIGHT and self.currentS == 7 and \
                        self.gameHiMove < len(self.gameHistory[self.gameHiSelection]) - 1:
                    self.gameHiMove += 1
                elif event.key == pygame.K_LEFT and self.currentS == 7 and self.gameHiMove > 0:
                    self.gameHiMove -= 1
                elif event.key == pygame.K_SPACE:
                    self.gameHiColor = ['W', 'B'][self.gameHiColor == 'W']

        return True

    def quit(self):
        print(self.connectionEst)
        self.sock.close()
        for thread in self.threads:
            thread.join()
        print(self.connectionEst)
        pygame.quit()
