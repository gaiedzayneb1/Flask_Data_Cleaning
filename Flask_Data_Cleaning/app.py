import pandas as pd
import numpy as np
import re
from flask import Flask
from flask import jsonify
import os
from flask import Flask
import os

# Créer l'application Flask
app = Flask(__name__)

# Définir le dossier d'upload
upload_folder = "upload"

# Configurer l'application Flask pour utiliser ce dossier pour les uploads
app.config["UPLOAD_FOLDER"] = upload_folder

# Vérifier et créer le dossier d'upload s'il n'existe pas
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])


#app.config : C'est un dictionnaire fourni par Flask pour stocker les configurations de l'application.
# Fonction d'analyse exploratoire des données (EDA)
def EDA(df):
    print(df.head())
    print(df.info())
    print('Les descriptions statistiques:')
    print(df.describe(include='all'))
    print(df.isnull().sum())
    print(df.columns.to_list())
    print(df.value_counts())
# Fonction pour calculer la similarité de Jaccard
def jaccard_similarity(str1, str2):
    if not isinstance(str1, str) or not isinstance(str2, str):
        return 0.0
    set1 = set(str1)
    set2 = set(str2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    if len(union) == 0:
        return 0.0

    return len(intersection) / len(union)

    
  
def nettoyer_article(article,lg):
    # Vérifier le type de donnée de l'article
    if isinstance(article, str):
        mots = article.split()  # Diviser l'article en mots
        mots_nettoyés = [mot for mot in mots if mot != lg]  # Supprimer le mot spécifié (lg)
        article_nettoyé = ' '.join(mots_nettoyés)  # Rejoindre les mots nettoyés en une chaîne
        return article_nettoyé  # Retourner l'article nettoyé
    else:
        return article  # Retourner l'article tel quel si ce n'est pas une chaîne de caractères

def filter_and_save_duplicates(df):
    # Vérifier et créer le dossier d'upload s'il n'existe pas
    
    
    # Identifier les lignes dupliquées basées sur 'Code' et 'IDAr_Couleur'
    duplicated_rows = df[df.duplicated(subset=['Code', 'IDAr_Couleur'], keep=False)]

    # Sélectionner les colonnes souhaitées
    selected_columns = ['IDArticle', 'Article', 'ArticleCleaned', 'IDAr_Couleur', 'Code']
    result = duplicated_rows[selected_columns]

    # Définir le chemin du fichier de sortie en utilisant le chemin du dossier d'upload
    result_filepath = os.path.join(upload_folder, 'duplicated_rows.csv')

    # Sauvegarder le résultat dans un nouveau fichier CSV
    result.to_csv(result_filepath, index=False)

    return result_filepath


    
def load_data():
    path_main = "content/input/nafArticle-9-23.csv (2)/nafArticle-9-23.csv"
    path_couleur = "content/input/ArCouleurNaf.csv/ArCouleurNaf.csv"
    path_grille = "content/input/GrilleTailleNaf.csv/GrilleTailleNaf.csv"

    df = pd.read_csv(path_main)
    df_couleur = pd.read_csv(path_couleur)
    df_grille = pd.read_csv(path_grille)
    return df, df_couleur, df_grille
def clean_main_data(df):
    # Opérations de nettoyage spécifiques aux données principales
    columns_to_drop = [
        'Image', 'ReferenceFssr', 'BaseStylisme', 'Dimensions', 'IDFournisseur',
        'ReseauArt', 'IDFibreComposition', 'PoidsBrut', 'IDSaison', 'TauxTVA', 'IDAr_Theme',
        'PrixAchat', 'PieceCarton', 'PrixOutlet', 'DateValidationNomenclature', 'Composition',
        'NbrPiecesColis', 'NomenclatureValide', 'NomenclatureValidePar', 'Boutonnage', 'Emballage',
        'DateMEP', 'ArticleLong', 'Poids Emballage', 'Code Douane', 'Observations', 'CompositionMatiere',
        'PoidsEmballage', 'NumInterne', 'IDSupportArticle', 'SupportArt'
    ]
    
    # Vérifier l'existence des colonnes à supprimer dans le DataFrame
    columns_to_drop_existing = [col for col in columns_to_drop if col in df.columns]
    
    # Supprimer les colonnes existantes
    df_cleaned = df.drop(columns=columns_to_drop_existing)
    
    return df_cleaned


    df_cleaned['SaisiPar'].fillna('inconnu', inplace=True)
    df_cleaned['SaisiPar'].replace({
        'SUPERVISEUR': 'superviseur', 'superviseur ': 'superviseur', 'SUPERVISEUR ': 'superviseur',
        'Benameur.Yassin': 'Benameur.yassin', 'Pascale baubois': 'Pascale Baubois'
    }, inplace=True)

    df_cleaned['ModifiePar'].fillna('inconnu', inplace=True)
    df_cleaned['ModifiePar'].replace({
        'SUPERVISEUR': 'superviseur', 'superviseur ': 'superviseur', 'SUPERVISEUR ': 'superviseur',
        'Benameur.Yassin': 'Benameur.yassin', 'Pascale baubois': 'Pascale Baubois',
        'Päscale baubois': 'Pascale Baubois'
    }, inplace=True)

    for col in df_cleaned.columns:
        if len(df_cleaned[col].unique()) == 1 and df_cleaned[col].unique()[0] == 0:
            df_cleaned.drop(columns=col, inplace=True)

    df_cleaned.dropna(subset=['Article'], inplace=True)
    df_cleaned = df_cleaned[(df_cleaned['PrixFac'] != 0) & (df_cleaned['PoidsNet'] != 0)]

    return df_cleaned

def get_invalid_codes_info(df):
    # Modèle d'expression régulière pour vérifier le format des codes
    pattern = re.compile(r'^[A-Za-z]{2,5}\d{2,3}[A-Za-z]$')
    
    # Liste des codes invalides qui ne correspondent pas au modèle
    invalid_codes = [code for code in df['Code'] if not pattern.match(code)]
    return invalid_codes
    
    


def find_invalid_codes(df):
    invalid_codes=get_invalid_codes_info(df)
    pattern = re.compile(r'^[A-Za-z]{2,5}\d{2,3}[A-Za-z]$')
    invalid_data_codes = df.loc[df['Code'].isin(invalid_codes), ['Code', 'IDArticle', 'IDAr_Couleur']]
    return invalid_data_codes

#creation de fichier des codes invalides

def analyze_sizes(df_grille):
    sizes=[]
    df_grille1 = df_grille[df_grille['LibTailleFR'].notna() & df_grille['LibTailleMX'].notna()]
    sizes .append(df_grille1['LibTailleFR'].unique())
    sizes .append( df_grille1['LibTailleEU'].unique())
    sizes .append(df_grille1['LibTailleIT'].unique())
    sizes .append( df_grille1['LibTailleUK'].unique())
    sizes .append(df_grille1['LibTailleMX'].unique())
    sizes .append(df_grille1['LibTailleRUS'].unique())
      
    
   
    return sizes

def analyze_colors(df_couleur):
    colors=[]

    colors.append(df_couleur['Couleur'].unique())
    return colors

def finalize_data_operations(df,lg):
    df['ArticleCleaned'] = df['Article'].apply(lambda x: nettoyer_article(x, lg))

    
    for index, row in df.iterrows():
        code = row['Code']
        reference = row['Reference']
        if isinstance(code, str) and isinstance(reference, str):
            similarity = jaccard_similarity(code, reference)
            df.loc[index, 'Similar'] = similarity >= 0.85
        else:
            df.loc[index, 'Similar'] = False
    invalid_codes=get_invalid_codes_info(df)
    df_duplicates = df[(df['Code'].isin(invalid_codes)) & (df['Similar'])]
    print(df_duplicates[['Code', 'Reference']])

    result_filepath = filter_and_save_duplicates(df)
    return result_filepath
from flask import jsonify, request, Flask

app = Flask(__name__)

@app.route('/clean', methods=['POST'])
def clean():
    try:
       
        # Charger les données à partir des fichiers CSV
        df, df_couleur, df_grille = load_data()

        # Nettoyer et préparer les données principales
        df_cleaned = clean_main_data(df)

        # Identifier et gérer les codes invalides
        invalid_codes = find_invalid_codes(df_cleaned)

        # Créer un dictionnaire à partir des données invalides
        invalid_json = {
            'invalid_codes': invalid_codes.to_dict(orient='records')
        }

        # Effectuer des analyses supplémentaires sur les tailles
        sizes=analyze_sizes(df_grille)

        # Analyser les couleurs
        colors=analyze_colors(df_couleur)
        lg=colors+sizes

        # Effectuer des opérations finales sur les données nettoyées
        result_filepath = finalize_data_operations(df_cleaned,lg)

        # Retourner la réponse JSON
        return jsonify(invalid_json)

    except Exception as e:
        # Gestion des erreurs avec un message approprié
        return jsonify({'error': str(e)})





if __name__ == '__main__':
    

    # Démarrer l'application Flask en mode debug
    app.run(debug=True)
    print("API started!")

