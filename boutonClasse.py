# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *


# creation de la class, on precise qu'on derive la class QPushButton entre parentheses
class BoutonClasse(QPushButton):
    # creation du signal emetteur (emet rien pour le moment)
    rightClick = pyqtSignal()
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    # creation de notre fonction __init__ avec un arg string pour le nom du futur bouton
    def __init__(self, laClasse):
        QPushButton.__init__(self, laClasse.nom)
        self.laClasse = laClasse
        self.setStyleSheet("background-color: %s " % laClasse.couleur)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    # modification de la fontion mousePressEvent
    def mousePressEvent(self, event):
        # on integre la fonction QPushButton.mousePressEvent(self, event) a notre fonction PushRightButton.mousePressEvent(self, event)
        QPushButton.mousePressEvent(self, event)
        # condition du click droit
        if event.button() == Qt.RightButton:
            # Edition de la couleur sur un clic droit
            color = QColorDialog.getColor()
            self.setStyleSheet("background-color: %s" % color.name())
            self.laClasse.couleur = color.name()

    def checkDoubleClick(self):
        if self.timer.isActive():
            text, ok = QInputDialog.getText(self, 'Changement de classe', 'Nom de la classe :')
            if ok:
                self.setText(text)
                self.laClasse.nom = text
            self.timer.stop()
        else:
            self.timer.start(250)