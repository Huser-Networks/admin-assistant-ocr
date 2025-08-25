# Structure du Projet OCR Assistant

## Organisation des Dossiers

```
admin-assistant-ocr/
│
├── START.bat          # ⭐ LANCEUR PRINCIPAL Windows
├── INSTALL.bat        # ⭐ INSTALLATION Windows
├── main.py            # Script principal OCR
├── requirements.txt   # Dépendances Python
│
├── gui/               # Interface graphique
│   └── ocr_gui.py    # Application Tkinter
│
├── bin/              # Scripts de lancement
│   ├── launch.bat    # Lanceur Windows simple
│   ├── launch.py     # Lanceur Python
│   └── archive/      # Anciens scripts
│
├── installers/       # Scripts d'installation et diagnostic
│   ├── install.bat           # Installation complète
│   ├── recreate_venv.bat     # Recrée l'environnement virtuel
│   ├── check_python.bat      # Diagnostic Python
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
# Windows - Double-cliquez sur:
INSTALL.bat

# Ou manuellement:
installers\install.bat
```

### Lancement
```bash
# Windows - Double-cliquez sur:
START.bat

# Ou depuis bin/:
bin\launch.bat
python bin\launch.py
```

### Diagnostic et maintenance
```bash
# Vérifier les versions Python:
installers\check_python.bat

# Recréer l'environnement virtuel:
installers\recreate_venv.bat
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