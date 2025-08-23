# Admin Assistant OCR

Système intelligent de reconnaissance et d'organisation automatique de documents PDF.

## 🎯 Fonctionnalités

- **OCR Automatique** : Extraction de texte depuis les PDFs scannés
- **Renommage Intelligent** : Analyse du contenu pour extraire :
  - Date du document (format YYYYMMDD)
  - Nom du fournisseur/émetteur
  - Numéro de facture/référence
- **Organisation Structurée** : Conservation de la structure des dossiers (scan → output)
- **Traitement en Masse** : Multithreading pour traiter plusieurs documents simultanément

## 📁 Structure du Projet

```
admin-assistant-ocr/
├── run_windows.bat     # Lancer l'application (Windows)
├── main.py            # Point d'entrée
├── requirements.txt   # Dépendances Python
├── docs/             # Documentation
├── scripts/          # Scripts d'installation
├── src/              # Code source
│   ├── config/       # Configuration
│   ├── controllers/  # Logique métier
│   └── utils/        # Utilitaires
├── scan/            # Dossier d'entrée (PDFs à traiter)
│   └── HN/          # Sous-dossiers par catégorie
├── output/          # Dossier de sortie (PDFs renommés)
└── logs/            # Fichiers de log
```

## 🚀 Installation Rapide

### Windows

1. Installer les prérequis (Python, Tesseract, Poppler)
2. Lancer l'installation :
   ```cmd
   scripts\install_windows.bat
   ```
3. Placer vos PDFs dans `scan\HN\`
4. Lancer le traitement :
   ```cmd
   run_windows.bat
   ```

📖 Guide complet : [docs/INSTALLATION_WINDOWS.md](docs/INSTALLATION_WINDOWS.md)

## 🔧 Configuration

Modifier `src/config/config.json` :

```json
{
  "scan_folder": "scan",
  "sub_folders": ["HN", "Factures", "Courriers"],
  "output_folder": "output"
}
```

## 📝 Format de Sortie

Les PDFs sont renommés automatiquement selon le format :
```
YYYYMMDD_NomFournisseur_NumeroFacture.pdf
```

Exemples :
- `20240315_EDF_FAC2024001.pdf`
- `20240122_Orange_Mobile_REF123456.pdf`
- `20240201_SARL_Dupont_DEVIS789.pdf`

## 🎨 Fonctionnement

1. **Scan** : Le système parcourt les dossiers configurés
2. **OCR** : Extraction du texte de chaque page du PDF
3. **Analyse** : Identification automatique des métadonnées :
   - Recherche de dates (multiples formats supportés)
   - Détection du fournisseur (mots-clés, en-tête)
   - Extraction du numéro de référence
4. **Organisation** : Copie du PDF avec nouveau nom dans la structure de sortie

## 📊 Logs

Les logs sont disponibles dans `logs/` avec :
- Niveau INFO dans la console
- Niveau DEBUG dans les fichiers
- Horodatage et traçabilité complète

## 🛠️ Technologies

- **Python 3.9+**
- **Tesseract OCR** : Moteur de reconnaissance optique
- **Poppler** : Conversion PDF vers images
- **pytesseract** : Interface Python pour Tesseract
- **pdf2image** : Conversion des PDFs
- **Pillow** : Traitement d'images