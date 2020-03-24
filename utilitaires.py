# -*- coding: utf-8 -*-

# Classes principalement utilisées dans genereClasses.py et genereImagettes.py

class Classe:
    '''
    Mémorise les caractéristiques d'une classe (type d'objet que l'on voudra faire apprendre à un réseau de neurones)
    '''
    def __init__(self,numero,nom):
        self.couleur = '#ff0000'
        self.nom = nom
        self.numero = numero

class ROI:
    '''
    Mémorise le centre du ROI ainsi que sa classe associée
    '''
    def __init__(self,x,y,classe):
        self.x = x
        self.y = y
        self.classe = classe

class Image:
    '''
    Représente une image (depuis un fichier ou une vidéo) et mémorise sa liste de ROI associés
    '''
    def __init__(self,idImg,posImg):
        self.idImg = idImg
        self.posImg = posImg
        self.lesROI = []

class Param:
    '''
    Mémorise les paramètres du projet (dimension du ROI et caractéristiques de la source d'images)
    '''
    def __init__(self):
        self.largeurROI = 40
        self.hauteurROI = 40
        self.video = True  # True si source est vidéo, False si répertoire images
        self.fichierOuRepertoire = None