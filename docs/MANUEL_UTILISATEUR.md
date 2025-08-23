# 📚 Manuel Utilisateur - OCR Assistant

Guide pratique pour configurer et utiliser l'OCR Assistant selon vos besoins.

## 🚀 Démarrage Rapide (5 minutes)

### 1. Installation
```cmd
# Installer les dépendances
scripts\install_windows.bat

# Vérifier l'installation
python scripts/test_config.py
```

### 2. Configuration de base
Éditez `src/config/config.json` :
```json
{
  "scan_folder": "scan",
  "sub_folders": ["MesDocuments"],
  "output_folder": "output"
}
```

### 3. Premier test
```cmd
# Placez un PDF dans scan/MesDocuments/
# Lancez le traitement
run_windows.bat
```

---

## ⚙️ Configuration Personnalisée

### 📁 Organiser vos Dossiers

**Structure recommandée :**
```
scan/
├── Personnel/      # Documents personnels
├── Entreprise/     # Documents professionnels  
├── Medical/        # Documents médicaux
├── Banque/         # Relevés bancaires
└── Factures/       # Factures diverses
```

**Configuration dans `src/config/config.json` :**
```json
{
  "scan_folder": "scan",
  "sub_folders": ["Personnel", "Entreprise", "Medical", "Banque", "Factures"],
  "output_folder": "output"
}
```

### 👤 Configuration de votre Profil

**Étape 1 :** Créer votre profil `src/config/profiles/Personnel.json`

```json
{
  "profile_name": "Mes Documents Personnels",
  "inherits_from": "global",
  
  "user_info": {
    "names": [
      "Jean Dupont",
      "J. Dupont", 
      "M. Dupont",
      "Monsieur Dupont"
    ],
    "addresses": [
      "123 rue de la République",
      "75001 Paris",
      "Paris 75001"
    ],
    "companies": [
      "Ma Société SARL"
    ],
    "emails": [
      "jean.dupont@email.com"
    ],
    "phones": [
      "06 12 34 56 78",
      "0612345678"
    ]
  },
  
  "supplier_mappings": {
    "Électricité de France": "Edf",
    "EDF SA": "Edf",
    "Orange France": "Orange",
    "Crédit Agricole Ile de France": "CreditAgricole",
    "Société Générale": "SG"
  }
}
```

**Étape 2 :** Copier ce profil pour vos autres dossiers

```cmd
# Dupliquer pour chaque dossier
copy "src/config/profiles/Personnel.json" "src/config/profiles/Entreprise.json"
copy "src/config/profiles/Personnel.json" "src/config/profiles/Medical.json"
```

### 🏢 Configuration Professionnelle

Pour `src/config/profiles/Entreprise.json` :

```json
{
  "profile_name": "Documents Entreprise",
  "inherits_from": "global",
  
  "user_info": {
    "companies": [
      "Ma Société SARL",
      "SARL Ma Société",
      "Ma Société"
    ],
    "addresses": [
      "456 Avenue du Commerce",
      "75008 Paris"
    ],
    "siret": "12345678901234",
    "tva": "FR12345678901"
  },
  
  "supplier_mappings": {
    "Amazon Business": "Amazon",
    "Microsoft France": "Microsoft",
    "OVH SAS": "OVH"
  },
  
  "special_rules": {
    "extract_tva": true,
    "extract_total_ht": true
  }
}
```

### 🏥 Configuration Médicale

Pour `src/config/profiles/Medical.json` :

```json
{
  "profile_name": "Documents Médicaux",
  "inherits_from": "global",
  
  "user_info": {
    "patient_id": "123456789"
  },
  
  "supplier_mappings": {
    "Hôpital Necker": "HN",
    "Hôpital Saint-Louis": "HSL",
    "CPAM Paris": "CPAM",
    "Assurance Maladie": "CPAM"
  },
  
  "special_rules": {
    "extract_patient_id": true,
    "extract_service": true
  }
}
```

---

## 🎯 Utilisation Pratique

### Workflow Complet

#### 1. Placement des Documents
```
scan/
├── Personnel/
│   ├── facture_edf.pdf
│   └── releve_ca.pdf
├── Entreprise/
│   ├── facture_amazon.pdf
│   └── devis_ovh.pdf
└── Medical/
    └── ordonnance_hn.pdf
```

#### 2. Traitement
```cmd
run_windows.bat
```

#### 3. Résultats
```
output/
├── Personnel/
│   ├── 20240315_Edf_FAC123456.pdf
│   └── 20240301_CreditAgricole_REL789.pdf
├── Entreprise/
│   ├── 20240320_Amazon_CMD654321.pdf
│   └── 20240325_Ovh_DEV987654.pdf
└── Medical/
    └── 20240310_HN_ORD456789.pdf
```

#### 4. Vérification et Apprentissage
```cmd
# Réviser les résultats et corriger si nécessaire
python scripts/review_results.py
```

### Mode Apprentissage

#### Première Utilisation
1. **Traitement initial** → Résultats imparfaits
2. **Révision** → Corrections manuelles
3. **Apprentissage** → Système s'améliore

#### Exemple d'Amélioration

**Premier traitement :**
```
📄 facture_edf.pdf → 20240315_Destinataire_123.pdf ❌
```

**Révision interactive :**
```
🏢 Fournisseur actuel: Destinataire
🏢 Nouveau fournisseur: Edf
📋 Numéro actuel: 123
📋 Nouveau numéro: FAC456789
✅ Corrections enregistrées !
```

**Traitements suivants :**
```
📄 autre_facture_edf.pdf → 20240320_Edf_FAC654321.pdf ✅
🧠 Pattern appris automatiquement
```

---

## 🔧 Personnalisation Avancée

### Ajouter des Patterns de Date

Dans `src/config/extraction_rules.json` :

```json
{
  "date_patterns": {
    "mon_format": {
      "patterns": ["le (\\d{1,2}) (\\w+) (\\d{4})"],
      "keywords": ["émis le", "établi le"],
      "priority": 12
    }
  }
}
```

### Ajouter des Types de Numéros

```json
{
  "invoice_patterns": {
    "mon_fournisseur": {
      "keywords": ["référence client", "n° abonné"],
      "patterns": ["[:\\s]*(CLI[0-9]+)"],
      "max_length": 15
    }
  }
}
```

### Format de Nommage Personnalisé

Dans votre profil :

```json
{
  "naming_rules": {
    "format": "{date}_{supplier}_{invoice}",
    "date_format": "YYYYMMDD",
    "use_camel_case": true,
    "max_filename_length": 100
  }
}
```

---

## 🛠️ Scripts Utiles

### Test de Configuration
```cmd
# Tester l'extraction sur des échantillons
python scripts/test_config.py
```

### Test du Format de Nommage
```cmd
# Vérifier le format des noms générés
python scripts/test_filename_format.py
```

### Révision et Apprentissage
```cmd
# Interface de correction
python scripts/review_results.py
```

### Statistiques
```cmd
# Voir les performances (après plusieurs traitements)
python -c "from src.utils.learning_system import LearningSystem; print(LearningSystem().generate_improvement_report())"
```

---

## 🐛 Dépannage

### Problèmes Courants

#### "Tesseract not found"
```cmd
# Vérifier l'installation
C:\Tools\Tesseract-OCR\tesseract.exe --version
```

#### "No PDF files found"
- Vérifiez que vos PDFs sont dans `scan/[sous-dossier]/`
- Extensions acceptées : `.pdf` (minuscules)

#### "Mauvais fournisseur extrait"
1. Ajoutez vos infos dans `user_info`
2. Utilisez le mode révision pour corriger
3. Le système apprendra automatiquement

#### "Date incorrecte"
- Ajoutez des mots-clés spécifiques dans les patterns
- Utilisez le mode révision pour corriger

### Logs et Debug

Les logs sont dans `logs/` :
- **Console** : Niveau INFO
- **Fichiers** : Niveau DEBUG

```cmd
# Voir les logs détaillés
type "logs\ocr_*.log"
```

---

## 📈 Optimisation Progressive

### Semaine 1 : Configuration de base
- ✅ Installer et configurer
- ✅ Créer vos profils avec vos infos
- ✅ Première série de tests

### Semaine 2 : Apprentissage
- ✅ Utiliser le mode révision
- ✅ Corriger les erreurs
- ✅ Observer l'amélioration

### Semaine 3 : Optimisation
- ✅ Ajuster les patterns spécifiques
- ✅ Affiner les mappings fournisseurs
- ✅ Automatiser le workflow

### Résultat : Système Ultra-Efficace
- 🎯 90%+ de précision sur vos documents
- ⚡ Traitement automatique fiable
- 🗂️ Organisation parfaite

---

## 💡 Conseils d'Expert

1. **Commencez simple** : Un profil, quelques PDFs
2. **Corrigez systématiquement** : Le système apprend vite
3. **Organisez par type** : Séparez perso/pro/médical
4. **Testez régulièrement** : `scripts/test_config.py`
5. **Sauvegardez vos configs** : Les profils sont précieux !

**Résultat garanti : Un assistant OCR qui vous connaît parfaitement !** 🚀