# VACANT — backlog priorisé, deux rails (17 octobre 2026)

**Mission fondamentale : rendre visible et intelligible la vacance résidentielle à Paris — son niveau, sa répartition territoriale, son évolution et les limites de nos connaissances.** L'histoire du bâti est une seconde lecture graphique et scientifique, pas un substitut à la mesure de la vacance.

**Source de vérité** : GitHub `Kiwinokoto/vacant`. App desktop prioritaire, petits écrans utilisables sans recette sur téléphone physique obligatoire. Une PR `dev/*` courte, tests et revue avant toute promotion ; produire les dérivés depuis des sources figées, sans données nominatives LOVAC.

## Rail V — Vacance résidentielle (prioritaire, environ 70 % de l'effort)

| ID | Priorité | Livrable et critère de validation | État au 17/10 |
| --- | --- | --- | --- |
| **V-01** | P0 | **Rendre lisible la carte IRIS 2023** : rappeler le taux parisien de référence, **139 075 / 1 402 024 = 9,9 %** selon Insee RP2023 ; afficher année, territoire, numérateur/dénominateur et avertissement « taux IRIS ≠ adresse ». Statistiques de distribution : pondération par logements, distinguer nombre d'IRIS et nombre de logements ; taux cachés si parc de moins de 50 logements | **Première synthèse IRIS implémentée dans la PR de cette passe**, avec taux non arrondis, contrôle indépendant du total Paris (9,9 %), 852/929 IRIS ≥ 5 %, 249/929 ≥ 12 %, 63 masqués ; recette avant déploiement |
| **V-02** | P0 | **Évolution Paris entier, graphique et tableau** : jalons réellement publiés Insee **1968, 1975, 1982, 1990, 1999, 2007, 2012, 2017, 2023**, nombres de vacants et taux calculé sur le parc total. Rupture explicite dénombrements 1968–1999 vs RP rénové 2007–2023 ; **ne pas interpoler** ni appliquer cette série historique aux IRIS/bâtiments | **Page 1968–2023, graphique taux/nombre et tableau implémentés dans la PR de cette passe** ; recette Chromium en cours, sans déploiement |
| **V-03** | P0 | **Évolution 20 arrondissements** : exploiter le dérivé déjà validé RP2006/2011/2016/2023, choix nombre/taux, mêmes classes, classement, comparaison de deux millésimes avec variations en points de pourcentage et nombres absolus, mention « limites IGN 2025 d'affichage, agrégats IRIS d'époque » | 4 jalons et carte existants ; comparaison à construire |
| **V-04** | P1 | **LOVAC public agrégé 2020–2026** à l'échelle Paris commune seulement : télécharger **uniquement** le CSV agrégé (aucun détail privé), figer source/schema/SHA, distinguer parc privé, vacance de plus de deux ans, suppression statistique. **Ruptures 2024 (GMBI) et 2025 (chaîne d'extraction)** représentées comme ruptures explicites ; ne jamais raccorder la courbe aux taux du RP | Source officielle identifiée, collecte/contrat à effectuer |
| **V-05** | P1 | IRIS historique comparables : 2006/2011/2016, contours IGN millésimés corrects, licences, matching 992 géométries, ambiguïtés d'IRIS explicitement non comparables. **Ne pas dessiner 2011 sur les contours 2025 sans avertissement ni table de passage** | Sources et candidats privés audités, droits à confirmer |
| **V-06** | P1 | Finesse maximale **sans réidentification** : indicateurs de disponibilité des données, petits effectifs grisés, quantiles et distributions pondérées, localisation indirecte impossible. Corrélation avec bâti uniquement **à la maille territoriale** et avec contrôle des variables confondantes | Politique de sécurité déjà établie ; analyses à créer |
| **V-07** | P2 | Étudier commerces et bureaux **dans un chapitre distinct** de la vacance résidentielle ; seulement s'il existe une source statistique adéquate, millésimée et légalement diffusable | Recherche préliminaire seulement |

## Rail B — Évolution du bâti / reconstitution (parallèle, environ 30 %)

| ID | Priorité | Livrable et critère de validation | État au 17/10 |
| --- | --- | --- | --- |
| **B-01** | P0 | Examiner la **PR #28 IGN 2008/2011/2018** en brouillon : 2011/2018 ≈ 97 % des IDs communs, mais **2008 très peu comparable**. Ne jamais interpréter différence de densité du référentiel comme constructions | PR de recherche ouverte, pas en production |
| **B-02** | P1 | Comparaison spatiale 2011 ↔ 2018 : intersections, tolérances, scissions/fusions, classes et surfaces, audits GEOS et échantillon réel ; classer « modification de géométrie du référentiel » séparément de « changement physique attesté » | Première comparaison IDs/échantillon local réalisée |
| **B-03** | P1 | Analyser BD TOPO **mars et septembre 2018**, puis améliorer la compréhension de l'édition 2008 et des différences de couverture avant toute série cartographique | Candidats historiques identifiés |
| **B-04** | P1 | **Paris qui apparaît en couleur** : animation / curseur de jalons géographiques authentiques, avec affichage discret de couverture et incertitudes ; ne pas colorer 1830, 2008 ou une année arbitraire en prétendant disposer d'une observation annuelle | Prototype privé 2011/2018 |
| **B-05** | P2 | Annexes de datation patrimoniale (Apur périodes attribuées, cadastres anciens, plans) : conserver « date de construction attribuée », « date du plan », « date du référentiel » comme dimensions distinctes | Apur périodes et hauteurs publiées sous ODbL |

## Critères communs

- Toutes les cartes et graphiques donnent **source, date, périmètre, unité, dénominateur, méthode, limites et droits**. Les séries hétérogènes ne sont **pas** une unique courbe comparable sans signalement.
- **Vacance IRIS/arrondissement/Paris = statistique territoriale**, jamais statut d'un appartement ou d'un bâtiment. Les catégories « résidences secondaires / occasionnels » et « vacants » ne s'additionnent pas implicitement dans les taux.
- Les vraies emprises anciennes sont des **états documentaires**, pas une preuve automatique de démolition/construction. Licence IGN des archives miroirs à valider avant toute redistribution.
- Un contrôle de provenance dans le code, tests unitaires et recette navigateur quand une UI change ; pas de migration ni publication automatique à partir d'un fichier de recherche.
- **Ordre immédiat** : V-02 (page temporelle sourcée) → V-01 (synthèse IRIS et pondération) → V-03 (comparateur arrondissements). En parallèle : B-01 (PR #28) → B-02 (concordance spatiale). Ensuite V-04 (LOVAC).
