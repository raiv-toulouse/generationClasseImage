# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class WidgetImage(QLabel):
    nouveauPoint = pyqtSignal(int,int)

    def __init__(self,parent=None):
        super(WidgetImage, self).__init__()
        self.setCursor(Qt.CrossCursor)

    def changeROI(self,larg,haut):
        self.largROI = larg
        self.hautROI = haut

    def changeClasse(self,classe):
        self.classe = classe

    def mousePressEvent(self, QMouseEvent):
        painter = QPainter(self.pixmap)
        pen = QPen(QColor(self.classe.couleur), 1)
        painter.setPen(pen)
        x = QMouseEvent.pos().x()
        y = QMouseEvent.pos().y()
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
