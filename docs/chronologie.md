# VACANT — choix temporel et protocole de confiance
Décision : **16 octobre 2026**. Départ de la série de vacance **IRIS : 2006**. Le millésime statistique n'est pas une année d'observation de l'état exact de chaque logement.

## Pourquoi 2006 plutôt que 1999, 2010 ou 2020 ?

- **2006** : premier point de la série Insee *recensement rénové* retenue pour comparer des statistiques de logements à la maille IRIS de Paris. Fichier officiel XLS de 70 Mo, géographie des IRIS **2008**, publié en octobre 2009 : https://www.insee.fr/fr/statistiques/2028562.
- **2011** : fichier IRIS géographie **2013**, publié en 2014 : https://www.insee.fr/fr/statistiques/2028269.
- **2016** : fichier IRIS géographie **2018**, publié en 2019 : https://www.insee.fr/fr/statistiques/4228432.
- **2023** : fichier IRIS géographie **2025**, publié le 15 octobre 2026 ; nouveau *format harmonisé* avec changement de dimensions : https://www.insee.fr/fr/statistiques/9061333.
- **1999 et avant** : séries de dénombrement **Paris/arrondissement** depuis 1968 à présenter comme contexte, pas comme une carte annuelle IRIS sans preuve d'une série et d'un zonage comparables : https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75.
- **LOVAC 2020–2026** : vacance fiscale du **parc privé** à la **commune** et vacance > 2 ans, deux ruptures importantes (changement GMBI introduit en 2023, impact LOVAC 2024 ; nouvelle chaîne d'extraction 2025). Ne pas raccorder numériquement à la série Insee : https://www.data.gouv.fr/datasets/logements-vacants-du-parc-prive-par-commune-departement-region-france-de-2020-a-2026.

**Insee comparabilité** : écart **au moins 5 ans** entre RP rénovés ; avec la perturbation Covid autour des RP 2019–2023, **au moins 6 ans** par rapport aux millésimes antérieurs concernés. Les jalons 2006→2011 (5 ans), 2011→2016 (5 ans) et 2016→2023 (7 ans) respectent cet intervalle. Un millésime isolé ne se transforme pas en observation quotidienne ou annuelle. Source : https://www.insee.fr/fr/metadonnees/source/operation/s2242/coherence-comparabilite.

## Premier tableau intégré au site : Paris entier uniquement

Transcription manuelle depuis **sources officielles Insee**, consultées le 16/10/2026. Chaque nombre ci-dessous est une estimation statistique publiée, **pas un statut d'immeuble**. Catégories disjointes.

| Millésime | Parc total de logements | Résidences principales | Résidences secondaires et logements occasionnels | Logements vacants | Source |
| --- | ---: | ---: | ---: | ---: | --- |
| 2006 | 1 334 814 | 1 131 810 | 80 337 | 122 667 | [RP2022 — LOG T1 Paris](https://www.insee.fr/fr/statistiques/8581193?geo=DEP-75) |
| 2011 | 1 356 074 | 1 165 541 | 91 835 | 98 698 | [RP2022 — LOG T1 Paris](https://www.insee.fr/fr/statistiques/8581193?geo=DEP-75) |
| 2016 | 1 374 377 | 1 140 127 | 119 943 | 114 306 | [RP2022 — LOG T1 Paris](https://www.insee.fr/fr/statistiques/8581193?geo=DEP-75) |
| 2023 | 1 402 024 | 1 124 522 | 138 426 | 139 075 | [RP2023 — LOG T1 Paris](https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75) |

Dans certains millésimes, la somme des composantes diffère du total **d'une unité**, cohérente avec les chiffres RP publiés / arrondis. Contrat test : tolérer <= 1, jamais corriger artificiellement les chiffres officiels.

Le taux = vacants / total × 100. L'interface affiche ce **niveau Paris uniquement**, indépendamment des polygones contemporains de Paris Data. Le taux ne mesure ni la vacance de plus de deux ans, ni les locaux professionnels, ni les résidences secondaires.

## Format 2023 et vigilance sur la géométrie

Le [document officiel Insee](https://www.insee.fr/fr/statistiques/fichier/9061333/aide_lecture_logement.pdf) décrit la nouvelle structure (`GEO_OBJECT`, `GEO`, `RP_MEASURE`, `OCS`, `OBS_VALUE`) avec modalités de sélection, et un autre document xlsx contient la **table de passage** entre dimensions : https://www.insee.fr/fr/statistiques/fichier/9061333/table_passage_logement.xlsx. **Ne pas confondre l'exemple OCS=DW_MAIN (résidence principale) avec la vacance.** Les codes catégoriels de vacance/total restent à vérifier par lecture du dictionnaire, donc aucun convertisseur 2023 de données brutes n'est encore publié.

Les contours [IGN Contours...IRIS](https://www.data.gouv.fr/datasets/contours-iris-r-2) sont ouverts sous Licence Ouverte 2.0, mais un jeu annoncé « édition 2024 » n'est pas automatiquement compatible avec le zonage **2025** de RP2023. Le couple exact source/édition doit être prouvé avant intégration. Un validateur indépendant `site/iris-contract.mjs` rejette les métadonnées de géographie incompatibles et laisse la cartographie inactive jusqu'à validation.

## Conditions pour une vraie couche IRIS temporelle

1. Extraire pour **chaque** millésime le fichier Insee d'origine, sa licence, URL, date, géographie et son empreinte SHA-256.
2. Vérifier en lisant le dictionnaire de variables la colonne du **total logements** et des **vacants**. RP2023 exige des filtres dans le **format harmonisé**, pas d'inférence à partir de champs RP2016.
3. Filtrer les **IRIS parisiens** ; vérifier les identifiants, les effectifs, la non-négativité, la couverture et les effectifs petits/soumis à secret. Ne pas normaliser les taux de petites mailles sans mesure des incertitudes.
4. Charger les contours **du même millésime géographique** que les statistiques (2008 / 2013 / 2018 / 2025). Ne jamais reporter silencieusement les effectifs 2006 sur les polygones 2025 : limites et clés peuvent différer.
5. Publier des **polygones IRIS séparés** (et non un badge de « vacance » sur un volume bâti) ; tooltip = *nombre estimé*, taux, numérateur, dénominateur, année, source, géographie, méthode, réserve.
6. Pour comparer des IRIS malgré les changements de limites, produire une **table explicite de correspondance** ou conserver l'affichage dans la géographie propre à chaque année, avec indication visible de la comparabilité imparfaite.
7. Pas de courbe continue, interpolation d'années absentes ou extrusion de logements vides. Si année absente, afficher « non disponible ».

## Qualification

- **Paris entier, 2006–2023** : bon pour tendance générale et niveaux du RP, prudence dans le rapprochement des éditions / définitions.
- **IRIS 2006–2023** : données officielles disponibles, mais **non encore extraites, testées ni visualisées**. Confiance cartographique *non établie* à ce stade.
- **Adresse ou immeuble** : aucune preuve publique de vacance individuelle. Confiance **nulle / interdit d'inférer**.
- **Vacance commerciale / bureaux** : métrique différente ; aucun historique intégré.
