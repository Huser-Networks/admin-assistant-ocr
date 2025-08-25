# Structure du Projet OCR Assistant

## Organisation des Dossiers

```
admin-assistant-ocr/
│
├── launch.bat           # Lanceur principal Windows
├── launch.py           # Lanceur principal Python (multi-plateforme)
├── install.bat         # Installation complète Windows
├── main.py            # Script principal OCR
├── requirements.txt   # Dépendances Python
│
├── gui/               # Interface graphique
│   └── ocr_gui.py    # Application Tkinter
│
├── bin/              # Scripts de lancement archivés
│   ├── launch_gui.bat
│   └── launch_gui.py
│
├── installers/       # Scripts d'installation
│   ├── install_all.bat
│   ├── install_dependencies.py
│   └── create_desktop_shortcut.py
│
├── scripts/          # Scripts utilitaires
│   ├── configure_hierarchical.py
│   ├── review_results.py
│   └── ...
│
├── src/              # Code source principal
│   ├── controllers/  # Contrôleurs (OCR, fichiers, config)
│   ├── extractors/   # Extracteurs modulaires
│   ├── utils/        # Utilitaires
│   └── config/       # Configuration
│
├── docs/             # Documentation
│   ├── MANUEL_UTILISATEUR.md
│   ├── INSTALLATION_WINDOWS.md
│   └── ...
│
├── logs/             # Fichiers de logs
├── scan/             # Dossiers à scanner (créés automatiquement)
├── output/           # Résultats OCR (créés automatiquement)
└── ocr-venv/         # Environnement virtuel Python
```

## Utilisation

### Installation (première fois)
```bash
# Windows
install.bat

# Ou manuellement
python -m venv ocr-venv
ocr-venv\Scripts\activate
pip install -r requirements.txt
```

### Lancement
```bash
# Windows - Double-cliquez sur:
launch.bat

# Ou en ligne de commande:
python launch.py
```

## Points Importants

1. **Environnement Virtuel**: Toujours utiliser `ocr-venv` pour éviter les conflits
2. **Lanceurs**: Utilisent automatiquement le bon environnement
3. **GUI**: Se trouve dans le dossier `gui/`
4. **Installation**: Le script `install.bat` configure tout automatiquement

## Dépendances Système

- **Python 3.8+**: Requis
- **Tesseract OCR**: Installer dans `C:\Tools\Tesseract-OCR` ou `C:\Program Files\Tesseract-OCR`
- **Poppler** (Windows): Pour pdf2image, installer dans `C:\Tools\poppler`