# API Documentation

## Endpoints

### `/clean`
- **Method**: POST
- **URL**: http://127.0.0.1:5000/clean
- **Description**: Nettoyer les fichiers CSV fournis et retourne un fichier CSV avec les codes invalides.

#### Request Body:
- `file1`: 
  - **Description**: Fichier CSV principal contenant les informations des articles.
  - **Format**: UTF-8, séparé par des virgules.
  - **Exemple**: `nafArticle-9-23.csv`
- `file2`: 
  - **Description**: Fichier CSV contenant les informations des couleurs.
  - **Format**: UTF-8, séparé par des virgules.
  - **Exemple**: `ArCouleurNaf.csv`
- `file3`: 
  - **Description**: Fichier CSV contenant les informations des tailles.
  - **Format**: UTF-8, séparé par des virgules.
  - **Exemple**: `GrilleTailleNaf.csv`

#### Response:
- **Success**: 
  - **Description**: Un fichier JSON avec les codes invalides.
  - **Example**:
    ```json
    {
      "invalid_codes": [
        {
          "Code": "LHNR162AD",
          "IDAr_Couleur": 433,
          "IDArticle": 3357
        }
      ]
    }
    ```

- **Error**:
  - **Description**: Message d'erreur approprié.
  - **Example**:
    ```json
    {
      "error": "Description de l'erreur"
    }
    ```

### Example 
```bash
curl -X POST -F "file1=@path/to/nafArticle-9-23.csv" -F "file2=@path/to/ArCouleurNaf.csv" -F "file3=@path/to/GrilleTailleNaf.csv" http://127.0.0.1:5000/clean
