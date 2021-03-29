import sys
import cfg
import pygame
import modules.Levels as Levels
import modules.Util as Util
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import QMainWindow,  QApplication


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 553)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Users/ios/.designer/backup/Users/ios/Desktop/src=http___c-ssl.duitang.com_uploads_item_201605_19_20160519225450_RHyA5.png&refer=http___c-ssl.duitang.jpeg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(310, 240, 171, 81))
        font = QtGui.QFont()
        font.setFamily("American Typewriter")
        font.setPointSize(24)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(310, 340, 171, 81))
        font = QtGui.QFont()
        font.setFamily("American Typewriter")
        font.setPointSize(24)
        font.setItalic(False)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(250, 80, 291, 91))
        font = QtGui.QFont()
        font.setFamily("Baskerville")
        font.setPointSize(64)
        font.setItalic(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(310, 160, 171, 20))
        font = QtGui.QFont()
        font.setFamily("American Typewriter")
        font.setItalic(False)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PAC-MAN"))
        self.pushButton_2.setText(_translate("MainWindow", "Play"))
        self.pushButton_3.setText(_translate("MainWindow", "Quit"))
        self.label.setText(_translate("MainWindow", "PAC-MAN"))
        self.label_2.setText(_translate("MainWindow", "Python Group Assignment"))

        self.pushButton_2.clicked.connect(self.play)
        self.pushButton_3.clicked.connect(QCoreApplication.instance().quit)

    def play(self, MainWindow):
        main(initialize())

def startLevelGame(level, screen, font):
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(cfg.SKYBLUE)
    gate_sprites = level.setupGate(cfg.WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers(cfg.HEROPATH, [cfg.BlinkyPATH, cfg.ClydePATH, cfg.InkyPATH, cfg.PinkyPATH])
    food_sprites = level.setupFood(cfg.YELLOW, cfg.WHITE)
    superFood_sprites = level.setupSuperFood(cfg.YELLOW, cfg.WHITE)
    pathData = level.setupPathData()
    is_clearance = False
    move_buffer = Util.Vector2.Zero()
    while True:
        # Input from User
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    move_buffer = -1 * Util.Vector2.Right()
                elif (event.key == pygame.K_RIGHT):
                    move_buffer = Util.Vector2.Right()
                elif (event.key == pygame.K_UP):
                    move_buffer = Util.Vector2.Up()
                elif (event.key == pygame.K_DOWN):
                    move_buffer = -1 * Util.Vector2.Up()
            # elif(event.type == pygame.KEYUP):
            #     move_dir = Vector2.Zero()

        # GhostAI Installment
        for hero in hero_sprites:
            for ghost in ghost_sprites:
                if ghost.AIProgram != None:
                    tmp_move_buffer = ghost.AIProgram(pathData, ghost, hero)
                ghost.update(wall_sprites, gate_sprites, tmp_move_buffer)

        screen.fill(cfg.BLACK)
        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites, move_buffer)
        hero_sprites.draw(screen)
        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
            food_eaten += 2 * pygame.sprite.spritecollide(hero, superFood_sprites, True)
        SCORE += len(food_eaten)
        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)
        superFood_sprites.draw(screen)
        ghost_sprites.draw(screen)

        score_text = font.render("Score: %s" % SCORE, True, cfg.RED)
        screen.blit(score_text, [10, 10])
        if len(food_sprites) == 0:
            is_clearance = True
            break
        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            is_clearance = False
            break
        pygame.display.flip()
        clock.tick(30)
    return is_clearance


def showText(screen, font, is_clearance, flag=False):
    clock = pygame.time.Clock()
    msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
    positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 200))
    texts = [font.render(msg, True, cfg.WHITE),
            font.render('Press ENTER to continue or play again.', True, cfg.WHITE),
            font.render('Press ESCAPE to quit.', True, cfg.WHITE)]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if is_clearance:
                        if not flag:
                            return
                        else:
                            main(initialize())
                    else:
                        main(initialize())
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
                    pygame.quit()
        for idx, (text, position) in enumerate(zip(texts, positions)):
            screen.blit(text, position)
        pygame.display.flip()
        clock.tick(10)


def initialize():
    pygame.init()
    icon_image = pygame.image.load(cfg.ICONPATH)
    pygame.display.set_icon(icon_image)
    screen = pygame.display.set_mode([606, 606])
    pygame.display.set_caption('Pacman')
    return screen

def main(screen):
    pygame.mixer.init()
    pygame.mixer.music.load(cfg.BGMPATH)
    pygame.mixer.music.play(-1, 0.0)
    pygame.font.init()
    font_small = pygame.font.Font(cfg.FONTPATH, 18)
    font_big = pygame.font.Font(cfg.FONTPATH, 24)
    for num_level in range(1, Levels.NUMLEVELS+1):
        level = getattr(Levels, f'Level0{num_level}')()
        is_clearance = startLevelGame(level, screen, font_small)
        if num_level == Levels.NUMLEVELS:
            showText(screen, font_big, is_clearance, True)
        else:
            showText(screen, font_big, is_clearance)


'''run'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
