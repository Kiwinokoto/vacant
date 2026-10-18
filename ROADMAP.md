# VACANT — backlog priorisé, deux rails (18 octobre 2026)

## État de production du 18 octobre 2026

**Site public à jour** : `https://vacant.kiwinokoto.fr` sert le code `bcc1a97f00c85eb7f2de74cb37d86fbb98520d03` (PR #39, gate d'agrégats corrigé). Vérifié : **111 tests JS, 102 tests Python, Chromium 8/8 parcours desktop/mobile simulé sur HTTPS réel**, nouvelles pages 200, les deux GeoJSON et trois JSON 200, distribution des **456 cellules Apur ODbL** et empreintes intactes, privé exclu. Ancienne release conservée pour rollback ; les leases ont été relâchés. Ne pas confondre des futurs commits **purement documentaires** sur `main` avec un nouveau code déployé.

**Prochaine passe scientifique — précision des estimations plutôt que 3D :**
- **Résidentiel** : fournir par arrondissement nombre / taux / dénominateur Insee 2023 ; LOVAC 2026 séparé, observation 01/01/2025, logement privé fiscalement vacant et longue durée (26 264 / 105 785 = 24,8 % *parmi les vacants*). Ruptures de séries fiscal GMBI explicites, aucune interprétation bâtiment ou état de salubrité.
- **Locaux de RDC** : édition Apur 2026 `8 323` vacants hors travaux et `1 402` en travaux, sur `83 115` locaux enquêtés ; édition non harmonisée avec les archives 2017/2020/2023 ; attendre la méthode Apur avant courbe de taux.
- **Bureaux** : mesure publique la plus récente repérée pour **Paris** : `1 578 000 m²` d'**offre immédiate fin septembre 2026** (Cushman & Wakefield / ImmoStat 6/10), **pas** du nombre de bureaux physiquement déserts, ni du nombre de logements possibles. Colliers donne >`1 200 000 m²` vacants depuis >2 ans pour **toute l'Île-de-France**, interdit de reporter sur Paris. Chercher une mesure parisienne ventilée par durée / surface, bâtiments réellement désoccupés et travaux ; ne pas produire de « places » à partir des m². Source : https://www.cushmanwakefield.com/fr-fr/france/news/2026/10/reactions-immostat-t3-2026.
- **Mobilisable** : distinguer stock vacant constaté, état matériel, droits, délai/coût de transformation, et possibilité d'accueil après diagnostic. Fourchette seulement si chaque facteur est documenté, sinon **inconnu**.

**Rail B** historique IGN #28 toujours hors priorité et hors `main`. Voir `docs/handoff.md` pour la recette et la mise en production.


## Blocage de publication levé en branche — 18 octobre 2026

La nouvelle release doit intégrer **exactement trois JSON agrégés suivis par Git** (LOVAC 2026, BDCOM par arrondissement 2023, BDCOM historique 2017–2023). Correction ciblée dans `scripts/stage_reviewed_release.py` + trois tests, sans relâcher l'interdiction des jeux arbitraires ou privés. **Tests : 111/111 JS, 102/102 Python.** Le site public reste à mettre à jour par release immuable, **en conservant la distribution Apur ODbL** avec option `--publish-apur` et empreintes déjà consignées. Pas de déploiement sans vérifier AgentCTL, les montages, le rollback et les URL publiques.

**Piste scientifique étayée mais non additive** : Colliers mesure ~1,542 million de m² disponibles **à Paris** fin juin 2026 ; l'indicateur de **plus de 1,2 million de m² vacants depuis plus de 2 ans** de son analyse de conversion porte sur **l'Île-de-France**, donc n'est PAS une estimation de la vacance durable parisienne ni une capacité d'hébergement. Pas de série T1→T2 exploitable sans clarification. Il faut rechercher des données parisiennes par durée, surface réellement inoccupée, destination, état et contraintes juridiques avant toute estimation de réemploi. Sources : https://www.colliers.com/fr-fr/etudes/2026-2t-etude-marche-bureaux ; https://www.colliers.com/fr-fr/etudes/2026-transformation-des-bureaux-obsoletes-en-logements.


## Statut et priorité actualisés — 18 octobre 2026

**Livré sur GitHub `main`** : PR #29→#37 fusionnées dans l'ordre, arbre final du code identique à #37 `93a9ef78` ; référence d'intégration `16ce23487e80`. **Site public non redéployé** lors de cette passe. Contre-recette pré-merge : 111 JS, 99 Python, Chromium 49/50 contrôles stricts (404 de favicon uniquement). Pas de CI GitHub versionnée. La PR **#28 IGN** reste indépendante et non fusionnée.

**Priorités prochaines, rail V avant toute 3D :**
1. **Logements résidentiels** : tableau clair par année / arrondissement des effectifs, taux et dénominateurs Insee, avec LOVAC **séparé** pour le parc privé fiscalement vacant et la part de vacance de plus de deux ans. Afficher ruptures de méthode, couverture et incertitude ; aucune attribution à un immeuble.
2. **Espaces non résidentiels** : suivre BDCOM commerces/locaux de RDC **vacants hors travaux vs en travaux**, réconcilier si possible les versions 2017/2020/2023/2026 avant de tracer des évolutions harmonisées ; bureaux dans un univers distinct avec surfaces en m², dates, durée d'inoccupation et définition de l'offre.
3. **Potentiel de réemploi** : indiquer une **fourchette uniquement si les données et hypothèses peuvent la justifier** ; sinon conserver « inconnu ». Ventiler sécurité/habitabilité, état physique, transformation, disponibilité juridique et coûts/délais à instruire. Ne pas convertir mécaniquement surfaces ou locaux vides en logements ou places d'hébergement.

Rail B : recherches historiques IGN/Apur en parallèle, sans priorité d'affichage 3D et sans interpréter des mutations du référentiel comme de la construction/démolition.

*Les checkpoints « pas encore fusionné » plus bas sont conservés comme historique daté, et non comme état courant.*


## Checkpoint de recette — 18 octobre 2026 (sans promotion)

**Code de référence `599329f4` (PR #37)** : chaîne Git #29→#37 **strictement linéaire**, #28 IGN séparée. Revalidation indépendante : **111 tests JS + 99 tests Python réussis** en environnements temporaires. **Chromium 154** sur les quatre pages en 1440×900 et 390×844 : **49/50 vérifications strictes**, seule la demande navigateur de `/favicon.ico` renvoie 404 ; pas d'erreur applicative ni de débordement. Test des 20 arrondissements LOVAC/BDCOM, de la restriction de ratio LOVAC 2023, des 9 recensements Insee, de 992 IRIS, et de la présentation BDCOM 2026 **séparée**. Aucun ajout de données individuelles.

**Gate avant intégration** : aucune CI sur HEAD échantillonnés (#29/#33/#37), aucun workflow versionné dans cette branche ; compléter la recette et les protections avant promotion. La simulation d'intégration de #28 sur #37 signale des conflits sur `docs/handoff.md` et `docs/sources.md` : traiter #28 dans un second temps, sans mêler les deux rails. **Ne pas squash-merger une pile de PR sans recréer les bases** ; conserver l'ascendance lors du retarget successif ou reconstituer une pile revue. Pas de merge `main`, pas de déploiement ni de relance Apur. Détails dans [la passation](docs/handoff.md).


**Mission fondamentale : rendre visible et intelligible la vacance résidentielle à Paris — son niveau, sa répartition territoriale, son évolution et les limites de nos connaissances.** L'histoire du bâti est une seconde lecture graphique et scientifique, pas un substitut à la mesure de la vacance.

**Source de vérité** : GitHub `Kiwinokoto/vacant`. App desktop prioritaire, petits écrans utilisables sans recette sur téléphone physique obligatoire. Une PR `dev/*` courte, tests et revue avant toute promotion ; produire les dérivés depuis des sources figées, sans données nominatives LOVAC.

**Point de reprise PR #33 (17/10/2026) :** la PR #31 donne les agrégats LOVAC ouverts ; #32 ajoute leur carte par arrondissement ; **#33** étudie la vacance longue par **effectif et part parmi les vacants privés**, en interdisant le ratio 2023 (dates non alignées) et en exposant les ruptures 2024–2025. 98 JS et 99 Python, Chromium desktop et 390 px validés sur code `717f5bd`. Tout reste **en brouillon hors production** ; ordre #29 → #30 → #31 → #32 → #33, #28 en parallèle. Prochaine priorité scientifique : contextes/contrastes territoriaux sans comparer des taux incompatibles ni des immeubles.

## Périmètre transversal — espaces vacants et potentiel d'accueil (PR #34)

**Décision utilisateur du 17/10/2026 :** ne pas compter au même titre logements habitables, logements dégradés et bureaux ou commerces inoccupés, **sans exclure les espaces non habitables de l'étude**. Les garder comme potentiel de remise en état, transformation ou accueil temporaire éventuel, à **expertiser** : sécurité, hygiène, eau, ventilation, lumière, évacuation, accès, droits d'usage et délais. **Inconnu par défaut**, jamais « habitable » ou « mobilisable » par déduction statistique.

- **V-08 (P1)** — Protocole de potentiel d'accueil, distinguant destination, occupation, état d'usage, possibilités et contraintes. Première page `site/potentiel.html` en PR #34, note `docs/potentialite-locaux-20261017.md`. Ne pas produire de capacité d'accueil fictive.
- **V-07 (P1 renforcée)** — Locaux tertiaires/commerciaux : Apur BDCOM 2023 = **9 059 locaux vacants parmi 83 154 locaux enquêtés en rez-de-chaussée**, soit 10,9 % ; cette mesure n'est **ni** la vacance de tous les bureaux de Paris **ni** le nombre de logements convertibles. Prochaine enquête : audit BDCOM ouvert (champs vacance/travaux, licences) puis source de **bureaux réellement inoccupés à Paris intra-muros** (m², date, champ).

**Ordre de la pile avant revue : #29 → #30 → #31 → #32 → #33 → #34**. Rail B IGN #28 indépendant. Pas de fusion ni déploiement de ces travaux.

## V-07 — Note Apur BDCOM 2026, sources et révisions (complément PR #37)

**Premier résultat officiel octobre 2026 :** 83 115 locaux, 9 725 vacants travaux inclus, dont 1 402 travaux (8 323 hors travaux ; 11,7 % / 10,0 % selon Apur). La même publication **révise 2023** à 83 284 locaux / 9 104 vacants, versus 83 154 / 9 059 dans la publication initiale 2023, et 9 060 dans l'API 2023. Le texte de 2023 mentionne également **8 541** vacants 2020 là où le graphique indique **8 560**. **Ne pas harmoniser sans confirmation Apur.** Page `site/potentiel.html` avec photographie 2026 distincte du JSON historique 2017–2023. Interrogation méthodologique **envoyée le 17/10/2026** à `data@apur.org` via Gmail (message `1a149909decf1bfc`), distincte du courriel du 16/10/2026 sur les emprises bâties ; réponse non reçue ; demande de dictionnaires et tables de correspondance. Revue de la pile PR avant fusion ; GitHub combined statuses et check-runs vérifiés : aucun signal de CI associé aux HEAD contrôlés, ne pas assimiler « mergeable » à une certification de qualité.

## V-07 — Dénominateurs historiques retrouvés, compatibilité ouverte (PR #37)

La fiche Apur 2017 donne **83 720 locaux** ; le service Apur 2020 donne **83 399** (somme `localrdc`), et la couche 2023 **83 154**. Ce sont des **tailles de parcs par édition**, non une preuve que l'on peut comparer les taux. Le 2017 d'origine donne 7 804 vacants et la série rétrospective 7 853 vacants/travaux ; le désaccord 2020 (8 760 contre 8 560) se concentre en partie dans les **travaux : 1 517 contre 1 310**. La raison de ces révisions est inconnue. La page « Potentiel » affiche désormais la couverture des enquêtes, sans fabriquer de taux harmonisés. Détails : `docs/bdcom-historical-audit-20261017.md`. Prochaine action : demander métadonnées des éditions à Apur et valider les conventions des numérateurs avant une courbe de taux. Chaîne en brouillon #29 → #30 → #31 → #32 → #33 → #34 → #35 → #36 → #37 ; IGN #28 distincte.

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
