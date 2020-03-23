# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi


class DialogParam(QDialog):
    def __init__(self,param):
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
        if self.rbVideo.isChecked():
            fichVideo, _ = QFileDialog.getOpenFileName(self, "Sélectionnez un fichier vidéo")
            self.lblFichierOuRepertoire.setText(fichVideo)
        else:
            rep = QFileDialog.getExistingDirectory(self, "Selectionnez le répertoire des images")
            self.lblFichierOuRepertoire.setText(rep)

    def accept(self):
        try:
            self.param.largeurROI = int(self.edtLargeurROI.text())
            self.param.hauteurROI = int(self.edtHauteurROI.text())
            self.param.video = self.rbVideo.isChecked()  # True si source est vidéo, False si répertoire images
            self.param.fichierOuRepertoire = self.lblFichierOuRepertoire.text()
        except:
            QMessageBox.warning(self, "Erreur de saisie", "Une donnée n'est pas correcte")
        if self.param.fichierOuRepertoire:
            super().accept()
