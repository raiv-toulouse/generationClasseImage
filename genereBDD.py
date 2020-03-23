#
# Construit la banque d'images depuis une série de fichiers
#
import numpy as np
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import os,cv2,sys
from imutils import paths

NOM_FICHIER_ROI = 'demiLargeurROI.txt'

class DialogGenerationBDD(QDialog):
    def __init__(self):
        super(DialogGenerationBDD,self).__init__()
        loadUi('ihm_genereClasses.ui',self)
        self.imagesChargees = False
        if os.path.exists(NOM_FICHIER_ROI):
            f = open(NOM_FICHIER_ROI,'r')
            self.demiLargeurROI = int(f.readline())
            f.close()
        else:
            self.demiLargeurROI = 100
        self.edtLargeurROI.setText(str(2*self.demiLargeurROI))
        self.roi = QRect(320-self.demiLargeurROI, 0, self.demiLargeurROI * 2, 480)
        self.sauverDemiLargeurROI()
        self.fichierSortie = open('lesFichiers','a')
        # Gestion d'evt pour les boutons et autres widgets
        self.btnRepertoireImage.clicked.connect(self.selectionnerRepertoireImage)
        self.btnSuivant.clicked.connect(self.imageSuivante)
        self.btnPrecedent.clicked.connect(self.imagePrecedente)
        self.btnDebut.clicked.connect(self.imageDebut)
        self.btnMais.clicked.connect(self.enregistrerImage)
        self.btnRien.clicked.connect(self.enregistrerImage)
        self.btnDouble.clicked.connect(self.enregistrerImage)
        self.btnAutre.clicked.connect(self.enregistrerImage)
        self.edtLargeurROI.textChanged.connect(self.chgtLargeurROI)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',"Etes vous sûr de vouloir quitter?", QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.fichierSortie.close()
            event.accept()
        else:
            event.ignore()

    def sauverDemiLargeurROI(self):
        fichierROI = open(NOM_FICHIER_ROI,'w')
        fichierROI.write(str(self.demiLargeurROI))
        fichierROI.close()

    def imageDebut(self):
        self.indiceImage=0
        self.afficherImageCourante()

    def chgtLargeurROI(self):
        txt = self.edtLargeurROI.text()
        if txt:
            self.demiLargeurROI = int(int(txt)/ 2.0)
            self.sauverDemiLargeurROI()
            self.roi = QRect(320 - self.demiLargeurROI, 0, self.demiLargeurROI * 2, 480)
            self.afficherImageCourante()

    def imageSuivante(self):
        self.indiceImage+=1
        if self.indiceImage==len(self.imagePaths):  # Pour ne pas aller au delà de la dernière image
            self.indiceImage -= 1
        self.afficherImageCourante()

    def imagePrecedente(self):
        self.indiceImage-=1
        if self.indiceImage<0: # Pour ne pas aller avant la première image
            self.indiceImage=0
        self.afficherImageCourante()

    def selectionnerRepertoireImage(self):
        self.repertoireImage = str(QFileDialog.getExistingDirectory(self, "Selectionnez le répertoire contenant les images"))
        self.lblRepertoireImage.setText(self.repertoireImage)
        self.imagePaths = sorted(list(paths.list_images(self.repertoireImage)))
        self.imagesChargees = True
        # Affichage de la première image
        self.indiceImage = 0
        self.afficherImageCourante()

    def afficherImageCourante(self):
        # Lecture de l'image depuis le disque
        nomFichier = self.imagePaths[self.indiceImage]
        self.lblFichier.setText(nomFichier)
        imgCV = cv2.imread(nomFichier)
        # Affichage d'une image dans le QLabel
        img = cv2.cvtColor(imgCV, cv2.COLOR_BGR2RGB)
        height, width, _ = img.shape
        bytesPerLine = 3 * width
        mQImage = QImage(img.data, width, height, bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(mQImage)
        painter = QPainter(pixmap)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        painter.drawRect(self.roi)
        painter.end()
        self.lblImage.setPixmap(pixmap)
        imageRoi = imgCV[self.roi.y():self.roi.y()+self.roi.height(),self.roi.x():self.roi.x()+self.roi.width()]

    def enregistrerImage(self):
        nomFichier = self.imagePaths[self.indiceImage]
        txtBouton = self.sender().objectName()[3:]
        self.fichierSortie.write(nomFichier+';'+txtBouton+'\n')
        self.imageSuivante()



app = QApplication(sys.argv)
widget = DialogGenerationBDD()
widget.show()
sys.exit(app.exec_())
