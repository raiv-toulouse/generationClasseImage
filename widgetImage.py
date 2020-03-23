# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class WidgetImage(QLabel):
    nouveauPoint = pyqtSignal(int,int)

    def __init__(self,parent=None):
        super(WidgetImage, self).__init__()
        self.parent = parent
        self.setCursor(Qt.CrossCursor)
        self.parent.signalUndo.connect(self.effacer)

    def changeROI(self,larg,haut):
        self.largROI = larg
        self.hautROI = haut

    def changeClasse(self,classe):
        self.classe = classe

    def effacer(self):
        self.dessinerROI(self.x,self.y,Qt.black)

    def mousePressEvent(self, QMouseEvent):
        self.x = QMouseEvent.pos().x()
        self.y = QMouseEvent.pos().y()
        self.dessinerROI(self.x,self.y)

    def dessinerROI(self,x,y,color=None):
        painter = QPainter(self.pixmap)
        if color:
            pen = QPen(color, 1)
        else:
            pen = QPen(QColor(self.classe.couleur), 1)
        painter.setPen(pen)
        self.nouveauPoint.emit(x,y)
        painter.drawRect(x-int(self.largROI/2),y-int(self.hautROI/2),self.largROI,self.hautROI)
        painter.end()
        self.setPixmap(self.pixmap)

    def afficherImage(self, imgCV):
        # Affichage d'une image dans le WidgetImage
        img = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        bytesPerLine = 3 * width
        mQImage = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(mQImage)
        self.setPixmap(self.pixmap)
