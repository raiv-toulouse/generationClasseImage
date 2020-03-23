# -*- coding: utf-8 -*-
from imutils import paths
import cv2

class SourceImagesFichier:
    def __init__(self,repertoireImage):
        self.indiceImage = 0
        self.repertoireImage = repertoireImage
        self.imagePaths = sorted(list(paths.list_images(self.repertoireImage)))
        self.nbFrames = len(self.imagePaths)

    # Lecture de l'image depuis le disque
    def imageCourante(self,ind):
        self.indiceImage = ind
        nomFichier = self.imagePaths[self.indiceImage]
        imgCV = cv2.imread(nomFichier)
        return self.indiceImage, imgCV

    def imagePrecedente(self):
        self.indiceImage -= 1
        if self.indiceImage < 0: # Pour ne pas aller avant la première image
            self.indiceImage = 0
        return self.imageCourante(self.indiceImage)

    def imageSuivante(self):
        self.indiceImage += 1
        if self.indiceImage == self.nbFrames:  # Pour ne pas aller au delà de la dernière image
            self.indiceImage -= 1
        return self.imageCourante(self.indiceImage)