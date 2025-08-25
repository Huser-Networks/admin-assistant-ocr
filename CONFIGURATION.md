# ⚙️ Configuration OCR Assistant

## 📊 Structure de Configuration Actuelle

```
src/config/
├── config.json              # Liste des dossiers actifs (AUTO-GÉRÉ)
├── extraction_rules.json    # Patterns de détection (PERSONNALISABLE)
├── hierarchical_config.json # Config par dossier (AUTO + MANUEL)
└── archives/                # Anciennes configs (ignoré)
```

## 🚀 Configuration Rapide

### 1. Lancer le Script de Configuration
```cmd
python scripts/configure_hierarchical.py
```

**Le script fait TOUT automatiquement :**
- ✅ Détecte les dossiers existants dans `scan/`
- ✅ Configure la hiérarchie globale → dossiers
- ✅ Gère les ajouts (+) et suppressions (-) par dossier

### 2. Workflow du Script

```
📁 DÉTECTION AUTOMATIQUE
├── Scan les dossiers existants
├── Propose: Utiliser / Ajouter / Recréer
└── Crée la structure scan/ et output/

🌍 CONFIGURATION GLOBALE
├── Vos noms (ignorés partout)
├── Vos adresses (ignorées partout)
└── Vos entreprises par défaut

📂 CONFIGURATION PAR DOSSIER
├── Personnel: utilise config globale
├── EntrepriseSARL: +ajoute l'entreprise
├── DocsPourAmi: -retire votre nom, +ajoute nom ami
└── Etc...
```

## 📝 Fichiers de Configuration

### `config.json` (AUTO)
```json
{
  "scan_folder": "scan",
  "sub_folders": ["Personnel", "EntrepriseSARL", "DocsPourAmi"],
  "output_folder": "output"
}
```
**⚠️ NE PAS MODIFIER - Géré par le script**

### `hierarchical_config.json` (AUTO + MANUEL)
```json
{
  "global": {
    "user_info": {
      "names": ["Jean Michel"],
      "addresses": ["123 route de Pré"],
      "companies": []
    }
  },
  "folders": {
    "Personnel": {
      "add": {},
      "remove": {}
    },
    "EntrepriseSARL": {
      "add": {
        "user_info": {
          "companies": ["Entreprise SARL"],
          "addresses": ["456 avenue Commerce"]
        }
      },
      "remove": {}
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
**✅ MODIFIABLE MANUELLEMENT si besoin**

### `extraction_rules.json` (MANUEL)
```json
{
  "date_patterns": {...},      # Formats de dates
  "invoice_patterns": {...},   # Patterns de factures
  "supplier_rules": {...}      # Règles fournisseurs
}
```
**✅ PERSONNALISABLE pour améliorer la détection**

## 🎯 Exemples Concrets

### Cas 1: Configuration Simple
```
Global: Jean Dupont / 75001 Paris
├── Personnel (config globale)
├── Factures (config globale)
└── Medical (config globale)
```

### Cas 2: Multi-Entreprises
```
Global: Jean Dupont / rue Principale
├── Personnel (global)
├── EntrepriseA (+SARL A / rue Commerce)
├── EntrepriseB (+SARL B / avenue Industrie)
└── EntrepriseC (+SARL C / boulevard Tech)
```

### Cas 3: Documents pour Tiers
```
Global: Jean Dupont
├── Personnel (global)
├── ComptaMaman (-Jean +Marie Dupont)
├── DocsPourAmi (-Jean +Paul Martin)
└── AssocSportive (+Asso Sport / -Jean)
```

## 🔄 Ajout de Dossiers

### Option 1: Via Script Principal
```cmd
python scripts/configure_hierarchical.py
# Choisir: "2. Ajouter des nouveaux dossiers"
```

### Option 2: Script Dédié
```cmd
python scripts/add_folder.py
```

### Option 3: Manuel
1. Créer `scan/NouveauDossier/`
2. Relancer le script de config (détection auto)

## 📋 Résumé de l'Organisation

```
ENTRÉE (scan/)           →  TRAITEMENT (OCR + IA)  →  SORTIE (output/)
├── Personnel/           →  Config Personnel       →  Personnel/
├── EntrepriseSARL/      →  Config + SARL         →  EntrepriseSARL/
├── DocsPourAmi/         →  Config + Ami - Vous   →  DocsPourAmi/
└── [VosDossiers]/       →  [VosConfigs]          →  [VosDossiers]/
```

## ✅ Points Clés

1. **Détection Automatique** - Le script trouve vos dossiers existants
2. **Héritage Intelligent** - Global → Dossier avec +/-
3. **100% Personnalisable** - Créez autant de dossiers que nécessaire
4. **Configuration Hybride** - Auto par script + manuel si besoin
5. **Structure Claire** - Un seul fichier principal (`hierarchical_config.json`)

## 🚀 Commandes Essentielles

```cmd
# Configuration complète
python scripts/configure_hierarchical.py

# Ajouter un dossier
python scripts/add_folder.py

# Tester la config
python scripts/test_config.py

# Lancer le traitement
run_windows.bat

# Réviser les résultats
python scripts/review_results.py
```

## 💡 Conseils

- **Commencez simple** avec 2-3 dossiers
- **Testez** avec quelques PDFs avant la production
- **Affinez** la config après avoir vu les résultats
- **Utilisez la révision** pour améliorer le système

**La configuration est maintenant SIMPLE et PUISSANTE !** 🎯