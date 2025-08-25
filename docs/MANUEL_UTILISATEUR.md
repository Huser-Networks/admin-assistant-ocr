# 📚 Manuel Utilisateur - OCR Assistant

Guide pratique pour configurer et utiliser l'OCR Assistant avec système hiérarchique.

## 🚀 Démarrage Rapide (5 minutes)

### 1. Installation
```cmd
# Installer les dépendances Windows
scripts\install_windows.bat
```

### 2. Configuration Hiérarchique
```cmd
# Lancer la configuration intelligente
python scripts\configure_hierarchical.py
```

**Le script détecte automatiquement vos dossiers et vous guide :**
- 🔍 **Détection auto** des dossiers existants dans `scan/`
- 🌍 **Config globale** (infos à ignorer partout)
- 📁 **Config par dossier** (ajouts/suppressions spécifiques)
- ✅ **Validation** avec résumé complet

### 3. Premier Test
```cmd
# Placez un PDF dans scan/[VotreDossier]/
# Lancez le traitement
run_windows.bat
```

### 4. Révision et Apprentissage
```cmd
# Corriger les erreurs pour améliorer le système
python scripts\review_results.py
```

---

## ⚙️ Configuration Hiérarchique

### 🌍 Principe : Global → Dossiers

**Système d'héritage avec surcharges :**
```
GLOBAL (ignoré partout)
├── Personnel (utilise global)
├── Entreprise (+ajoute entreprise)
├── DocsPourAmi (-retire votre nom, +ajoute ami)
└── [VosDossiers] (+/- selon besoins)
```

### 📁 Gestion Automatique des Dossiers

Le script détecte et propose :
1. **Utiliser** les dossiers existants
2. **Ajouter** de nouveaux dossiers  
3. **Repartir** de zéro

### 🔧 Configuration en 3 Étapes

**1. Configuration Globale (ignorée partout) :**
- Vos noms/prénoms
- Vos adresses
- Vos entreprises par défaut

**2. Configuration par Dossier :**
- **Ajouts (+)** : Éléments spécifiques au dossier
- **Suppressions (-)** : Retirer des éléments globaux

**3. Résultat Final :**
- Chaque dossier a SA configuration effective
- Héritage intelligent avec surcharges

---

## 📋 Exemples Concrets

### Exemple 1 : Configuration Simple

```
🌍 Global : Jean Dupont / 75001 Paris
├── Personnel : utilise config globale
├── Factures : utilise config globale
└── Medical : utilise config globale
```

### Exemple 2 : Multi-Entreprises

```
🌍 Global : Jean Michel / route de Pré
├── Personnel : config globale
├── SdbSarl : +Salle de Bains SARL / route du Chemin
├── ItSA : +Informatique SA
└── DocsPourAmi : -Jean Michel, +Justin Machin
```

**Résultat :**
- Facture pour Jean Michel de IT SA → Dossier `ItSA` ✅
- Facture pour Justin Machin → Dossier `DocsPourAmi` ✅

### Fichier Généré (`hierarchical_config.json`)

```json
{
  "global": {
    "user_info": {
      "names": ["Jean Michel"],
      "addresses": ["route de Pré"]
    }
  },
  "folders": {
    "Personnel": {
      "add": {},
      "remove": {}
    },
    "SdbSarl": {
      "add": {
        "user_info": {
          "companies": ["Salle de Bains SARL"],
          "addresses": ["route du Chemin"]
        }
      }
    },
    "DocsPourAmi": {
      "add": {
        "user_info": {
          "names": ["Justin Machin"]
        }
      },
      "remove": {
        "user_info": {
          "names": ["Jean Michel"]
        }
      }
    }
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
│   └── facture_edf.pdf
├── SdbSarl/
│   └── commande_leroy.pdf
└── DocsPourAmi/
    └── doc_important.pdf
```

#### 2. Traitement
```cmd
run_windows.bat
```

#### 3. Résultats
```
output/
├── Personnel/
│   └── 20240315_Edf_FAC123.pdf
├── SdbSarl/
│   └── 20240320_LeroyMerlin_CMD456.pdf
└── DocsPourAmi/
    └── 20240325_Document_789.pdf
```

#### 4. Apprentissage
```cmd
python scripts\review_results.py
```

---

## 🛠️ Scripts Utiles

### Configuration Principale
```cmd
# Configuration complète avec détection auto
python scripts\configure_hierarchical.py
```

### Ajout de Dossiers
```cmd
# Ajouter un nouveau dossier
python scripts\add_folder.py
```

### Tests et Validation
```cmd
# Tester la configuration
python scripts\test_config.py

# Tester le format de nommage
python scripts\test_filename_format.py
```

### Révision et Statistiques
```cmd
# Interface de correction
python scripts\review_results.py

# Voir les stats d'apprentissage
python -c "from src.utils.learning_system import LearningSystem; print(LearningSystem().generate_improvement_report())"
```

---

## 🔧 Personnalisation Avancée

### Modifier les Patterns de Détection

Dans `src/config/extraction_rules.json` :

```json
{
  "date_patterns": {
    "custom": {
      "patterns": ["\\b(\\d{4})\\.(\\d{2})\\.(\\d{2})\\b"],
      "keywords": ["date", "le"],
      "priority": 10
    }
  }
}
```

### Ajouter des Mappings Fournisseurs

Dans `hierarchical_config.json`, section globale :

```json
{
  "global": {
    "supplier_mappings": {
      "Électricité de France": "Edf",
      "Orange SA": "Orange",
      "Crédit Agricole": "CA"
    }
  }
}
```

### Format de Nommage

Les PDFs sont renommés automatiquement :
```
YYYYMMDD_Fournisseur_NumeroReference.pdf
```

Exemples :
- `20240315_Edf_FAC123456.pdf`
- `20240320_Orange_REF789.pdf`
- `20240325_CreditAgricole_RLV456.pdf`

---

## 🐛 Dépannage

### Problèmes Courants

#### "Tesseract not found"
- Vérifier : `C:\Tools\Tesseract-OCR\tesseract.exe --version`
- Installer depuis : https://github.com/UB-Mannheim/tesseract/wiki

#### "Mauvais destinataire détecté"
1. Vérifier la config globale (noms à ignorer)
2. Vérifier la config du dossier (+/-)
3. Utiliser le mode révision pour corriger

#### "Dossier non détecté"
- Le script cherche dans `scan/`
- Créer le dossier puis relancer le script

### Logs et Debug

Les logs sont dans `logs/` :
```cmd
# Voir les derniers logs
type logs\ocr_*.log | more
```

---

## 📈 Optimisation Progressive

### Semaine 1 : Configuration
- ✅ Lancer `configure_hierarchical.py`
- ✅ Définir config globale
- ✅ Configurer 2-3 dossiers

### Semaine 2 : Tests
- ✅ Traiter quelques PDFs
- ✅ Utiliser `review_results.py`
- ✅ Observer l'amélioration

### Semaine 3 : Production
- ✅ Ajouter tous vos dossiers
- ✅ Affiner les patterns
- ✅ Automatiser complètement

---

## 💡 Conseils d'Expert

1. **Commencez simple** : 2-3 dossiers pour tester
2. **Config globale complète** : Tous vos noms/adresses
3. **Dossiers spécifiques** : Utilisez +/- intelligemment
4. **Corrigez régulièrement** : Le système apprend vite
5. **Sauvegardez** : `hierarchical_config.json` est précieux

---

## 📚 Documentation Complète

- **[Configuration](../CONFIGURATION.md)** : Guide détaillé du système
- **[Installation Windows](INSTALLATION_WINDOWS.md)** : Installation complète
- **[Personnalisation](CUSTOMIZATION_GUIDE.md)** : Personnalisation avancée
- **[Config Guide](../src/config/CONFIG_GUIDE.md)** : Structure des fichiers

**Votre assistant OCR est maintenant intelligent et adaptatif !** 🚀