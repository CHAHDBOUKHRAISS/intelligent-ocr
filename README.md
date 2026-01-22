# Intelligent OCR

**A semi-structured document processing system using OCR and semantic extraction**

---

## Table of Contents / Table des Matières

- [English](#english)
  - [Project Description](#project-description)
  - [Objectives](#objectives)
  - [System Architecture](#system-architecture)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Limitations](#limitations)
  - [Future Improvements](#future-improvements)
- [Français](#français)
  - [Description du Projet](#description-du-projet)
  - [Objectifs](#objectifs)
  - [Architecture du Système](#architecture-du-système)
  - [Technologies Utilisées](#technologies-utilisées)
  - [Installation](#installation-1)
  - [Utilisation](#utilisation)
  - [Limitations](#limitations-1)
  - [Améliorations Futures](#améliorations-futures)

---

# English

## Project Description

Intelligent OCR is a functional prototype system designed for processing semi-structured documents, with a primary focus on forms and experimental support for CVs and invoices. The system combines traditional OCR (Optical Character Recognition) techniques with semantic extraction to transform scanned documents into structured, machine-readable data.

The project implements a modular architecture consisting of a FastAPI REST backend, an OCR processing pipeline, and a Streamlit web interface. The system processes documents through multiple stages: image preprocessing, layout detection, text recognition, and semantic field extraction.

## Objectives

The main objectives of this project are:

1. **Document Processing**: Develop a system capable of processing scanned documents (PDFs and images) through an automated OCR pipeline.

2. **Text Extraction**: Extract text content from documents using Tesseract OCR engine with preprocessing optimizations.

3. **Semantic Extraction**: Identify and extract structured information such as names, dates, email addresses, and monetary amounts using natural language processing techniques.

4. **Structured Output**: Provide extracted data in structured formats (JSON and CSV) for further processing and integration.

5. **User Interface**: Offer an intuitive web interface for document upload, processing, and result visualization.

6. **Modular Architecture**: Design a clean, maintainable codebase that allows for future extensions and improvements.

## System Architecture

The system follows a modular, layered architecture:

```
┌─────────────────────────────────────────────────┐
│           Streamlit Web Interface               │
│         (User-facing frontend)                   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│           FastAPI REST Backend                   │
│    (API endpoints, request handling)             │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│            OCR Pipeline                          │
│  ┌──────────────┬──────────────┬──────────────┐│
│  │Preprocessing │  Layout      │  Text        ││
│  │              │  Detection    │  Recognition ││
│  └──────────────┴──────────────┴──────────────┘│
│  ┌─────────────────────────────────────────────┐│
│  │      Semantic Extraction                    ││
│  └─────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

### Components

1. **Preprocessing Module**: Image normalization, noise removal, binarization, and deskewing using OpenCV.

2. **Layout Detection**: Identifies document regions (currently a placeholder for future implementation).

3. **Text Recognition**: OCR text extraction using Tesseract, supporting region-based and full-image extraction.

4. **Semantic Extraction**: Named entity recognition and pattern matching using spaCy for extracting structured fields.

5. **Result Formatting**: Converts extracted data into structured JSON and CSV formats.

6. **API Layer**: RESTful endpoints for document upload, processing, and result retrieval.

7. **Web Interface**: Streamlit-based UI for document upload, preview, and result visualization.

## Technologies Used

### Backend
- **Python 3.8+**: Core programming language
- **FastAPI**: Modern, fast web framework for building REST APIs
- **Uvicorn**: ASGI server for FastAPI

### OCR & Image Processing
- **Tesseract OCR (pytesseract)**: Text recognition engine
- **OpenCV**: Image preprocessing and manipulation
- **Pillow**: Image processing utilities
- **pdf2image**: PDF to image conversion

### Natural Language Processing
- **spaCy**: Named entity recognition and NLP processing

### Web Interface
- **Streamlit**: Rapid web application development framework
- **Requests**: HTTP client for API communication

### Data Validation & Configuration
- **Pydantic**: Data validation and settings management
- **python-dotenv**: Environment variable management

## Installation

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system
  - Windows: Download from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux: `sudo apt-get install tesseract-ocr`
  - macOS: `brew install tesseract`

### Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd OCR_INTELLIGENT
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configure environment** (optional):
   Create a `.env` file in the project root:
   ```env
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

## Usage

### Starting the Backend API

```bash
python scripts/run_api.py
```

The API will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health/`

### Starting the Web Interface

```bash
python scripts/run_web.py
```

The web interface will be available at `http://localhost:8501`

### Using the API Directly

```bash
# Upload and process a document
curl -X POST "http://localhost:8000/documents/upload-and-process" \
  -F "file=@document.pdf" \
  -F "document_type=form" \
  -F "language=eng"
```

## Limitations

This is a functional prototype with the following limitations:

1. **Layout Detection**: The layout detection module is currently a placeholder. The system processes documents without advanced layout analysis, which may affect accuracy for complex documents.

2. **Document Types**: While the system targets forms, CVs, and invoices, the semantic extraction is generic and may not capture document-specific structures optimally.

3. **Language Support**: Currently supports English, French, and Arabic, but semantic extraction is primarily optimized for English.

4. **Accuracy**: OCR accuracy depends on document quality. Poor quality scans, handwritten text, or complex layouts may result in lower extraction accuracy.

5. **Scalability**: The current implementation processes documents synchronously. Large files or high concurrent loads may impact performance.

6. **Error Handling**: While basic error handling is implemented, the system may not gracefully handle all edge cases or malformed documents.

7. **Model Limitations**: The spaCy model used is a small model (`en_core_web_sm`), which provides good performance but may have limitations in entity recognition accuracy compared to larger models.

## Future Improvements

Potential areas for enhancement:

1. **Advanced Layout Detection**: Implement deep learning-based layout detection models (e.g., LayoutLM, Detectron2) for better region identification.

2. **Document-Specific Extractors**: Develop specialized extraction logic for forms, CVs, and invoices with domain-specific field recognition.

3. **Multi-language Support**: Expand semantic extraction support for multiple languages with appropriate spaCy models.

4. **Asynchronous Processing**: Implement background job processing for large documents and batch operations.

5. **Database Integration**: Add persistent storage for processed documents and results.

6. **User Management**: Implement authentication and user-specific document management.

7. **Advanced Preprocessing**: Add more sophisticated image enhancement techniques and document-specific preprocessing pipelines.

8. **Confidence Thresholds**: Implement configurable confidence thresholds for filtering low-quality extractions.

9. **Validation Rules**: Add rule-based validation for extracted fields (e.g., email format validation, date range checks).

10. **Export Formats**: Support additional export formats (XML, Excel) and custom templates.

---

# Français

## Description du Projet

Intelligent OCR est un prototype fonctionnel conçu pour le traitement de documents semi-structurés, avec un focus principal sur les formulaires et un support expérimental pour les CV et factures. Le système combine des techniques OCR (Reconnaissance Optique de Caractères) traditionnelles avec l'extraction sémantique pour transformer des documents scannés en données structurées et lisibles par machine.

Le projet implémente une architecture modulaire composée d'un backend REST FastAPI, d'un pipeline de traitement OCR, et d'une interface web Streamlit. Le système traite les documents à travers plusieurs étapes : prétraitement d'image, détection de mise en page, reconnaissance de texte, et extraction de champs sémantiques.

## Objectifs

Les objectifs principaux de ce projet sont :

1. **Traitement de Documents** : Développer un système capable de traiter des documents scannés (PDFs et images) à travers un pipeline OCR automatisé.

2. **Extraction de Texte** : Extraire le contenu textuel des documents en utilisant le moteur OCR Tesseract avec des optimisations de prétraitement.

3. **Extraction Sémantique** : Identifier et extraire des informations structurées telles que les noms, dates, adresses email, et montants monétaires en utilisant des techniques de traitement du langage naturel.

4. **Sortie Structurée** : Fournir les données extraites dans des formats structurés (JSON et CSV) pour un traitement et une intégration ultérieurs.

5. **Interface Utilisateur** : Offrir une interface web intuitive pour l'upload de documents, le traitement, et la visualisation des résultats.

6. **Architecture Modulaire** : Concevoir une base de code propre et maintenable qui permet des extensions et améliorations futures.

## Architecture du Système

Le système suit une architecture modulaire en couches :

```
┌─────────────────────────────────────────────────┐
│        Interface Web Streamlit                   │
│         (Frontend utilisateur)                   │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│        Backend REST FastAPI                     │
│    (Points d'API, gestion des requêtes)         │
└──────────────────┬──────────────────────────────┘
                   │
┌──────────────────▼──────────────────────────────┐
│            Pipeline OCR                         │
│  ┌──────────────┬──────────────┬──────────────┐│
│  │Prétraitement │  Détection   │  Reconnaissance││
│  │              │  de Mise en  │  de Texte     ││
│  │              │  Page        │               ││
│  └──────────────┴──────────────┴──────────────┘│
│  ┌─────────────────────────────────────────────┐│
│  │      Extraction Sémantique                ││
│  └─────────────────────────────────────────────┘│
└──────────────────────────────────────────────────┘
```

### Composants

1. **Module de Prétraitement** : Normalisation d'image, suppression du bruit, binarisation, et correction de l'inclinaison en utilisant OpenCV.

2. **Détection de Mise en Page** : Identifie les régions du document (actuellement un placeholder pour une implémentation future).

3. **Reconnaissance de Texte** : Extraction de texte OCR en utilisant Tesseract, supportant l'extraction par région et sur image complète.

4. **Extraction Sémantique** : Reconnaissance d'entités nommées et correspondance de motifs en utilisant spaCy pour extraire des champs structurés.

5. **Formatage des Résultats** : Convertit les données extraites en formats structurés JSON et CSV.

6. **Couche API** : Points d'extrémité RESTful pour l'upload de documents, le traitement, et la récupération des résultats.

7. **Interface Web** : Interface utilisateur basée sur Streamlit pour l'upload de documents, la prévisualisation, et la visualisation des résultats.

## Technologies Utilisées

### Backend
- **Python 3.8+** : Langage de programmation principal
- **FastAPI** : Framework web moderne et rapide pour construire des APIs REST
- **Uvicorn** : Serveur ASGI pour FastAPI

### OCR et Traitement d'Image
- **Tesseract OCR (pytesseract)** : Moteur de reconnaissance de texte
- **OpenCV** : Prétraitement et manipulation d'images
- **Pillow** : Utilitaires de traitement d'image
- **pdf2image** : Conversion PDF en image

### Traitement du Langage Naturel
- **spaCy** : Reconnaissance d'entités nommées et traitement NLP

### Interface Web
- **Streamlit** : Framework de développement rapide d'applications web
- **Requests** : Client HTTP pour la communication API

### Validation de Données et Configuration
- **Pydantic** : Validation de données et gestion des paramètres
- **python-dotenv** : Gestion des variables d'environnement

## Installation

### Prérequis

- Python 3.8 ou supérieur
- Tesseract OCR installé sur votre système
  - Windows : Télécharger depuis [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
  - Linux : `sudo apt-get install tesseract-ocr`
  - macOS : `brew install tesseract`

### Configuration

1. **Cloner le dépôt** :
   ```bash
   git clone <repository-url>
   cd OCR_INTELLIGENT
   ```

2. **Créer un environnement virtuel** :
   ```bash
   python -m venv venv
   source venv/bin/activate  # Sur Windows: venv\Scripts\activate
   ```

3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Télécharger le modèle de langue spaCy** :
   ```bash
   python -m spacy download en_core_web_sm
   ```

5. **Configurer l'environnement** (optionnel) :
   Créer un fichier `.env` à la racine du projet :
   ```env
   API_HOST=0.0.0.0
   API_PORT=8000
   ```

## Utilisation

### Démarrer l'API Backend

```bash
python scripts/run_api.py
```

L'API sera disponible à `http://localhost:8000`
- Documentation API : `http://localhost:8000/docs`
- Vérification de santé : `http://localhost:8000/health/`

### Démarrer l'Interface Web

```bash
python scripts/run_web.py
```

L'interface web sera disponible à `http://localhost:8501`

### Utiliser l'API Directement

```bash
# Uploader et traiter un document
curl -X POST "http://localhost:8000/documents/upload-and-process" \
  -F "file=@document.pdf" \
  -F "document_type=form" \
  -F "language=eng"
```

## Limitations

Ceci est un prototype fonctionnel avec les limitations suivantes :

1. **Détection de Mise en Page** : Le module de détection de mise en page est actuellement un placeholder. Le système traite les documents sans analyse de mise en page avancée, ce qui peut affecter la précision pour les documents complexes.

2. **Types de Documents** : Bien que le système cible les formulaires, CVs et factures, l'extraction sémantique est générique et peut ne pas capturer de manière optimale les structures spécifiques aux documents.

3. **Support des Langues** : Supporte actuellement l'anglais, le français et l'arabe, mais l'extraction sémantique est principalement optimisée pour l'anglais.

4. **Précision** : La précision OCR dépend de la qualité du document. Des scans de mauvaise qualité, du texte manuscrit, ou des mises en page complexes peuvent entraîner une précision d'extraction plus faible.

5. **Scalabilité** : L'implémentation actuelle traite les documents de manière synchrone. Les fichiers volumineux ou les charges concurrentes élevées peuvent impacter les performances.

6. **Gestion des Erreurs** : Bien qu'une gestion d'erreurs de base soit implémentée, le système peut ne pas gérer gracieusement tous les cas limites ou documents malformés.

7. **Limitations du Modèle** : Le modèle spaCy utilisé est un petit modèle (`en_core_web_sm`), qui offre de bonnes performances mais peut avoir des limitations en précision de reconnaissance d'entités par rapport aux modèles plus grands.

## Améliorations Futures

Domaines potentiels d'amélioration :

1. **Détection de Mise en Page Avancée** : Implémenter des modèles de détection de mise en page basés sur l'apprentissage profond (ex. LayoutLM, Detectron2) pour une meilleure identification des régions.

2. **Extracteurs Spécifiques aux Documents** : Développer une logique d'extraction spécialisée pour les formulaires, CVs et factures avec reconnaissance de champs spécifiques au domaine.

3. **Support Multi-langue** : Étendre le support d'extraction sémantique pour plusieurs langues avec les modèles spaCy appropriés.

4. **Traitement Asynchrone** : Implémenter le traitement de tâches en arrière-plan pour les documents volumineux et les opérations par lots.

5. **Intégration de Base de Données** : Ajouter un stockage persistant pour les documents traités et les résultats.

6. **Gestion des Utilisateurs** : Implémenter l'authentification et la gestion de documents spécifique aux utilisateurs.

7. **Prétraitement Avancé** : Ajouter des techniques d'amélioration d'image plus sophistiquées et des pipelines de prétraitement spécifiques aux documents.

8. **Seuils de Confiance** : Implémenter des seuils de confiance configurables pour filtrer les extractions de faible qualité.

9. **Règles de Validation** : Ajouter une validation basée sur des règles pour les champs extraits (ex. validation du format email, vérification des plages de dates).

10. **Formats d'Export** : Supporter des formats d'export supplémentaires (XML, Excel) et des modèles personnalisés.

---

## License

This project is open source and available for educational and research purposes.

## Contact

For questions or contributions, please open an issue on GitHub.
