# 📋 Guide de Configuration

## Fichiers de Configuration

### 1️⃣ `config.json` (AUTO-GÉRÉ)
Liste des dossiers actifs - **NE PAS MODIFIER MANUELLEMENT**
```json
{
  "scan_folder": "scan",
  "sub_folders": ["Personnel", "Entreprise"],
  "output_folder": "output"
}
```

### 2️⃣ `extraction_rules.json` (MODIFIABLE)
Patterns de détection - **VOUS POUVEZ PERSONNALISER**
- Formats de dates
- Patterns de numéros de facture
- Mots-clés de détection

### 3️⃣ `hierarchical_config.json` (AUTO-GÉRÉ + MODIFIABLE)
Configuration par dossier - **GÉNÉRÉ PAR SCRIPT, MODIFIABLE SI BESOIN**
```json
{
  "global": {
    "user_info": {
      "names": ["Votre Nom"],
      "addresses": ["Votre Adresse"]
    }
  },
  "folders": {
    "Personnel": {
      "add": {},
      "remove": {}
    }
  }
}
```

## 🚀 Utilisation

### Configuration Automatique (RECOMMANDÉ)
```cmd
python scripts/configure_hierarchical.py
```

### Modification Manuelle (AVANCÉ)
Éditez `hierarchical_config.json` directement :
- `add` : Ajoute des éléments pour ce dossier
- `remove` : Retire des éléments du global

## 📁 Dossiers Archives
`archives/` contient les anciennes configs (peut être supprimé)