# Structure du Projet OCR Assistant

## Organisation Simplifiée

```
admin-assistant-ocr/
│
├── START.bat          # ⭐ UNIQUE POINT D'ENTRÉE - Gère tout automatiquement
├── main.py            # Script principal OCR
├── requirements.txt   # Dépendances Python
│
├── gui/               # Interface graphique
│   └── ocr_gui.py    # Application Tkinter
│
├── scripts/          # Scripts utilitaires de configuration
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
│
├── scan/             # Dossiers à scanner (créé automatiquement)
├── output/           # Résultats OCR (créé automatiquement)
├── logs/             # Fichiers de logs (créé automatiquement)
└── ocr-venv/         # Environnement virtuel (créé automatiquement)
```

## Utilisation Ultra-Simple

### 🚀 Un seul fichier à lancer : START.bat

Double-cliquez sur **START.bat** qui gère automatiquement :

1. **Vérification de Python** ✓
2. **Détection/création de l'environnement virtuel** ✓
3. **Installation des dépendances** ✓
4. **Configuration initiale** ✓
5. **Lancement de l'application** ✓

### Fonctionnalités du START.bat

- **Détection intelligente** : Vérifie si l'environnement virtuel existe et fonctionne
- **Personnalisation** : Permet de choisir le nom de l'environnement virtuel
- **Auto-réparation** : Recrée automatiquement le venv si problème de version Python
- **Configuration guidée** : Demande nom/entreprise à la première utilisation
- **Création des dossiers** : Crée automatiquement scan/, output/, logs/

### En cas de problème

Si l'application ne démarre pas :
1. Supprimez le dossier `ocr-venv`
2. Relancez `START.bat`
3. Il recréera tout automatiquement

## Points Importants

- **Un seul fichier** : Plus besoin de multiples scripts, START.bat fait tout
- **Intelligent** : Détecte et répare automatiquement les problèmes courants
- **Flexible** : Permet de personnaliser le nom du venv si souhaité
- **Guidé** : Configuration interactive pour les nouveaux utilisateurs