# GenerationClasseImage
Génération d'imagettes pour DeepLearning

##But
A partir d'une vidéo ou d'un répertoire d'images, sélectionnez des ROI que vous affecterez à une classe et qui seront ensuite transformés en imagettes.
Ces imagettes serviront ensuite à l'entrainement d'un réseau de neurones de type DeepLearning.
##Mode d'emploi
Deux applications sont disponibles : 
* **genereClasse** : une vidéo ou une série d'images s'affiche. Vous sélectionnez une classe puis vous cliquez pour mettre des ROI (Region Of Interest) centrées sur vos zones d'intérêt.
* **genereImagettes** : produit effectivement les imagettes à partir des fichiers produits par l'application précédente.

Vous devez installer les modules suivants: 
* PyQt5
* imutils  
* opencv

Exemple sous Ubuntu :
```
sudo apt-get install python3-pyqt5
sudo pip install imutils opencv-contrib-python
```
###genereClasse

####Nouveau projet
Lors de l'utilisation pour un nouveau projet, il faut utiliser l'option -n pour spécifier le nombre de classes que l'on souhaite.
```
python genereClasse -n 2
```
Dans l'exemple ci-dessus, on aura 2 classes, ce qui se traduira par 2 boutons dans la partie droite de l'IHM.

A l'initialisation, la fenêtre de configuration apparait, vous permettant de choisir la taille de vos ROI mais également si votre source d'images sera une vidéo ou un répertoire d'images, qu'il vous faudra renseigner dans les deux cas.

Les boutons de la partie droite peuvent être customisés par :
* clic droit : choix de la couleur (ce sera aussi celle dessinant le ROI)
* double clic gauche : changement du nomm de la classe
* clic gauche : sélection de cette classe qui devient la classe courante (la classe courante est rappelée tout en haut de l'interface)

Une fois les boutons customisés, parcourez les images à l'aide du slider et/ou des 2 boutons < et >.

Sur une image, faites un clic gauche au centre de la zone que vous avez sélectionné comme ROI. Changez au besoin de classe avec les boutons à droite avant de générer un ROI.

Si vous appuyez sur le bouton 'Paramètres', vous pourez modifier la source des images et/ou la taille des ROI mais ATTENTION, si vous validez, vous perdrez tout vos ROI précédemment créés.

Pour quitter l'application, fermez la fenêtre de la façon classique (croix en haut à droite) ce qui aura pour effet de vous demander unrépertoire de sauvegarde pour ce projet où seront sauvés les deux fichier, param et images, qui contiennent tout votre travail.

![alt text](https://github.com/raiv-toulouse/generationClasseImage/blob/master/safra.png "Logo Title Text 1")
####Projet existant
Si votre projet existe déjà et que vous souhaitez juste le compléter (lui ajouter de nouveaux ROI), il faudra utiliser l'option -r et pour cela faites : 
```
python genereClass -r <le répertoire de votre projet>
``` 
L'interface s'ouvre sur la dernière image traitée. Vous n'avez plus qu'à ajouter des ROI puis quitter pour sauvegarder toutes ces données.

###genereImagettes

Cette application, sans IHM, prend en entrée le répertoire contenant les 2 fichiers générés par l'application genereClasses et construit les imagettes correspondant aux ROI spécifiés et les range dans des répertoires, un par classe.*

Un paramètre est obligatoire : le répertoire contenant les 2 fichiers. C'est dans ce répertoire que seront créés les dossiers avec leurs imagettes.

```
python genereImagettes <nom_du_repertore>
```


