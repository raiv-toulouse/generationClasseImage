# -*- coding: utf-8 -*-
from imutils import paths
import cv2

class SourceImagesFichier:
    '''
    Source d'images depuis un répertoire
    '''
    def __init__(self,repertoireImage):
        '''
        Constructeur
        :param repertoireImage: un répertoire contenant les images à traiter
        '''
        self.indiceImage = 0
        self.repertoireImage = repertoireImage
        self.imagePaths = sorted(list(paths.list_images(self.repertoireImage)))
        self.nbFrames = len(self.imagePaths)

    def imageCourante(self,ind):
        '''
        Récupération de la 'ind' ième image du répertoire
        :param ind:
        :return: la position de cette image dans la liste des images du répertoire et l'image elle même (format OpenCV)
        '''
        self.indiceImage = ind
        nomFichier = self.imagePaths[self.indiceImage]
        imgCV = cv2.imread(nomFichier)
        return self.indiceImage, imgCV

    def imagePrecedente(self):
        '''
        Recule, si possible, sur l'image précédente
        :return: l'image précédente et sa position (ou bien l'image courante si pas possible)
        '''
        self.indiceImage -= 1
        if self.indiceImage < 0: # Pour ne pas aller avant la première image
            self.indiceImage = 0
        return self.imageCourante(self.indiceImage)

    def imageSuivante(self):
        '''
        Avance, si possible, sur l'image suivante
        :return: l'image suivante et sa position (ou bien l'image courante si pas possible)
        '''
        self.indiceImage += 1
        if self.indiceImage == self.nbFrames:  # Pour ne pas aller au delà de la dernière image
            self.indiceImage -= 1
        return self.imageCourante(self.indiceImage)