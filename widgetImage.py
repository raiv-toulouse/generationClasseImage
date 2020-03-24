# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import cv2

class WidgetImage(QLabel):
    '''
    Zone d'affichage de l'image sur laquelle on va dessiner les ROI
    '''
    nouveauPoint = pyqtSignal(int,int)  # Signal envoyé vers IHMGenereClasses

    def __init__(self,parent=None):
        super(WidgetImage, self).__init__()
        self.parent = parent
        self.setCursor(Qt.CrossCursor)
        self.parent.signalUndo.connect(self.effacer)

    def changeROI(self,larg,haut):
        '''
        Appelée depuis IHMGenereClasses pour signaler un changement de dimension du ROI
        :param larg: nouvelle largeur du ROI
        :param haut: nouvelle hauteur du ROI
        :return:
        '''
        self.largROI = larg
        self.hautROI = haut

    def changeClasse(self,classe):
        '''
        Appelée depuis IHMGenereClasses pour signaler un changement de classe
        :param classe: nouvelle classe
        :return:
        '''
        self.classe = classe

    def effacer(self):
        '''
        'Efface' un ROI en cas de Undo (le dessine en noir)
        :return:
        '''
        self.dessinerROI(self.x,self.y,Qt.black)

    def mousePressEvent(self, QMouseEvent):
        '''
        Suite à un clic gauche, dessine un ROI
        :param QMouseEvent:
        :return:
        '''
        self.x = QMouseEvent.pos().x()
        self.y = QMouseEvent.pos().y()
        self.dessinerROI(self.x,self.y)

    def dessinerROI(self,x,y,color=None):
        '''
        Dessin d'un ROI de la couleur de sa classe ou en noir en cas d'effacement du dit ROI
        :param x: coord x du centre du ROI
        :param y: coord y du centre du ROI
        :param color: couleur du ROI (celui de sa classe ou noir si effacement)
        :return:
        '''
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
        '''
        Appelée depuis IHMGenereClasses pour afficher l'image OpenCV
        :param imgCV: image OpenCV à afficher
        :return:
        '''
        # Affichage d'une image dans le WidgetImage
        img = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        bytesPerLine = 3 * width
        mQImage = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        self.pixmap = QPixmap.fromImage(mQImage)
        self.setPixmap(self.pixmap)
