# -*- coding: utf-8 -*-
import cv2

class SourceImagesVideo:
    '''
    Source d'images depuis une vidéo
    '''
    def __init__(self,fichierVideo):
        '''
        Constructeur
        :param fichierVideo: le fichier vidéo
        '''
        self.indiceImage = 0
        self.cap = cv2.VideoCapture(fichierVideo)
        self.nbFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def imageCourante(self,ind):
        '''
        Récupération de la 'ind' ième image de la vidéo
        :param ind:
        :return: la position de cette image dans la vidéo et l'image elle même (format OpenCV)
        '''
        self.indiceImage = ind
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.indiceImage)
        ret, frame = self.cap.read()
        return self.indiceImage, frame

    def imagePrecedente(self):
        '''
        Recule, si possible, sur l'image précédente
        :return: l'image précédente et sa position (ou bien l'image courante si pas possible)
        '''
        self.indiceImage -= 1
        if self.indiceImage < 0:  # Pour ne pas aller avant la première image
            self.indiceImage = 0
        return  self.imageCourante(self.indiceImage)

    def imageSuivante(self):
        '''
        Avance, si possible, sur l'image suivante
        :return: l'image suivante et sa position (ou bien l'image courante si pas possible)
        '''
        self.indiceImage += 1
        if self.indiceImage == self.nbFrames:  # Pour ne pas aller au delà de la dernière image
            self.indiceImage -= 1
        return self.imageCourante(self.indiceImage)