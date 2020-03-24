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

#
# But : Création de ROI à partir d'images provenant d'une vidéo ou d'un répertoire.
#       Produit en sortie 2 fichiers, param et images, qui seront pris comme entrée par le programme genereImagettes
#
# python genereClasse -n <nb_de_classes>  si première fois (donc pas encore de projet)
# python genereClasse -r <répertoire_du_projet>  si déjà un projet contenant des images déjà traitées)
#
class IHMGenereClasses(QMainWindow):
    '''
    IHM permettant la création de ROI pour chacune des classes ce qui permettra de créer ensuite les imagettes correspondantes
    '''
    signalUndo = pyqtSignal()  # Signal envoyé à WidgetImage lors de la suppression du dernier ROI créé

    def __init__(self, args,parent=None):
        super(IHMGenereClasses, self).__init__()
        loadUi('ihm_genereClasses.ui', self)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint,True)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint,True)
        # Gestionnaires d'évenements
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
        # Ajout dynamique des boutons de classe
        if args["repProjet"]:  # Un projet existe
            self.initDepuisProjet(args)
        else:  # Pas encore de projet => première fois
            self.initPremiereFois(args)
        self.verticalLayout.addSpacerItem(QSpacerItem(150, 10, QSizePolicy.Expanding))


    def undo(self):
        '''
        Lors du clic sur le bouton Undo, permet de supprimer le dernier ROI créé
        :return:
        '''
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
        '''
        Lors du déplacement du slider, affiche l'image correspondante
        :return:
        '''
        if hasattr(self,'sourceImages'):  # Pour éviter une erreur lors de l'initialisation
            indImg = self.imageSlider.value()
            idImg, img = self.sourceImages.imageCourante(indImg)
            if img is not None:
                self.lesImages.append(Image(idImg, indImg))
                self.lblImage.afficherImage(img)
                self.lblIndFrame.setText(str(self.imageSlider.value()))

    def selectSource(self):
        '''
        Choix de la source d'images (vidéo ou répertoire)
        :return:
        '''
        if self.param.video:  # On va lire depuis une vidéo
            self.sourceImages = SourceImagesVideo(self.param.fichierOuRepertoire)
        else:
            self.sourceImages = SourceImagesFichier(self.param.fichierOuRepertoire)
        self.imageSlider.setMaximum(self.sourceImages.nbFrames)
        self.lblNbFrames.setText(str(self.imageSlider.maximum()))

    def changerParam(self):
        '''
        Lors de l'appui sur le bouton Paramètres, permet de changer les dimensions du ROI et la source des images
        :return:
        '''
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
        '''
        Initialisation des boutons de classe en cas de première fois (pas encore de projet).
        :param args: Les paramètres de la ligne de commande. Permet de récupérer le nb de classes à créer
        :return:
        '''
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
        '''
        Initialisation des boutons de classe en cas de projet déjà existant (donc on a mémorisé dans le fichier 'param'
        les caractéristiques des ROI et la source des images) et dans 'images' les images et leurs ROI.
        :param args: Les paramètres de la ligne de commande. Permet de récupérer le répertoire contenant les fichiers 'param' et 'images'
        :return:
        '''
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

    def make_calluser(self, classe):
        """
        Appelée lors d'un clic sur un bouton de changement de classe
        :param classe: la nouvelle classe courante (celle qui servira pour les futurs ROI)
        :return:
        """
        def calluser():
            self.changeClasseCourante(classe)
        return calluser

    def changeClasseCourante(self, classe):
        '''
        Mémorise que classe devient la classe courante, celle qui sera associée à tous les futurs ROI créés
        :param classe: la classe à mémoriser
        :return:
        '''
        self.laClasseCourante = classe
        self.lblImage.changeClasse(classe)
        # Mise à jour de l'IHM pour indiquer la nouvelle classe courante
        self.lblClasseCourante.setText(self.laClasseCourante.nom)
        self.lblClasseCourante.setStyleSheet("background-color: %s " % self.laClasseCourante.couleur)

    def ajoutBoutonClasse(self,laClasse):
        '''
        Création dynamique des boutons permettant de sélectionner le type de classe pour les futurs ROI.
        :param laClasse: la classe qui sera associée aux futurs ROI que l'on va créer
        :return:
        '''
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
        '''
        Appelé lors de la réception du signal 'nouveauPoint' venant de WidgetImage quand un nouveau point a été cliqué
        et donc qu'il faut créer le ROI correspondant.
        :param x: coord x (en pixel) du clic
        :param y: coord y (en pixel) du clic
        :return:
        '''
        imgCourante = self.lesImages[-1]
        imgCourante.lesROI.append(ROI(x,y,self.laClasseCourante))
        # Màj du compteur de cette classe
        numClasse = self.laClasseCourante.numero
        nbEltDansClasse = int(self.lesLabelsCompteurs[numClasse].text())
        nbEltDansClasse += 1
        self.lesLabelsCompteurs[numClasse].setText(str(nbEltDansClasse))

    def imageSuivante(self):
        '''
        Suite à l'appui sur le bouton >, récupère depuis la source et affiche l'image suivante
        :return:
        '''
        idImg, img = self.sourceImages.imageSuivante()
        if img is not None:
            self.imageSlider.setValue(self.imageSlider.value()+1)
            self.lesImages.append(Image(idImg,self.imageSlider.value()))
            self.lblImage.afficherImage(img)
            self.lblIndFrame.setText(str(self.imageSlider.value()))

    def imagePrecedente(self):
        '''
        Suite à l'appui sur le bouton <, récupère depuis la source et affiche l'image précédente
        :return:
        '''
        idImg, img = self.sourceImages.imagePrecedente()
        if img is not None:
            self.imageSlider.setValue(self.imageSlider.value() - 1)
            self.lesImages.append(Image(idImg,self.imageSlider.value()))
            self.lblImage.afficherImage(img)
            self.lblIndFrame.setText(str(self.imageSlider.value()))

    def closeEvent(self, event):
        '''
        lors de la fermeture de la fenêtre, propose la sauvegarde du travail dans 2 fichiers : 'param' et 'images'
        :param event:
        :return:
        '''
        reply = QMessageBox.question(self, 'Message',"Quitter (Y/N) et sauver (Y)?", QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel)
        if reply == QMessageBox.Yes:  # On quitte en sauvant
            self.sauveDansFichier()
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()   # On quitte, mais sans sauver
        else:
            event.ignore()  # On ne quitte pas

    def sauveDansFichier(self):
        '''
        Sauve les données (iamges et ROI) dans le fichier 'images' et les paramètres (ROI et source) dans 'param'
        :return:
        '''
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