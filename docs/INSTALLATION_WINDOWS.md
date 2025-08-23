# Installation sur Windows

## Prérequis

### 1. Python (OBLIGATOIRE)
- Télécharger Python 3.9+ depuis : https://www.python.org/downloads/
- **IMPORTANT** : Cocher "Add Python to PATH" lors de l'installation

### 2. Tesseract OCR (OBLIGATOIRE)
- Télécharger : https://github.com/UB-Mannheim/tesseract/wiki
- Installer dans le dossier par défaut : `C:\Program Files\Tesseract-OCR` ou dans : `C:\Tools\Tesseract-OCR`
- L'application détectera automatiquement Tesseract

### 3. Poppler pour Windows (OBLIGATOIRE pour les PDFs)
- Télécharger : https://github.com/oschwartz10612/poppler-windows/releases
- Extraire dans `C:\Tools\poppler`
- Ajouter `C:\Tools\poppler\Library\bin` au PATH Windows :
  1. Panneau de configuration → Système → Paramètres système avancés
  2. Variables d'environnement → Variable Path → Modifier
  3. Ajouter `C:\Tools\poppler\Library\bin`

## Installation rapide

1. **Cloner ou télécharger le projet**

2. **Ouvrir un terminal Windows (cmd ou PowerShell) dans le dossier du projet**

3. **Lancer l'installation automatique :**
   ```cmd
   install_windows.bat
   ```

4. **Placer vos PDFs dans :** `scan\HN\`

5. **Lancer l'application :**
   ```cmd
   run_windows.bat
   ```

## Installation manuelle

Si le script automatique ne fonctionne pas :

```cmd
# Créer l'environnement virtuel
python -m venv ocr-venv

# Activer l'environnement
ocr-venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Créer les dossiers
mkdir scan\HN
mkdir output
mkdir logs

# Lancer l'application
python main.py
```

## Structure des dossiers

```
admin-assistant-ocr/
├── scan/           # Placer vos PDFs ici
│   └── HN/        # Sous-dossier par défaut
├── output/        # Résultats OCR (fichiers .txt)
├── logs/          # Fichiers de log
└── src/config/    # Configuration
```

## Dépannage

### Erreur "tesseract is not installed"
- Vérifier que Tesseract est installé dans `C:\Program Files\Tesseract-OCR`
- Ou modifier le chemin dans `src/controllers/ocr_controller.py`

### Erreur "No module named 'pdf2image'"
- Vérifier que Poppler est dans le PATH
- Redémarrer le terminal après ajout au PATH

### Erreur "No PDF files found"
- Vérifier que les PDFs sont dans `scan\HN\`
- Vérifier l'extension des fichiers (.pdf en minuscules)

## Configuration

Modifier `src/config/config.json` pour personnaliser :
- `scan_folder` : Dossier de scan
- `sub_folders` : Liste des sous-dossiers à traiter
- `output_folder` : Dossier de sortie