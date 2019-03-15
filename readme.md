# EuropresseToLexico

Script python 3.6 permettant d'exporter un fichier HTML produit par le service [Europresse](https://fr.wikipedia.org/wiki/Europresse_(Internet)) vers des fichiers de corpus lexicométriques compatiables avec les logiciels [Lexico](http://www.lexi-co.com/), [Iramuteq](http://www.iramuteq.org/) et [TXM](http://textometrie.ens-lyon.fr/).

## Fonctionnalités

* Le script parcourt le fichier HTML produit par Europresse afin de récupérer pour chaque article :
  * le titre du journal
  * le titre de l'article
  * le nom de l'auteur lorsqu'il est mentionné
  * la date de publication de l'article
  * le contenu de l'article
* Ces différents éléments sont nettoyés et formatés afin d'éviter des erreurs d'importation dans les logiciles de lexicométrie.
* Il est possible d'exporter au format Lexico, Iramuteq et en XML pour TXM.

## Installation

1. Cloner le dépôt :
`git clone https://framagit.org/leodumont/EuropresseToLexico.git`
2. Se déplacer dans le répertoire du script :
`cd EuropresseToLexico`
3. Installer les dépendances avec pip :
`pip3 install -r requirements.txt`

## Utilisation

* Appel du script :
`python3 EuropresseToLexico.py`
* il faut alors indiquer le chemin vers le fichier HTML Europresse
* un fichier de corpus est produit à la fin de l'exécution du script.