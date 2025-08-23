# Guide de Personnalisation - OCR Assistant

## 🎯 Vue d'ensemble

Le système est conçu pour être facilement extensible et personnalisable via des fichiers de configuration JSON. Pas besoin de modifier le code !

## 📁 Architecture Modulaire

```
src/config/
├── extraction_rules.json    # Règles d'extraction globales
├── profiles/                # Profils par dossier
│   ├── global.json          # Configuration par défaut
│   ├── HN.json              # Profil pour scan/HN/
│   ├── Entreprise1.json    # Profil pour scan/Entreprise1/
│   └── Personnel.json       # Profil pour scan/Personnel/
```

## 🔧 1. Créer un Profil pour un Nouveau Dossier

### Étape 1: Créer le dossier de scan
```
scan/
├── HN/
├── Factures/           # Nouveau dossier
└── MonEntreprise/      # Nouveau dossier
```

### Étape 2: Créer le fichier de profil
Créer `src/config/profiles/Factures.json`:

```json
{
  "profile_name": "Mes Factures",
  "description": "Configuration pour mes factures",
  "inherits_from": "global",
  
  "user_info": {
    "names": ["Votre Nom"],
    "addresses": ["Votre Adresse"],
    "companies": ["Votre Société"]
  },
  
  "supplier_mappings": {
    "Électricité de France": "EDF",
    "Orange SA": "Orange"
  }
}
```

## 🎨 2. Personnaliser l'Extraction

### Modifier les Patterns de Date

Dans `src/config/extraction_rules.json`:

```json
{
  "date_patterns": {
    "custom_format": {
      "patterns": ["\\b(\\d{4})\\.(\\d{2})\\.(\\d{2})\\b"],
      "keywords": ["émis le", "date facture"],
      "priority": 15
    }
  }
}
```

### Ajouter des Mots-clés pour les Factures

```json
{
  "invoice_patterns": {
    "custom_invoice": {
      "keywords": ["numéro client", "référence client"],
      "patterns": ["[\\s:]*(CLI[0-9]+)"],
      "max_length": 15
    }
  }
}
```

## 👤 3. Configurer vos Informations Personnelles

Pour éviter que vos infos soient détectées comme fournisseur, dans votre profil:

```json
{
  "user_info": {
    "names": [
      "Jean Dupont",
      "J. Dupont",
      "M. Dupont"
    ],
    "addresses": [
      "123 rue de la Paix",
      "75001 Paris"
    ],
    "companies": [
      "Ma Société SARL",
      "Mon Auto-Entreprise"
    ],
    "emails": ["jean@example.com"],
    "phones": ["0612345678"]
  }
}
```

## 🏢 4. Mapper les Noms de Fournisseurs

Pour raccourcir/standardiser les noms:

```json
{
  "supplier_mappings": {
    "Électricité de France EDF SA": "EDF",
    "Orange France Telecom": "Orange",
    "Société Générale": "SG",
    "Caisse d'Épargne Île-de-France": "CE",
    "Free Mobile": "Free"
  }
}
```

## 📝 5. Personnaliser le Format de Nommage

```json
{
  "naming_rules": {
    "format": "{date}_{supplier}{invoice}",
    "date_format": "YYYYMMDD",
    "use_camel_case": true,
    "max_filename_length": 80,
    "remove_accents": true,
    "include_amount": false
  }
}
```

Exemples de formats :
- `"{date}_{supplier}{invoice}"` → `20240315_EdfFAC2024001.pdf`
- `"{date}_{supplier}"` → `20240315_ElectriciteDeFrance.pdf`
- `"{supplier}{date}{invoice}"` → `Edf20240315FAC2024001.pdf`

Formats disponibles:
- `{date}` : Date du document
- `{supplier}` : Nom du fournisseur
- `{invoice}` : Numéro de facture
- `{amount}` : Montant (si configuré)
- `{type}` : Type de document

## 🔍 6. Zones d'Extraction Spécifiques

Pour mieux cibler l'extraction:

```json
{
  "extraction_zones": {
    "supplier_zone": {
      "top_lines": 20,
      "avoid_after_keywords": ["destinataire", "client"],
      "prefer_before_keywords": ["facture", "date"]
    }
  }
}
```

## 🏥 7. Exemple: Configuration Médicale

Pour `src/config/profiles/Medical.json`:

```json
{
  "profile_name": "Documents Médicaux",
  "inherits_from": "global",
  
  "special_rules": {
    "extract_patient_id": true,
    "extract_service": true,
    "extract_doctor": true
  },
  
  "extraction_settings": {
    "priority_keywords": [
      "consultation",
      "ordonnance",
      "compte-rendu",
      "examen"
    ]
  },
  
  "supplier_mappings": {
    "Hôpital Saint-Louis": "HSL",
    "Clinique du Parc": "CDP",
    "Laboratoire Central": "LAB"
  }
}
```

## 🔄 8. Héritage de Configuration

Les profils peuvent hériter d'autres profils:

```
global.json (base)
    ↓
Personnel.json (hérite de global)
    ↓
Personnel_2024.json (hérite de Personnel)
```

## 💡 9. Conseils d'Amélioration

### Améliorer la Détection du Fournisseur

1. **Ajouter vos infos personnelles** dans `user_info` pour les exclure
2. **Mapper les variantes** de noms dans `supplier_mappings`
3. **Identifier les zones** où apparaît le fournisseur

### Améliorer la Détection de Date

1. **Ajouter des mots-clés** spécifiques à vos documents
2. **Augmenter la priorité** des formats que vous utilisez
3. **Limiter la recherche** aux premières lignes si nécessaire

### Améliorer les Numéros de Référence

1. **Identifier les préfixes** utilisés (FAC-, REF-, etc.)
2. **Ajouter les patterns** spécifiques
3. **Définir la longueur max** pour éviter les faux positifs

## 🐛 10. Debug et Tests

Pour voir ce qui est extrait, vérifiez les logs dans `logs/`:
- Niveau INFO : Résultats d'extraction
- Niveau DEBUG : Détails du processus

Exemple de log:
```
INFO - Date extraite: 20240315 (score: 85.2, type: french)
INFO - Fournisseur extrait: EDF (score: 72.5)
INFO - Numéro extrait: FAC2024-001 (type: standard, score: 90.0)
```

## 📚 11. Structure Recommandée

```
scan/
├── Personnel/          # Documents personnels
├── Entreprise1/        # Société 1
├── Entreprise2/        # Société 2
├── Medical/            # Documents médicaux
├── Banque/            # Relevés bancaires
├── Impots/            # Documents fiscaux
└── Assurances/        # Polices et sinistres
```

Chaque dossier peut avoir son propre profil avec ses règles spécifiques !