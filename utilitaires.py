# -*- coding: utf-8 -*-
class Classe:
    def __init__(self,numero,nom):
        self.couleur = '#ff0000'
        self.nom = nom
        self.numero = numero

class ROI:
    def __init__(self,x,y,classe):
        self.x = x
        self.y = y
        self.classe = classe

class Image:
    def __init__(self,idImg,posImg):
        self.idImg = idImg
        self.posImg = posImg
        self.lesROI = []

class Param:
    def __init__(self):
        self.largeurROI = 40
        self.hauteurROI = 40
        self.video = True  # True si source est vidéo, False si répertoire images
        self.fichierOuRepertoire = None