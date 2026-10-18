# VACANT — Audit LOVAC 2020–2026 (17 octobre 2026)

Source publique officielle : https://www.data.gouv.fr/datasets/61816c6e23197bb34835228e (DGALN/Cerema, Licence Ouverte 2.0).

Trois CSV publics (communes, départements, dictionnaire) ont été téléchargés sur le VPS personnel et vérifiés par SHA-256. Le jeu comporte vingt lignes parisiennes, codes 75101–75120, sans suppression statistique pour leurs indicateurs. Leurs sommes correspondent exactement à la ligne du département 75.

**Attention aux ruptures de méthode GMBI dès le millésime 2024, puis changement de sélection en 2025.** Les grandes variations ne sont pas des flux de logements libérés. LOVAC couvre le parc privé fiscal ; le RP Insee le parc total. Les dates de référence diffèrent aussi des millésimes : 2026 correspond au 01/01/2025 ; la vacance longue 2023 au 01/01/2022. Ne pas construire de taux de vacance 2026 à partir de `ff_pp_total_25`, date 01/01/2024.


## Sources figées et contrôles reproductibles

- Jeu officiel : https://www.data.gouv.fr/datasets/61816c6e23197bb34835228e, publié le **25 juin 2026**, Licence Ouverte 2.0.
- `lovac-opendata-communes26.csv` (7 628 201 octets), SHA-256 `b856568d4b69784d32f9fafaf7e1376047e45eed245fb114dd737d2d43826245`.
- `lovac-opendata-departements26.csv`, SHA-256 `b6c3d2304dd4d35d07f6153720874650ea1f55583ffe58e459632b2f3e01a2ff`.
- `lovac-opendata-metadonnees26.csv`, SHA-256 `d8698c32631201ab295268aa2e8679cd715abcc7c3550379c53c41076174bd81`.
- Originaux publics figés **hors racine web** sous `/srv/vacant/data/raw/lovac/open-aggregate-20260625/`, droits 0600. Le script `scripts/audit_lovac_open_paris.py` refuse les SHA altérés, un code 75101–75120 manquant, une valeur `s` masquée, des dates incompatibles et des sommes divergentes de la ligne départementale 75.
- Dérivé vérifié avec **20 arrondissements, sept millésimes, sans données au logement** : `site/data/lovac-paris-open-2026.json` (9 612 octets, SHA-256 `383978506b23b21d75a22b84e6a4499e26a41b347e6e1108e833e86eb98fb326`). Cette petite ressource ouverte est suivie dans GitHub et relit systématiquement sa provenance.

## Totaux publics Paris

| Millésime de production | Vacants du parc privé | Plus de 2 ans | Parc privé connu (date distincte) |
|---|---:|---:|---:|
| 2020 | 122 856 | 18 648 | 1 136 856 |
| 2021 | 124 555 | 19 822 | 1 134 924 |
| 2022 | 129 788 | 20 380 | 1 132 827 |
| 2023 | 150 072 | 21 489 | 1 130 872 |
| 2024 | 142 848 | 32 091 | 1 125 864 |
| 2025 | 75 774 | 36 205 | 1 124 440 |
| 2026 | 105 785 | 26 264 | **Indisponible dans ce fichier** |

**Attention : dates par variable dans le dictionnaire**. Par exemple le 2026 « tous vacants » relève du **01/01/2025** et n'est pas une observation de l'année civile 2026. Le 2023 « longue durée » relève du **01/01/2022** alors que « tous vacants » est daté **01/01/2023**. Les dénominateurs ne sont pas automatiquement alignés : ne publier **aucun taux LOVAC 2026** avec `ff_pp_total_25` (daté 01/01/2024).

## Interface et état de réalisation

La page expérimentale `site/lovac.html` présente deux indicateurs avec **sept barres distinctes** et trois familles visuelles de méthode, une table de vingt arrondissements et les dates de référence exactes. Elle est reliée depuis l'accueil et la page historique Insee. Le script client `site/lovac-public-contract.mjs` revérifie l'agrégat Paris et les dates. Aucun rapprochement avec les logements individuels, aucun taux individuel ou bâti.

**Recette Chromium locale** sur la branche : desktop 1440×900 et mobile simulé 390×844, 7 barres, 20 lignes, bascule entre mesures et millésimes 2026→2023, 0 erreur JS, 0 overflow. Tests unitaires : 6 Python de l'audit et 2 JavaScript du contrat, puis suite totale de **91 tests JS** réussis (compte Python exact à revérifier sur HEAD final).

La publication du graphe ne doit pas lui donner une continuité causale : **GMBI peut modifier la mesure sans changement réel d'occupation**. Préférer une analyse fine par arrondissement, descriptive et prudentielle, plutôt que des variations « logements libérés » entre 2024 et 2025.
