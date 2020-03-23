import cv2

class SourceImagesVideo:
    def __init__(self,fichierVideo):
        self.indiceImage = 0
        self.cap = cv2.VideoCapture(fichierVideo)
        self.nbFrames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))

    def imageCourante(self,ind):
        self.indiceImage = ind
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.indiceImage)
        ret, frame = self.cap.read()
        return self.indiceImage, frame

    def imagePrecedente(self):
        self.indiceImage -= 1
        if self.indiceImage < 0:  # Pour ne pas aller avant la première image
            self.indiceImage = 0
        return  self.imageCourante(self.indiceImage)

    def imageSuivante(self):
        self.indiceImage += 1
        if self.indiceImage == self.nbFrames:  # Pour ne pas aller au delà de la dernière image
            self.indiceImage -= 1
        return self.imageCourante(self.indiceImage)