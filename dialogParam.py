# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class DialogParam(QDialog):
    '''
    Dialog permettant la modification des paramètres : dimensions du ROI et source des images
    '''
    def __init__(self,param):
        '''
        Constructeur
        :param param: objet de class Param (utilitaires.py) servant à mémoriser les dimensions ROI et source des images
        '''
        super(QDialog, self).__init__()
        loadUi('ihm_parametre.ui', self)
        self.btnChoix.clicked.connect(self.choixFichierOuRepertoire)
        self.param = param
        self.lesBoutons.accepted.connect(self.accept)
        self.edtLargeurROI.setText(str(param.largeurROI))
        self.edtHauteurROI.setText(str(param.hauteurROI))
        self.rbVideo.setChecked(self.param.video == True)
        self.rbImages.setChecked(self.param.video == False)
        self.lblFichierOuRepertoire.setText(self.param.fichierOuRepertoire)

    def choixFichierOuRepertoire(self):
        '''
        Après appui sur le bouton de choix de la source, demande un nom de fichier vidéo ou un répertoire d'images
        :return:
        '''
        if self.rbVideo.isChecked():
            fichVideo, _ = QFileDialog.getOpenFileName(self, "Sélectionnez un fichier vidéo")
            self.lblFichierOuRepertoire.setText(fichVideo)
        else:
            rep = QFileDialog.getExistingDirectory(self, "Selectionnez le répertoire des images")
            self.lblFichierOuRepertoire.setText(rep)

    def accept(self):
        '''
        Après appui sur le bouton OK, mémorise dans 'param' les dimensions ROI et source des images
        :return:
        '''
        try:
            self.param.largeurROI = int(self.edtLargeurROI.text())
            self.param.hauteurROI = int(self.edtHauteurROI.text())
            self.param.video = self.rbVideo.isChecked()  # True si source est vidéo, False si répertoire images
            self.param.fichierOuRepertoire = self.lblFichierOuRepertoire.text()
        except:
            QMessageBox.warning(self, "Erreur de saisie", "Une donnée n'est pas correcte")
        if self.param.fichierOuRepertoire:
            super().accept()
