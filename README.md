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

1. **Installation automatique :**
   ```cmd
   scripts\install_windows.bat
   ```

2. **Configuration interactive :**
   ```cmd
   python scripts\setup_user_config.py
   ```

3. **Premier traitement :**
   ```cmd
   run_windows.bat
   ```

📖 **Guides détaillés :**
- [Installation complète](docs/INSTALLATION_WINDOWS.md)
- [Manuel utilisateur](docs/MANUEL_UTILISATEUR.md)
- [Personnalisation avancée](docs/CUSTOMIZATION_GUIDE.md)

## 🔧 Configuration

Modifier `src/config/config.json` :

```json
{
  "scan_folder": "scan",
  "sub_folders": ["Devis", "Factures", "Courriers"],
  "output_folder": "output"
}
```

## 📝 Format de Sortie

Les PDFs sont renommés automatiquement selon le format :
```
YYYYMMDD_NomFournisseur_NumeroFacture.pdf
```

Format CamelCase avec séparateurs pour une meilleure lisibilité :
- `20240315_Edf_FAC2024001.pdf`
- `20240122_OrangeMobile_REF123456.pdf`
- `20240201_SarlDupont_DEVIS789.pdf`
- `20240810_CaisseEpargne_BDC45678.pdf`

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

## 🧠 Mode Apprentissage

Le système s'améliore automatiquement à chaque utilisation !

### Fonctionnement Automatique
- 📊 **Statistiques** : Enregistre le taux de succès de chaque extraction
- 🏢 **Fournisseurs fréquents** : Apprend vos fournisseurs habituels
- 📈 **Patterns efficaces** : Retient ce qui fonctionne bien

### Correction Manuelle
Après traitement, vous pouvez corriger les erreurs :

```cmd
# Réviser les derniers résultats et corriger si nécessaire
python scripts/review_results.py
```

**Processus de correction :**
1. 📋 Affiche les extractions récentes
2. ❓ "Cette extraction est-elle correcte ?"
3. ❌ Si NON → Saisir les bonnes valeurs
4. 🧠 Le système apprend et s'améliore

### Exemple d'Amélioration

**Première fois :**
```
📄 facture_edf.pdf → 20240315_Destinataire_REF123.pdf ❌
```

**Correction :**
```
🏢 Nouveau fournisseur: Edf
✅ Correction enregistrée
```

**Fois suivantes :**
```
📄 autre_facture_edf.pdf → 20240320_Edf_FAC456.pdf ✅
🧠 Pattern reconnu automatiquement
```

### Configuration Personnalisée

**Éviter votre adresse :** Éditez `src/config/profiles/[dossier].json`
```json
{
  "user_info": {
    "names": ["Votre Nom"],
    "addresses": ["Votre Adresse"],
    "companies": ["Votre Société"]
  }
}
```

**Mapper les fournisseurs :**
```json
{
  "supplier_mappings": {
    "Électricité de France": "Edf",
    "Orange SA": "Orange"
  }
}
```

📖 Guide complet : [docs/CUSTOMIZATION_GUIDE.md](docs/CUSTOMIZATION_GUIDE.md)