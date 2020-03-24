# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import  *


class BoutonClasse(QPushButton):
    '''
    Un bouton, associé à un label, qui permet de changer la classe cournate, càd celle qui sera associée à tous les futurs ROi créés
    '''
    # Les signaux
    rightClick = pyqtSignal()
    doubleClicked = pyqtSignal()
    clicked = pyqtSignal()

    def __init__(self, laClasse):
        """
        Constructeur mémorisant la classe et utilisant ses caractéristiques pour initialiser la couleur et le texte du bouton
        :param laClasse:
        """
        QPushButton.__init__(self, laClasse.nom)
        self.laClasse = laClasse
        self.setStyleSheet("background-color: %s " % laClasse.couleur)
        self.setMinimumHeight(100)
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.clicked.emit)
        super().clicked.connect(self.checkDoubleClick)

    def mousePressEvent(self, event):
        '''
        Edition de la couleur sur un clic droit
        :param event:
        :return:
        '''
        QPushButton.mousePressEvent(self, event)
        if event.button() == Qt.RightButton:
            # Edition de la couleur sur un clic droit
            color = QColorDialog.getColor()
            self.setStyleSheet("background-color: %s" % color.name())
            self.laClasse.couleur = color.name()

    def checkDoubleClick(self):
        '''
        Edition du texte du bouton sur un double-clic (modifie aussi le nom associé à la classe)
        :return:
        '''
        if self.timer.isActive():
            text, ok = QInputDialog.getText(self, 'Changement de classe', 'Nom de la classe :')
            if ok:
                self.setText(text)
                self.laClasse.nom = text
            self.timer.stop()
        else:
            self.timer.start(250)