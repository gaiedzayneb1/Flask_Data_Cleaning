# Flask Data Cleaning API

## Description
This project provides a Flask-based API for processing and analyzing CSV files. It includes functions for exploratory data analysis (EDA), duplicate detection, data cleaning, and validation of codes.

## Installation

### Prérequis
- Python 3.6 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation
1. Clonez le dépôt :
    sh
    git clone <url-du-depot>
    cd Flask_Data_Cleaning
  

2. Créez un environnement virtuel et activez-le :
    sh
    python -m venv venv
    # Sous Windows
    venv\Scripts\activate
    # Sous macOS/Linux
    source venv/bin/activate


3. Installez les dépendances :
    sh
    pip install -r requirements.txt
### Structures
PROJECT STAGE/
├── app/         
│   ├── routes.py             
│   ├── _init_.py            
│   └── config.py             
|__content/                
│   |__input
├   |__output              
│   |__static
├── tests/                    
│   ├── _init_.py
│   └── test_routes.py              
├── requirements.txt          
├── README.md  
|__apidocumentation.md                                 
└── app.py                   

### Utilisation
#### Endpoint:/clean
-*Method HTTP*:POST
-*Request Example*:
sh
curl -X POST -F "file1=@path/to/nafArticle-9-23.csv" -F "file2=@path/to/ArCouleurNaf.csv" -F "file3=@path/to/GrilleTailleNaf.csv" http://127.0.0.1:5000/clean

*Response*:
-EN cas     de succès :
json
{
  "invalid_codes": [
    {
      "Code": "LHNR162AD",
      "IDAr_Couleur": 433,
      "IDArticle": 3357
    }
  ]
}
-Réponse en cas d'erreur :
{
  "error": "Description de l'erreur"
}
-Exemples supplémentaires
Scénario : Fichier CSV avec des formats de codes incorrects:
      -*Requête *:
      curl -X POST -F "file1=@path/to/invalid_codes.csv" -F "file2=@path/to/ArCouleurNaf.csv" -F "file3=@path/to/GrilleTailleNaf.csv" http://127.0.0.1:5000/clean
      -*Response*:
      {
  "invalid_codes": [
    {
      "Code": "INVALID123",
      "IDAr_Couleur": 999,
      "IDArticle": 1234
    },
    {
      "Code": "WRONG456",
      "IDAr_Couleur": 888,
      "IDArticle": 5678
    }
  ]
}
Scénario : Erreur de chargement des fichiers CSV:
        -*Requête *:
        curl -X POST -F "file1=@path/to/missing_file.csv" -F "file2=@path/to/ArCouleurNaf.csv" -F "file3=@path/to/GrilleTailleNaf.csv" http://127.0.0.1:5000/clean
         -*Response*:
         {
  "error": "Fichier manquant ou chemin incorrect"
}

        









