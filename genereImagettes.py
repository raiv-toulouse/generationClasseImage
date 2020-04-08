# -*- coding: utf-8 -*-
import pickle,argparse,os,cv2
from utilitaires import Classe,ROI,Image,Param
from sourceImagesFichier import SourceImagesFichier
from sourceImagesVideo import SourceImagesVideo

#
# Depuis le répertoire du projet contenant les fichiers produits par genereClasses ('param' et 'images'),
# génère les imagettes correspondant aux ROI des différentes images.
#
# python genereImagettes <repertoire_du_projet> [-lROI <largeur_ROI> -hROI <hauteur_ROI>]
#
parser = argparse.ArgumentParser()
parser.add_argument("repProjet", help="répertoire du projet")
parser.add_argument("-lROI", type=int,  help="largeur du ROI")
parser.add_argument("-hROI", type=int,  help="hauteur du ROI")
# Indique que le fichier doit être pris dans le répertoire courant, pas dans celuid'origine.
parser.add_argument("-r", help="fichier dans répertoire", action="store_true")
parser.add_argument("-e", help="egalisation d'histogramme", action="store_true")
args = parser.parse_args()
repertoireProjet = args.repProjet
# Lecture du fichier des images
fichImages = open(repertoireProjet+"/images","rb")
lesImages = pickle.load(fichImages)
fichImages.close()
# Lecture du fichier de paramètres
fichParam = open(repertoireProjet+"/param","rb")
param = pickle.load(fichParam)
# Si le paramètre in est défini, alors on va chercher les fichiers dans le répertoire courant
if args.r:
    param.fichierOuRepertoire = repertoireProjet+"/"+os.path.basename(param.fichierOuRepertoire)
lesClasses = pickle.load(fichParam)
fichParam.close()
# On prend en compte les éventuelles valeurs de largeur et hauteur pouur les ROI
if args.lROI:
    param.largeurROI = args.lROI
if args.hROI:
    param.hauteurROI = args.hROI
# On va travailler dans le répertoire passé en paramètre
os.chdir(repertoireProjet)
# Création des répertoires pour les classes
dicoIndClasse = {}
for cl in lesClasses:
    if not os.path.exists(cl.nom):
        os.makedirs(cl.nom)
    dicoIndClasse[cl.nom] = 0
# Sélection de la source d'image
if param.video:  # On va lire depuis une vidéo
    sourceImages = SourceImagesVideo(param.fichierOuRepertoire)
else:
    sourceImages = SourceImagesFichier(param.fichierOuRepertoire)
# On traite maintenant image par image (depuis un répertoire d'images ou une vidéo)
indImg = 0
for img in lesImages:
    _,image = sourceImages.imageCourante(img.posImg)
    (hautImage,largImage,_) = image.shape
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if args.e:  # On veut faire une égalisation d'histogramme
        gray = cv2.equalizeHist(gray)
    # cv2.imshow('image', gray)  # Pour DEBUG
    # cv2.waitKey(0)
    # Génération des imagettes (une par ROI)
    for roi in img.lesROI:
        x = roi.x
        y = roi.y
        ymin = y - int(param.hauteurROI/2)
        ymax = y + int(param.hauteurROI/2)
        xmin = x - int(param.largeurROI/2)
        xmax = x + int(param.largeurROI/2)
        if xmin >= 0 and ymin >= 0 and xmax < largImage and ymax < hautImage: # Aucune dimension ne sort de l'image
            imagette = gray[ymin:ymax, xmin:xmax]
            cv2.imwrite(roi.classe.nom+'/'+str(dicoIndClasse[roi.classe.nom])+".png", imagette)
            dicoIndClasse[roi.classe.nom] += 1
print('fini')