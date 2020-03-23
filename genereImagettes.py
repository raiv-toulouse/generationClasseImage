# -*- coding: utf-8 -*-
import pickle,argparse,os,cv2
from utilitaires import Classe,ROI,Image,Param
from sourceImagesFichier import SourceImagesFichier
from sourceImagesVideo import SourceImagesVideo

parser = argparse.ArgumentParser()
parser.add_argument("repProjet", help="répertoire du projet")
args = parser.parse_args()
repertoireProjet = args.repProjet
# Lecture du fichier des images
fichImages = open(repertoireProjet+"/images","rb")
lesImages = pickle.load(fichImages)
fichImages.close()
# Lecture du fichier de paramètres
fichParam = open(repertoireProjet+"/param","rb")
param = pickle.load(fichParam)
lesClasses = pickle.load(fichParam)
fichParam.close()
# On va travailler dans le répertoire passé en paramètre
os.chdir(repertoireProjet)
# Création des répertoires pour les classes
dicoIndClasse = {}
for cl in lesClasses:
    if not os.path.exists(cl.nom):
        os.makedirs(cl.nom)
    dicoIndClasse[cl.nom] = 0
print(dicoIndClasse)
# Sélection de la source d'image
if param.video:  # On va lire depuis une vidéo
    sourceImages = SourceImagesVideo(param.fichierOuRepertoire)
else:
    sourceImages = SourceImagesFichier(param.fichierOuRepertoire)
# On traite maintenant image par image (depuis un répertoire d'iamges ou une vidéo)
indImg = 0
for img in lesImages:
    _,image = sourceImages.imageCourante(img.posImg)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(type(gray))
    cv2.imshow('image', gray)
    cv2.waitKey(0)
    # Génération des imagettes (une par ROI)
    for roi in img.lesROI:
        x = roi.x
        y = roi.y
        ymin = y - int(param.hauteurROI/2)
        ymax = y + int(param.hauteurROI/2)
        xmin = x - int(param.largeurROI/2)
        xmax = x + int(param.largeurROI/2)
        imagette = gray[ymin:ymax, xmin:xmax]
        cv2.imwrite(roi.classe.nom+'/'+str(dicoIndClasse[roi.classe.nom])+".png", imagette)
        dicoIndClasse[roi.classe.nom] += 1
print('fini')