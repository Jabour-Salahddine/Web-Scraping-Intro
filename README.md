#   Web Scraping avec Python – TimesJobs

Ce projet a pour objectif de démontrer l'utilisation de **Python** pour effectuer du **web scraping** sur le site [TimesJobs](https://m.timesjobs.com). Le but est de récupérer automatiquement des offres d'emploi en lien avec des compétences spécifiques (comme Python, data, etc.), et de les stocker localement.

---

##   Structure du projet

Voici la structure globale des dossiers et leur rôle :


web_scraping_project/
│
├── venv/
│    Environnement virtuel Python, utilisé pour isoler les bibliothèques nécessaires au projet.
│
├── offres_emploi_python/
│    Dossier contenant les offres d’emploi extraites depuis le site TimesJobs.
│
├── Test With Local File/
│    Dossier contenant un test local avec un fichier HTML statique pour s'entraîner à parser avec BeautifulSoup.
│
├── Scraping A Production Website/
│    Dossier principal du projet contenant le code final de scraping à partir du site réel.
│ └── main.py
│
└── README.md
 Ce fichier de documentation.


 ##  Bibliothèques Python utilisées

Le projet utilise les bibliothèques suivantes :

- [`requests`](https://pypi.org/project/requests/) : Pour envoyer des requêtes HTTP et récupérer le contenu des pages web.

- [`beautifulsoup4`](https://pypi.org/project/beautifulsoup4/) : Pour parser le HTML et extraire les données souhaitées.

- [`lxml`](https://pypi.org/project/lxml/) : Un parseur rapide et efficace pour BeautifulSoup.



Créer un environnement virtuel : 
    python -m venv venv

Activer l’environnement virtuel (sous windows bash) :
    source venv/Scripts/activate

Installer les dépendances : 
    pip install beautifulsoup4 requests lxml

Désactiver l'environnement virtuel : 
    deactivate

