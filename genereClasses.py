# -*- coding: utf-8 -*-
import argparse
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUi
from boutonClasse import BoutonClasse
from sourceImagesFichier import SourceImagesFichier
from sourceImagesVideo import SourceImagesVideo
from dialogParam import DialogParam
from utilitaires import Classe,ROI,Image,Param
import pickle


class IHMGenereClasses(QDialog):
    signalUndo = pyqtSignal()

    def __init__(self, args):
        super(QDialog, self).__init__()
        loadUi('ihm_genereClasses.ui', self)
        self.btnSuivant.clicked.connect(self.imageSuivante)
        self.btnPrecedent.clicked.connect(self.imagePrecedente)
        self.btnParam.clicked.connect(self.changerParam)
        self.lblImage.nouveauPoint.connect(self.ajoutPoint)
        self.imageSlider.valueChanged.connect(self.selectImage)
        self.btnUndo.clicked.connect(self.undo)
        # Les attributs
        self.lesClasses = []
        self.lesLabelsCompteurs = []
        self.lesImages = []
        # Ajout des boutons de classe
        if args["repProjet"]:  # Un projet existe
            self.initDepuisProjet(args)
        else:  # Pas encore de projet => première fois
            self.initPremiereFois(args)
        self.verticalLayout.addSpacerItem(QSpacerItem(150, 10, QSizePolicy.Expanding))

    def undo(self):
        imgCourante = self.lesImages[-1]
        if imgCourante.lesROI:
            imgCourante.lesROI.pop()
            self.signalUndo.emit()  # Pour demander à effacer le dessin du ROI dans WidgetImage
            # Màj du compteur de cette classe
            numClasse = self.laClasseCourante.numero
            nbEltDansClasse = int(self.lesLabelsCompteurs[numClasse].text())
            nbEltDansClasse -= 1
            self.lesLabelsCompteurs[numClasse].setText(str(nbEltDansClasse))

    def selectImage(self):
        if hasattr(self,'sourceImages'):  # Pour éviter une erreur lors de l'initialisation
            indImg = self.imageSlider.value()
            idImg, img = self.sourceImages.imageCourante(indImg)
            self.lesImages.append(Image(idImg, indImg))
            self.lblImage.afficherImage(img)
            self.lblIndFrame.setText(str(self.imageSlider.value()))

    def selectSource(self):
        if self.param.video:  # On va lire depuis une vidéo
            self.sourceImages = SourceImagesVideo(self.param.fichierOuRepertoire)
        else:
            self.sourceImages = SourceImagesFichier(self.param.fichierOuRepertoire)
        self.imageSlider.maximum = self.sourceImages.nbFrames
        self.lblNbFrames.setText(str(self.imageSlider.maximum))

    def changerParam(self):
        dialog = DialogParam(self.param)
        result = dialog.exec_()
        if result:
            self.lblImage.changeROI(self.param.largeurROI, self.param.hauteurROI)
            self.lesImages = []
            self.selectSource()
            for lbl in self.lesLabelsCompteurs:
                lbl.setText('0')
            self.imageSuivante()

    def initPremiereFois(self,args):
        nbClass = int(args["nbClass"])
        # Construction dynamique des boutons de classe
        for i in range(nbClass):
            self.lesClasses.append(Classe(i, str(i)))
            self.ajoutBoutonClasse(self.lesClasses[i])
        self.param = Param()
        dialog = DialogParam(self.param)
        result = dialog.exec_()
        self.repertoireProjet = None
        self.selectSource()
        idImg, img = self.sourceImages.imageCourante(0)
        self.lesImages.append(Image(0, 0))
        self.lblImage.afficherImage(img)
        self.lblImage.changeROI(self.param.largeurROI,self.param.hauteurROI)
        self.changeClasseCourante(self.lesClasses[0])

    def initDepuisProjet(self,args):
        self.repertoireProjet = args["repProjet"]
        # Lecture du fichier des images
        fichImages = open(self.repertoireProjet+"/images","rb")
        self.lesImages = pickle.load(fichImages)
        fichImages.close()
        # On place le slider sur la dernière image
        posLastImage = self.lesImages[-1].posImg
        self.imageSlider.setValue(posLastImage)
        self.lblIndFrame.setText(str(posLastImage))
        # Lecture du fichier de paramètres
        fichParam = open(self.repertoireProjet+"/param","rb")
        self.param = pickle.load(fichParam)
        self.lesClasses = pickle.load(fichParam)
        fichParam.close()
        # Construction dynamique des boutons de classe
        for cl in self.lesClasses:
            self.ajoutBoutonClasse(cl)
        self.selectSource()
        idImg, img = self.sourceImages.imageCourante(posLastImage)
        self.lblImage.afficherImage(img)
        self.lblImage.changeROI(self.param.largeurROI,self.param.hauteurROI)
        self.changeClasseCourante(self.lesClasses[0])

    def ajoutBoutonClasse(self,laClasse):
        layoutHoriz = QHBoxLayout()
        button = BoutonClasse(laClasse)
        button.clicked.connect(self.make_calluser(laClasse))
        layoutHoriz.addWidget(button)
        # Combien de ROI déjà présents pour cette classe
        indClasse = laClasse.numero
        cptROI = 0
        for im in self.lesImages:
            for roi in im.lesROI:
                if roi.classe.numero == indClasse:
                    cptROI += 1
        # Ajout du label pour le compteur
        lbl = QLabel(str(cptROI))
        self.lesLabelsCompteurs.append(lbl)
        layoutHoriz.addWidget(lbl)
        self.verticalLayout.addLayout(layoutHoriz)

    # un nouveau point a été ajouté sur l'image
    def ajoutPoint(self,x,y):
        imgCourante = self.lesImages[-1]
        imgCourante.lesROI.append(ROI(x,y,self.laClasseCourante))
        # Màj du compteur de cette classe
        numClasse = self.laClasseCourante.numero
        nbEltDansClasse = int(self.lesLabelsCompteurs[numClasse].text())
        nbEltDansClasse += 1
        self.lesLabelsCompteurs[numClasse].setText(str(nbEltDansClasse))

    def changeClasseCourante(self, classe):
        self.laClasseCourante = classe
        self.lblImage.changeClasse(classe)
        # Mise à jour de l'IHM pour indiquer la nouvelle classe courante
        self.lblClasseCourante.setText(self.laClasseCourante.nom)
        self.lblClasseCourante.setStyleSheet("background-color: %s " % self.laClasseCourante.couleur)

    def imageSuivante(self):
        idImg, img = self.sourceImages.imageSuivante()
        if img is not None:
            self.imageSlider.setValue(self.imageSlider.value()+1)
            self.lesImages.append(Image(idImg,self.imageSlider.value()))
            self.lblImage.afficherImage(img)
            self.lblIndFrame.setText(str(self.imageSlider.value()))

    def imagePrecedente(self):
        idImg, img = self.sourceImages.imagePrecedente()
        if img is not None:
            self.imageSlider.setValue(self.imageSlider.value() - 1)
            self.lesImages.append(Image(idImg,self.imageSlider.value()))
            self.lblImage.afficherImage(img)
            self.lblIndFrame.setText(str(self.imageSlider.value()))

    def make_calluser(self, classe):
        def calluser():
            self.changeClasseCourante(classe)
        return calluser

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',"Quitter (Y/N) et sauver (Y)?", QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel)
        if reply == QMessageBox.Yes:  # On quitte en sauvant
            self.sauveDansFichier()
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()   # On quitte, mais sans sauver
        else:
            event.ignore()  # On ne quitte pas

    def sauveDansFichier(self):
        # Demande du répertoire de sauvegarde du projet
        if self.repertoireProjet==None: # Pas encore défini
            self.repertoireProjet = str(QFileDialog.getExistingDirectory(self, "Selectionnez le répertoire de sauvegarde du projet"))
        # Sauvegarde des paramètres
        fichParam = open(self.repertoireProjet+"/param","bw")
        pickle.dump(self.param,fichParam)
        pickle.dump(self.lesClasses, fichParam)
        fichParam.close()
        # Suppression des images qui n'ont pas de ROI
        self.lesImages = [im for im in self.lesImages  if im.lesROI]
        # Sauvegarde des images (avec leurs ROI)
        fichImages = open(self.repertoireProjet+"/images","wb")
        pickle.dump(self.lesImages,fichImages)
        fichImages.close()

#
# Programme principal
#
if __name__ == '__main__':
    # construct the argument parse and parse the arguments
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-n", "--nbClass", help="nombre de classes")
    group.add_argument("-r", "--repProjet", default=None, help="répertoire projet")
    args = vars(parser.parse_args())
    # IHM
    app = QApplication([])
    tb = IHMGenereClasses(args)
    tb.show()
    app.exec_()