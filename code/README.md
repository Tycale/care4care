## Virtual environement

Etant donné que nous allons utiliser des ressources extérieures. Afin d'éviter de devoir les installer manuellement à chaque fois et sur le système de tout le monde à la racine, nous utiliserons un environement virtuel et pip.

Ces outils permettent d'installer des paquets facilement sur votre système à un endroit précis.

##Création de l'environnement virtuel

Dans le dossier nommé "code", lancez la commande :

  pyvenv venv

##Activation de l'environnement virtuel

Pour activer l'environement :

  source ./venv/bin/activate

Quand l'environnement est activé, la chaîne de caractères "(venv) " doit apparaitre devant votre prompt.

##Mise à jour des dépendances

Pour installer les dépendances du projet, après avoir activé le venv, lancez :

  pip install -r requirements.txt

Afin d'installer une nouvelle dépendance X, utilisez :

  pip install X
  pip freeze > requirements.txt

N'oubliez pas ensuite d'envoyer vos changements sur le git :

  git commit -a
  git push

##Mettre à jour la base de donnée

Une fois que vous avez toutes les dépendances, il vous faut créer la base de donnée de l'application. En testing, on utilise SQLite comme gestionnaire de base de donnée. C'est simplement un fichier. Afin de créer ce dernier, rendez-vous dans le dossier care4care et exécutez la commande suivante :

  ./manage.py syncdb

ou

  python manage.py syncdb


##Lancer le serveur de développement

Dans le dossier care4care :

  ./manage.py runserver

Vous pouvez désormais accéder au serveur web de production sur http://localhost:8000/ !
