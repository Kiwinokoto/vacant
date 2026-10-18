# VACANT — backlog priorisé, deux rails (17 octobre 2026)

**Mission fondamentale : rendre visible et intelligible la vacance résidentielle à Paris — son niveau, sa répartition territoriale, son évolution et les limites de nos connaissances.** L'histoire du bâti est une seconde lecture graphique et scientifique, pas un substitut à la mesure de la vacance.

**Source de vérité** : GitHub `Kiwinokoto/vacant`. App desktop prioritaire, petits écrans utilisables sans recette sur téléphone physique obligatoire. Une PR `dev/*` courte, tests et revue avant toute promotion ; produire les dérivés depuis des sources figées, sans données nominatives LOVAC.

**Point de reprise PR #33 (17/10/2026) :** la PR #31 donne les agrégats LOVAC ouverts ; #32 ajoute leur carte par arrondissement ; **#33** étudie la vacance longue par **effectif et part parmi les vacants privés**, en interdisant le ratio 2023 (dates non alignées) et en exposant les ruptures 2024–2025. 98 JS et 99 Python, Chromium desktop et 390 px validés sur code `717f5bd`. Tout reste **en brouillon hors production** ; ordre #29 → #30 → #31 → #32 → #33, #28 en parallèle. Prochaine priorité scientifique : contextes/contrastes territoriaux sans comparer des taux incompatibles ni des immeubles.

## Périmètre transversal — espaces vacants et potentiel d'accueil (PR #34)

**Décision utilisateur du 17/10/2026 :** ne pas compter au même titre logements habitables, logements dégradés et bureaux ou commerces inoccupés, **sans exclure les espaces non habitables de l'étude**. Les garder comme potentiel de remise en état, transformation ou accueil temporaire éventuel, à **expertiser** : sécurité, hygiène, eau, ventilation, lumière, évacuation, accès, droits d'usage et délais. **Inconnu par défaut**, jamais « habitable » ou « mobilisable » par déduction statistique.

- **V-08 (P1)** — Protocole de potentiel d'accueil, distinguant destination, occupation, état d'usage, possibilités et contraintes. Première page `site/potentiel.html` en PR #34, note `docs/potentialite-locaux-20261017.md`. Ne pas produire de capacité d'accueil fictive.
- **V-07 (P1 renforcée)** — Locaux tertiaires/commerciaux : Apur BDCOM 2023 = **9 059 locaux vacants parmi 83 154 locaux enquêtés en rez-de-chaussée**, soit 10,9 % ; cette mesure n'est **ni** la vacance de tous les bureaux de Paris **ni** le nombre de logements convertibles. Prochaine enquête : audit BDCOM ouvert (champs vacance/travaux, licences) puis source de **bureaux réellement inoccupés à Paris intra-muros** (m², date, champ).

**Ordre de la pile avant revue : #29 → #30 → #31 → #32 → #33 → #34**. Rail B IGN #28 indépendant. Pas de fusion ni déploiement de ces travaux.

## Mise à jour V-07 — Historique prudent des locaux BDCOM, PR #36

Éditions publiques 2017/2020/2023 auditées sur ArcGIS Apur. **7 853 / 8 764 / 9 060** locaux classés vacants **ou en travaux**, respectivement, séparés par codes AA101/AA102 : **6 954/899**, **7 247/1 517** (dont trois `aa101` en minuscule), **7 495/1 565**. Divergences avec les notes : 2020 **8 760** dans la note 2021 mais **8 560** dans la rétrospective 2023, écart de **200**. À ne **pas** transformer en taux ou courbe annuelle de vacance « réelle » avant expertise de la comparabilité, des corrections et des dénominateurs d'époque. Livrables : JSON de trois agrégats, contrat JS, graphique et tableau, tests, [audit détaillé](docs/bdcom-historical-audit-20261017.md). Prochaine priorité : résoudre les écarts en demandant les métadonnées Apur et reconstruire si possible les dénominateurs 2017/2020 ; garder rail bureaux en m² séparé.

Chaîne PR à revoir : **#29 → #30 → #31 → #32 → #33 → #34 → #35 → #36**, #28 IGN indépendante. **Aucune promotion automatique**.

## Mise à jour V-07 — Audit sources effectives, PR #35 (17/10/2026)

- **BDCOM 2023 Apur :** vingt arrondissements agrégés depuis l'API des **83 154 locaux en RDC**. Identification des codes `AA101` = **7 495 locaux vacants hors travaux** et `AA102` = **1 565 locaux en travaux**, soit **9 060** contre 9 059 indiqués dans la note publiée. **Ne plus présenter 9 059 comme tous « vacants hors travaux ».** Enrichissement de `site/potentiel.html` avec classement local, validation du contrat, test et provenance ODbL. Aucun point/adresse.
- **Bureaux :** offre de marché à Paris intra-muros de **~1,5 million de m² fin juin 2026**, Colliers + Cushman & Wakefield. Source trimestrielle Colliers T1 vs T2 contradictoire : **pas de série temporelle avant réconciliation**, pas de taux de transformabilité inventé.
- **Suite** : qualifier BDCOM 2017/2020, faire confirmer la divergence +1 par Apur, creuser le stock de bureaux structurellement vides, distinguer offre immédiate de surfaces réellement convertibles et évaluer les conditions juridiques de l'accueil. Voir `docs/bdcom-open-audit-20261017.md`. Chaîne PR #29 → #30 → #31 → #32 → #33 → #34 → **#35** ; B-01 #28 indépendante.

## Rail V — Vacance résidentielle (prioritaire, environ 70 % de l'effort)

| ID | Priorité | Livrable et critère de validation | État au 17/10 |
| --- | --- | --- | --- |
| **V-01** | P0 | **Rendre lisible la carte IRIS 2023** : rappeler le taux parisien de référence, **139 075 / 1 402 024 = 9,9 %** selon Insee RP2023 ; afficher année, territoire, numérateur/dénominateur et avertissement « taux IRIS ≠ adresse ». Statistiques de distribution : pondération par logements, distinguer nombre d'IRIS et nombre de logements ; taux cachés si parc de moins de 50 logements | **Première synthèse IRIS implémentée dans la PR de cette passe**, avec taux non arrondis, contrôle indépendant du total Paris (9,9 %), 852/929 IRIS ≥ 5 %, 249/929 ≥ 12 %, 63 masqués ; recette avant déploiement |
| **V-02** | P0 | **Évolution Paris entier, graphique et tableau** : jalons réellement publiés Insee **1968, 1975, 1982, 1990, 1999, 2007, 2012, 2017, 2023**, nombres de vacants et taux calculé sur le parc total. Rupture explicite dénombrements 1968–1999 vs RP rénové 2007–2023 ; **ne pas interpoler** ni appliquer cette série historique aux IRIS/bâtiments | **Page 1968–2023, graphique taux/nombre et tableau implémentés dans la PR de cette passe** ; recette Chromium en cours, sans déploiement |
| **V-03** | P0 | **Évolution 20 arrondissements** : exploiter le dérivé déjà validé RP2006/2011/2016/2023, choix nombre/taux, mêmes classes, classement, comparaison de deux millésimes avec variations en points de pourcentage et nombres absolus, mention « limites IGN 2025 d'affichage, agrégats IRIS d'époque » | **V-03 implémenté sur branche dédiée** : comparateur 2006/2011/2016/2023 sur les 20 arrondissements, taux en **points** ou **logements estimés**, classement complet, contrôle Insee des totaux ; tests Chromium desktop et mobile simulé OK, sans déploiement |
| **V-04** | P1 | **LOVAC public agrégé 2020–2026** à l'échelle Paris commune seulement : télécharger **uniquement** le CSV agrégé (aucun détail privé), figer source/schema/SHA, distinguer parc privé, vacance de plus de deux ans, suppression statistique. **Ruptures 2024 (GMBI) et 2025 (chaîne d'extraction)** représentées comme ruptures explicites ; ne jamais raccorder la courbe aux taux du RP | **V-04 première tranche prête sur PR #31** : 3 CSV ouverts LOVAC figés et vérifiés SHA, 20 arrondissements Paris/ligne département concordants, dates du dictionnaire respectées, page distincte (7 millésimes, 2 mesures), rupture GMBI 2024/2025. Suite : carte des 20 arrondissements et comparabilité méthodologique. |
| **V-05** | P1 | IRIS historique comparables : 2006/2011/2016, contours IGN millésimés corrects, licences, matching 992 géométries, ambiguïtés d'IRIS explicitement non comparables. **Ne pas dessiner 2011 sur les contours 2025 sans avertissement ni table de passage** | Sources et candidats privés audités, droits à confirmer |
| **V-06** | P1 | Finesse maximale **sans réidentification** : indicateurs de disponibilité des données, petits effectifs grisés, quantiles et distributions pondérées, localisation indirecte impossible. Corrélation avec bâti uniquement **à la maille territoriale** et avec contrôle des variables confondantes | Politique de sécurité déjà établie ; analyses à créer |
| **V-07** | P1 | Étudier commerces et bureaux **dans un chapitre distinct** de la vacance résidentielle ; seulement s'il existe une source statistique adéquate, millésimée et légalement diffusable | Recherche préliminaire seulement |

## Rail B — Évolution du bâti / reconstitution (parallèle, environ 30 %)

| ID | Priorité | Livrable et critère de validation | État au 17/10 |
| --- | --- | --- | --- |
| **B-01** | P0 | Examiner la **PR #28 IGN 2008/2011/2018** en brouillon : 2011/2018 ≈ 97 % des IDs communs, mais **2008 très peu comparable**. Ne jamais interpréter différence de densité du référentiel comme constructions | PR de recherche ouverte, pas en production |
| **B-02** | P1 | Comparaison spatiale 2011 ↔ 2018 : intersections, tolérances, scissions/fusions, classes et surfaces, audits GEOS et échantillon réel ; classer « modification de géométrie du référentiel » séparément de « changement physique attesté » | **Audit exact exhaustif réalisé dans PR #28** : 113 634 ID communs, 112 567 géométries identiques, 1 067 changées ; IoU GEOS sur les formes changées (médiane 0,908579). Concordance spatiale **des ID différents** et scissions/fusions encore à étudier |
| **B-03** | P1 | Analyser BD TOPO **mars et septembre 2018**, puis améliorer la compréhension de l'édition 2008 et des différences de couverture avant toute série cartographique | Candidats historiques identifiés |
| **B-04** | P1 | **Paris qui apparaît en couleur** : animation / curseur de jalons géographiques authentiques, avec affichage discret de couverture et incertitudes ; ne pas colorer 1830, 2008 ou une année arbitraire en prétendant disposer d'une observation annuelle | Prototype privé 2011/2018 |
| **B-05** | P2 | Annexes de datation patrimoniale (Apur périodes attribuées, cadastres anciens, plans) : conserver « date de construction attribuée », « date du plan », « date du référentiel » comme dimensions distinctes | Apur périodes et hauteurs publiées sous ODbL |

## Critères communs

- Toutes les cartes et graphiques donnent **source, date, périmètre, unité, dénominateur, méthode, limites et droits**. Les séries hétérogènes ne sont **pas** une unique courbe comparable sans signalement.
- **Vacance IRIS/arrondissement/Paris = statistique territoriale**, jamais statut d'un appartement ou d'un bâtiment. Les catégories « résidences secondaires / occasionnels » et « vacants » ne s'additionnent pas implicitement dans les taux.
- Les vraies emprises anciennes sont des **états documentaires**, pas une preuve automatique de démolition/construction. Licence IGN des archives miroirs à valider avant toute redistribution.
- Un contrôle de provenance dans le code, tests unitaires et recette navigateur quand une UI change ; pas de migration ni publication automatique à partir d'un fichier de recherche.
- **Ordre immédiat** : V-02 + V-01 (PR #29) → **V-03 comparateur arrondissements (PR empilée en préparation)** → V-04 LOVAC agrégé public et distinct. En parallèle : B-01 (PR #28) → B-02 (concordance spatiale). Ensuite V-04 (LOVAC).
