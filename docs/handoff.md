# Passation prioritaire — PR #37, dénominateurs BDCOM (17/10/2026)

**Branche** `dev/bdcom-denominator-provenance-20261017` empilée sur #36. **Parcs recensés** : 2017 **83 720** (fiche Apur d'origine), 2020 **83 399** (somme de `localrdc` des 20 arrondissements depuis la structure BDCOM2020), 2023 **83 154** (couche BDCOM2023). Ce sont trois **périmètres documentés** ; les numérateurs ne sont pas prouvés historiquement harmonisés, et la page ne calcule aucun taux longitudinal.

**Différences encore ouvertes** : en 2017 la publication originale recense 7 804 locaux vacants alors que l'archive rétrospective inclut 7 853 vacants/travaux ; en 2020 le service original dénombre **1 517 locaux en travaux** (arrondi initial 1 520), mais la rétrospective de 2023 seulement **1 310**. L'écart de **207 travaux** recoupe largement celui de **200 locaux** de vacance regroupée, sans preuve de la cause du recalcul. L'addition brute des catégories `bdcom2020_structure` donne 83 390 contre 83 399 locaux en 2020, et 84 023 contre 83 720 en 2017. Ne pas employer ces additions comme dénominateurs. Voir [audit détaillé](bdcom-historical-audit-20261017.md).

**Restant** : contrôler HEAD GitHub, locks AgentCTL, tests JS/Python, recette Chromium, compléter SHA/test final puis laisser PR brouillon. Obtenir auprès d'Apur la signification des révisions avant un taux interprété comme tendance ou flux. Les bureaux en m² et logements Insee/LOVAC sont des univers distincts. Chaîne #29 → #30 → #31 → #32 → #33 → #34 → #35 → #36 → #37, #28 IGN parallèle. Production inchangée.

---

# Validation finale PR #36 — 17 octobre 2026

**PR [#36](https://github.com/Kiwinokoto/vacant/pull/36)** brouillon sur `dev/bdcom-historical-comparison-20261017` empilée sur #35. **Code recetté `6868825d5fb5e03a82971a072cf4bdb98e331004`** : **109/109 tests JavaScript et 99/99 Python**, `node --check`, `git diff --check`, clone propre. **Chromium réel** serveur local desktop 1440×900 et mobile simulé 390×844 : trois lignes 2017/2020/2023, trois barres, vingt lignes BDCOM 2023 présentes, années rendues sans espaces, aucun débordement et zéro erreur JavaScript.

**Résultats historiques en effectifs, aucun taux harmonisé** : 2017 (6954 vacants +899 travaux =7853), 2020 (7247 +1517 =8764), 2023 (7495 +1565 =9060). Écarts Apur réels : 2020 publication de 2021 **8760**, rétrospective 2023 **8560**, API **8764**. Ne pas interpoler, attribuer des causes ou appliquer des taux aux adresses/bâtiments. Sources, requêtes, licence et limites : [audit BDCOM historique](bdcom-historical-audit-20261017.md).

**Prochaines actions** : clarifier l'écart de 200 locaux 2020 avec l'Apur ; vérifier les dénominateurs par édition avant tout taux ; qualifier séparément la vacance réelle des bureaux et son potentiel de transformation. Site public non modifié. Avant reprise : HEAD, locks, CI et chaîne #29 → #30 → #31 → #32 → #33 → #34 → #35 → #36, #28 séparée. Ne pas fusionner sans revue.

---

# Passation prioritaire — VACANT / comparaison BDCOM 2017–2023, PR #36

Au 17/10/2026 : PR **#36** brouillon, branche `dev/bdcom-historical-comparison-20261017` empilée sur PR #35 (`8945896`). **GitHub est la vérité**. Série en **effectifs uniquement**, indépendamment du parc de logements : 2017 **6 954 AA101 + 899 AA102**, 2020 **7 247 AA101 (dont 3 minuscules) + 1 517 AA102**, 2023 **7 495 AA101 + 1 565 AA102**. Les données publiques ArcGIS Apur sont agrégées : pas de fichiers d'adresses ou points. Audit `docs/bdcom-historical-audit-20261017.md`, affichage dans `site/potentiel.html`.

**Divergence bloquante pour un taux harmonisé :** Apur 2020 annonce **8 760** dans les premiers résultats de 2021, mais **8 560** dans la rétrospective de 2023, contre 8 764 dans la couche 2020 ; 2023 contient 9 060 dans l'API mais la note annonce 9 059. Ne pas fabriquer d'explication ni un taux 2017/2020 en utilisant le stock BDCOM 2023. Bureaux : offre de marché ~1,5 M m² juin 2026 distincte du potentiel d'accueil. Aucune possibilité d'hébergement sans expertise, aucun taux à l'adresse/bâtiment.

**Tâches restantes :** confirmer tests complets JS + Python, recette Chromium desktop et mobile simulé, statut AGENTCTL, mettre à jour commit final recetté, attendre clarification Apur. Chaîne #29 → #30 → #31 → #32 → #33 → #34 → #35 → #36, #28 IGN parallèle. Ni fusion ni déploiement automatique. Release prod historique `8711f307` inchangée.

---

# Validation finale PR #35 — 17 octobre 2026
Branche `dev/bdcom-groundfloor-snapshot-20261017` sur PR #35 en brouillon, empilée sur #34. Code contrôlé `041c3bd` : **105 tests JS, 99 Python**, Chromium desktop 1440×900 et mobile simulé 390×844, 20 arrondissements, classement modifiable, zéro débordement. L'audit Apur des 83 154 locaux distingue **7 495 hors travaux**, **1 565 en travaux**, contre un **regroupement de 9 060** (+1 sur les 9 059 de la note). **Bureaux Paris** : ≈1,5 M m² d'offre disponible fin juin 2026, non convertis en « logements ». Sources et limites : [audit](bdcom-open-audit-20261017.md).

Suite : demander confirmation à l'Apur sur l'écart +1 et le calendrier terrain 2023, clarifier la divergence Colliers mars/juin 2026 ; analyser BDCOM 2017/2020 seulement à schéma et définitions compatibles, travailler la faisabilité des bureaux sans « nombre de places » artificiel. **Aucune fusion ni mise en production**. Verrou AgentCTL à vérifier/libérer après écriture. Ordre #29 → #30 → #31 → #32 → #33 → #34 → #35 ; #28 IGN à part.

---

# Dernière reprise — PR #35, BDCOM 2023 et offre de bureaux (17/10/2026)

**Github source de vérité ; PR #35 brouillon `dev/bdcom-groundfloor-snapshot-20261017` empilée sur #34.** Chaîne antérieure #29 → #30 → #31 → #32 → #33 → #34 ; #28 IGN indépendante. À reprendre en lisant [audit des sources](bdcom-open-audit-20261017.md), [méthode potentiel](potentialite-locaux-20261017.md), [roadmap](../ROADMAP.md) et AGENTS.md.

- **Données BDCOM réelles** : source [ArcGIS Apur couche 1](https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2023/MapServer/1), enquête 2023, ODbL ; **83 154** locaux, 20 arrondissements ; `codact=AA101` = **7 495 vacants hors travaux**, `AA102` = **1 565 en travaux**, regroupés `type=V` = **9 060**. Note Apur annonce **9 059** et 1 565 travaux. Décalage de 1 **non expliqué**, sans retouche ; couche 0 plus restrictive contient 60 845 commerces contre 60 846 de la note. Date terrain avril/juin selon les deux sources : année 2023 certaine.
- **Bureaux Paris intra-muros** : **1,542 million de m²** annoncés par Colliers en juin 2026, C&W ≈1,5 million, source d'offre immédiate, **pas de m² immédiatement convertibles en logements**. Colliers annonce 795 000 m² T1 : incohérence non résolue, éviter série T1/T2.
- Code envisagé : page `site/potentiel.html` enrichie, agrégat `site/data/bdcom-paris-arrond-2023.json` limité à 20 lignes, contrat `site/bdcom-contract.mjs`, table de classement, tests. Aucun détail nominatif ou adresse. Source open data ODbL, attribution Apur ; autres chiffres Insee/LOVAC non additionnés.
- **Reste à réaliser lors de la reprise** : vérifier HEAD #34/#35, verrou AgentCTL avant mutation, tests JS/Python et recette navigateur sur la PR ; actualiser le dernier SHA testé puis laisser PR brouillon hors production. Ensuite, examiner BDCOM 2017/2020 et résoudre la divergence Apur et Colliers, sans inventer de nombre de logements ou places mobilisables.

**Contraintes durables :** ne pas transformer une statistique territoriale en statut de bâtiment, pas de logement jugé habitable sur simple vacance, pas de publication de fichier BDCOM point/adresse, pas de fusion/main ni déploiement avant revue.

---

**Recette #34 vérifiée** : 102 JS, 99 Python, Chromium desktop 1440 et mobile simulé 390 sans débordement, liens 3/3 OK, aucune erreur JS de la nouvelle page. Branche `dev/vacancy-reuse-potential-20261017` initialement à `5d4cde6`, PR en brouillon. Prochaine vérification : audit des données BDCOM originales et bureaux. Aucun déploiement.

# Dernière passation — PR #34, réemploi des espaces vacants (17/10/2026)

Nouvelle demande prioritaire : **distinguer logements habitables, logements dégradés, bureaux et commerces sans exclure les locaux aujourd'hui non habitables** du potentiel d'accueil étudié. Les espaces non résidentiels nécessitent expertise technique/juridique préalable (sécurité, santé, accès, eau, évacuation, autorisations) : aucune disponibilité immédiate affirmée. Destinations / état / occupation / transformation sont des dimensions indépendantes ; **inconnu par défaut**.

**PR #34** `dev/vacancy-reuse-potential-20261017` est empilée sur **#33**. Page `site/potentiel.html` : Insee RP2023 139 075 vacants du parc total ; LOVAC 2026 105 785 privés vacants (observation 01/01/2025) ; Apur BDCOM 2023 **9 059 locaux vacants sur 83 154 locaux en rez-de-chaussée**. Ces mesures **ne s'additionnent pas** et ne prouvent aucune possibilité d'accueil. Les bureaux en étage ne sont pas recensés dans BDCOM. Documentation `docs/potentialite-locaux-20261017.md`.

Chaîne des PR : #29 → #30 → #31 → #32 → #33 → #34, #28 indépendante. GitHub autorité ; aucune modification prod. Revoir HEAD/tests/navigateur et AgentCTL avant mutation/fusion/déploiement. Suite : audit schéma et licences BDCOM, puis source spécifique bureaux vacants Paris ; ne jamais extrapoler des mètres carrés en places d'hébergement.

---

# Reprise immédiate — VACANT, PR #33 (17/10/2026)

**Nouvelle lecture LOVAC longue durée en PR brouillon [#33](https://github.com/Kiwinokoto/vacant/pull/33), empilée sur #32, elle-même sur #31 → #30 → #29.** Voir [passation actualisée](PASSATION-LOVAC-2026-10-17.md) et [analyse scientifique](lovac-long-duration-20261017.md). Le rail B IGN reste en #28 séparée. Source de vérité GitHub. Aucune fusion, aucun déploiement : release publique `8711f307` préservée.

Code vérifié au commit `717f5bd` : **98 tests JS, 99 Python**, Chromium desktop/mobile simulé, vrais contours IGN 2025, 20 polygones/rangs/lignes, ratio LOVAC 2026 **26 264 / 105 785 = 24,8 % parmi les vacants privés**, maximum de part dans le 8e et d'effectif dans le 18e. Ratio interdit pour 2023 (dates distinctes), aucune projection d'un taux au parc total, à l'IRIS ou à un bâtiment. Correctif de sélecteur pour écran 390 px validé. Prochain travail : revue/promotion dans l'ordre des PR seulement avec contrôles, puis approfondissements territoriaux à dénominateurs homologues. Sécurité : jamais LOVAC individuel.

---

# VACANT — passation prioritaire du 17 octobre 2026 : VACANCE D'ABORD, BÂTI EN PARALLÈLE

**Lire en priorité [ROADMAP.md](../ROADMAP.md) et [le protocole temporel 1968–2023](vacance-evolution-1968-2023.md).**

- Le porteur du projet rappelle sa mission **fondamentale : mesurer, cartographier et comprendre l'évolution de la vacance résidentielle**, avec la maille la plus fine crédible. L'histoire et la reconstruction graphique du bâti sont un **deuxième rail**, esthétique et documentaire ; effort indicatif 70 % vacance / 30 % bâti. Desktop prioritaire, petits écrans utilisables sans recette obligatoire sur téléphone physique.
- GitHub est la vérité, branche de travail actuelle `dev/vacancy-timeline-and-roadmap-20261017`, départ de `main=22f0ad1a07f0c8ea5bc6931c6369df410fac65bc`. Production active `8711f3071abd41b169c92dfe0daaa79708be9acf` ; ne pas confondre avec la tête documentaire de main. AgentCTL `repo:Kiwinokoto/vacant` et `state:vacant` pris pour la passe, à libérer après fin des tests.
- **Rail V/V-02 implémenté sur branche, avant fusion :** nouvelle page `site/evolution.html` avec **9 jalons Insee** historiques pour Paris entier (1968, 1975, 1982, 1990, 1999, 2007, 2012, 2017, 2023), graphique de barres (part / nombre) et tableau. **Rupture visuelle entre les dénombrements anciens et les RP rénovés.** Source officielle Insee LOG T1 `https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75`, 2023 : **139 075 / 1 402 024 = 9,9 %**. Pas d'interpolation ni projection sur un bâtiment, une adresse ou un IRIS. `site/evolution-data.mjs` et tests dédiés.
- **Quatre jalons de carte** 2006, 2011, 2016, 2023 conservés : leur source/historique est distinct du tableau 2007/2012/2017 de la nouvelle page. Ne pas injecter ces années historiques dans la carte des arrondissements.
- **V-03 comparateur d'arrondissements implémenté en PR empilée** sur la branche `dev/vacancy-arrondissement-compare-20261017` : 2006/2011/2016/2023, deux années, taux en points de pourcentage et nombre absolu, vingt rangs, sources et dénominateurs Insee, frontières IGN 2025 d'affichage ; tests Chromium desktop et mobile simulé réussis. Voir [protocole V-03](vacance-arrond-comparison-20261017.md). Aucun déploiement.
- **Rail V/V-01 implémenté dans cette passe :** répartition des 992 IRIS par classes calculées sur des taux **non arrondis**, 852/929 affichables ≥5 %, 249/929 ≥12 %, 63 IRIS sous 50 logements grisés, taux Paris pondéré vérifié 9,9 %, sans mélange avec les couleurs des bâtiments. **Rail V/V-03 ensuite :** comparaison de deux RP par arrondissement en **nombre** et en **points de pourcentage**. **LOVAC agrégé public 2020–2026** constitue une série à part (parc privé fiscal, ruptures 2024/2025), jamais à joindre aux taux du RP. Aucun détail nominatif LOVAC.
- **Rail B :** la PR [#28](https://github.com/Kiwinokoto/vacant/pull/28) d'audit IGN 2008/2011/2018 est en brouillon, séparée ; ~97 % d'IDs communs en 2011/2018, édition 2008 non directement comparable. La recherche parallèle PR #28 a désormais un **audit exact des 113 634 IDs communs** : 112 567 géométries identiques, 1 067 modifiées, IoU GEOS des changements ; aucune démolition/construction inférée. Les polygones historiques sont privés. Ne pas faire de fausses constructions/démolitions.
- Déploiement : PR documentaire et tests d'abord, aucune promotion automatique de cette tranche. Le prochain agent doit reprendre en inspectant les PR, finaliser les tests et prioriser la lecture de la vacance sur la page d'accueil. Les anciennes notes ci-dessous restent historiques.

---

# VACANT — état de production au 17 octobre 2026

**Déploiement Apur ODbL terminé et vérifié.** Voir [le procès-verbal de mise en ligne](apur-odbl-deployment-20261017.md) avant toute nouvelle intervention.

- **Production active** : `https://vacant.kiwinokoto.fr/`, release GitHub `8711f3071abd41b169c92dfe0daaa79708be9acf`. Les PR #23, #24, #25, #26 ont été fusionnées **sans squash** ; `main` a désormais progressé depuis `72a9d063`. Les anciens checkpoints qui parlent de « PR en brouillon non fusionnée » sont **historiques**.
- **ODbL public** : © Apur, archive adaptée de **456 cellules GeoJSON**, 128 089 emprises uniques, ZIP 28 106 318 octets SHA `9bef60651f2b0f20158392157ffe2e0a6757257a57757532348384e4521e9e24`, manifeste public SHA `2b0683c33e236b906163c73786133f300182ccc4f00c70485bbcf1e84eb75711`. Téléchargement libre via `/data/apur-grid/` (manifeste, NOTICE, cellules, ZIP).
- **Carte publique** : périodes attribuées Apur et hauteur médiane `h_med` en mètres, séparées des taux de vacance IRIS et arrondissements. **Aucune déduction de vacance à l'immeuble**. Millésime scientifique Apur toujours non confirmé ; extraction figée le 16/10/2026.
- **Tests post-déploiement** : 75/75 Node, 93/93 Python ; Nginx gzip `Via`, ZIP/manifeste et droits vérifiés via URL publique ; vrai Chromium HTTPS desktop 1280 et mobile simulé 390, 2 284 emprises, passages de couches réussis sans erreur JS. Pas de téléphone physique par choix du porteur de projet.
- **Rollback préservé** : release précédente `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`, procédure dans le procès-verbal. Nouveau répertoire stable `/srv/vacant/work-release-8711f307`. Ne pas réécrire les anciennes releases.
- **Prochaine priorité** : reprise scientifique de VACANT, datation historique distincte de la période Apur, optimisation de navigation desktop ; vérifier les nouvelles réponses Apur de `data@apur.org`. GitHub est la source canonique de tout changement.

---

# VACANT — passation du 17/10/2026 : base adaptée Apur ouverte sous ODbL

**Nouvelle priorité : [notice scientifique, attribution et protocole public](apur-odbl-public-dataset-20261017.md).** Le téléphone physique n'est **pas un prérequis** demandé par l'utilisateur ; conserver une responsivité correcte, privilégier le desktop.

- GitHub canonique `Kiwinokoto/vacant`. `main` avant travail `72a9d06377541b7b266e0d8153e89a7ae19afb95`. PR #23 consolidation → #24 raccordement → #25 release sûre, et branche de distribution `dev/apur-odbl-public-distribution-20261017` basée sur #25. User autorise fusion et déploiement **si les contrôles sont satisfaisants** ; choisir méthode merge qui conserve l'historique et déploiement avec rollback.
- Apur ODbL 1.0 : la base adaptée est **distribuée sous ODbL** elle-même, avec attribution source/lien licence, extraction du 16/10/2026, limites scientifiques (millésime métier non attesté), 104 géométries invalides/13 ID absents exclus et méthode de reproduction. Ne jamais qualifier les emprises de « vacantes ».
- Export original privée : SHA `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`; grille vérifiée 456 cellules, 128089 uniques, SHA manifest source `bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c`. Une **copie publique dérivée distincte** est préparée via `scripts/package_apur_public.py`.
- Manifest public reproductible SHA `2b0683c33e236b906163c73786133f300182ccc4f00c70485bbcf1e84eb75711`, archive ODbL complète `apur-paris-grid-500m-2026-10-16-odbl.zip`, **28 106 318 octets** SHA `9bef60651f2b0f20158392157ffe2e0a6757257a57757532348384e4521e9e24`. Les 456 cellules, manifeste public, NOTICE et ZIP sont inclus **uniquement** lors de la préparation explicite `stage_reviewed_release.py --publish-apur`; aucun GeoJSON dans Git.
- Le script exige les SHA indépendants et refuse toute publication implicite. Tests synthétiques et **préparation réelle réussie sur /tmp**, 459 fichiers en sortie, permissions 755/644. ZIP reproduit deux fois **bit pour bit**. Origine privée préservée.
- Cartographie Apur rendue disponible sur le domaine public dans le code : périodes (12 classes), hauteurs médianes en mètres (6 classes), une carte/une couche active à la fois ; les deux prévisualisations historiques de 150 emprises restent réservées au laboratoire localhost. Téléchargement ODbL et notice visibles dans la colonne desktop. Manifest et cellules sont contrôlés SHA par le navigateur après HTTPS.
- Chromium **HTTPS local avec résolution du domaine public en 127.0.0.1** : desktop 1280×800 et mobile simulé 390×844 validés, **2 284 emprises uniques sur 4 cellules**, période ↔ hauteur sans nouvelle requête, zéro erreur JS et zéro overflow horizontal ; HTTP non sécurisé n'offre pas Web Crypto, d'où recette HTTPS. **Ce n'est pas encore un déploiement public**.
- Tests avant finalisation sur branche : **75/75 JavaScript et 93/93 Python**, à rejouer sur commit final ; passer la PR en ready seulement après revue de portée, puis fusionner la chaîne dans l'ordre si autorisé et vérifier HEAD après chaque étape. Générer la release réelle depuis le main fusionné après locks de déploiement, QA locale Nginx et rollback.
- Source de vérité antérieure : [revue gzip et sécurité](apur-publish-readiness-20261016.md) + [plan des PR](apur-review-merge-plan-20261016.md). Aucune annonce de mise en production sans HTTPs/ZIP/manifeste/QA réellement vérifiés.

---

## Mise à jour — recette Nginx réelle et ordre des PR (16/10/2026, fin de soirée)

- Chaîne de revue, **non fusionnée** : [ordre des PR #23 → #24 → #25](apur-review-merge-plan-20261016.md). Les anciennes PR #17–#22 restent intactes. Nouvelle proposition gzip dans `deploy/nginx.conf` **non déployée**.
- Recette **native Nginx 1.18** avec `scripts/recipe_nginx_gzip_loopback.py` : port éphémère lié exclusivement à `127.0.0.1`, **données synthétiques seulement**, HTTP gzip et identity conformes, `Vary: Accept-Encoding`, MIME GeoJSON/JSON/JS vérifiés, petites réponses non compressées, dotfiles 403 et absent 404. Test spécifique d'une requête avec en-tête `Via` réussi grâce à `gzip_proxied any` derrière un reverse proxy. Processus Nginx de recette arrêté. Aucune géométrie Apur privée servie.
- Résultats du vrai jeu de données inchangés : 456 cellules 91,5 Mo brut, gzip 27,4 Mo, Brotli 23,1 Mo ; dans le navigateur à débit 1,6 Mbit/s et 150 ms simulés : **9,0 s → 3,3 s** pour 2 284 emprises uniques avec gzip. **Pas de téléphone physique**.
- `deploy/README.md` prescrit la préparation sûre Git-only et la recette Nginx isolée. Contrats SIG/ODbL et distinction vacance territoriale / emprises Apur inchangés ; aucun déploiement, `main` figée à `72a9d063` au départ. Voir [rapport](apur-publish-readiness-20261016.md).
- Avant toute nouvelle écriture, revalider GitHub et les leases AgentCTL ; finir la présente session en libérant le verrou `repo:Kiwinokoto/vacant`.

# VACANT — passation prioritaire : revue de release et compression Apur (16/10/2026)

**Consulter d'abord [la revue de prépublication](apur-publish-readiness-20261016.md), puis [le raccordement local](apur-grid-site-local-20261016.md) et [la consolidation](checkpoint-apur-consolidated-20261016.md).**

- GitHub canonique `Kiwinokoto/vacant`. `main=72a9d06377541b7b266e0d8153e89a7ae19afb95` au début ; **PR #23** consolidation, **PR #24** raccordement local, cette branche de revue `dev/apur-release-gate-review-20261016` basée sur #24. Aucune fusion vers `main` ni déploiement.
- **Danger corrigé dans la procédure :** `cp -r site/*` peut embarquer les 456 cellules privées ignorées par Git. Nouveau `scripts/stage_reviewed_release.py` : prépare seulement une release **neuve**, à partir des fichiers `git archive` d'un SHA Git vérifié, avec les **deux GeoJSON publics explicitement autorisés et vérifiés SHA**, et **aucune géométrie Apur**. Nouvelle procédure obligatoire dans `deploy/README.md`. Le script **ne déploie rien**.
- Compression observée sur les **456 cellules Apur**, total brut **91 515 440 octets** → gzip-4 **27 435 040** (−70,0 %) ou Brotli-4 **23 089 233** (−74,8 %). Manifeste 152 865 → gzip 39 096 / Brotli 36 314 octets. Aucun dérivé modifié ou écrit.
- Emulation Chromium 390×844 à **1,6 Mbit/s, 150 ms de latence**, **2 284 emprises uniques** : brut **8 973 ms / 1 610 329 octets transmis**, gzip-4 **3 297 ms / 466 240 octets transmis**. **Pas de téléphone physique ni réseau réel** ; Nginx public inchangé.
- ODbL Apur confirmée dans sa fiche officielle de 2019 ; licence sections **4.2–4.7** : attribution, partage à l'identique pour base dérivée publiée, accès au dérivé/méthode et pas de restriction technique incompatible. **Millésime scientifique toujours non attesté** et aucun bâtiment vacant identifié par la couche Apur.
- Tests de sécurité : **7 nouveaux** avec clone synthétique, puis staging réel dans `/tmp` avec IRIS/arrondissements publics et **zéro donnée Apur copiée**. Suite Python consolidée auparavant **81/81**, nouvelle passe **88/88** et suite Node **71/71** à valider sur le commit final. Revalidation de `main`/release et nettoyage des clones avant fin. AgentCTL `repo:Kiwinokoto/vacant` acquis, libérer en fin de passe.
- **Ne pas fusionner ni activer** avant revue de la chaîne PR #23 → #24 → PR de sûreté, tests de serveurs gzip et téléphone physique, conformité à l'ODbL et décision explicite.

---

# VACANT — passation prioritaire : grille Apur dans le laboratoire VACANT (16/10/2026)

**Lire d'abord [le checkpoint d'intégration](apur-grid-site-local-20261016.md), puis [la consolidation #23](checkpoint-apur-consolidated-20261016.md).** Les notes plus anciennes ci-dessous restent historiques.

- GitHub source canonique : `Kiwinokoto/vacant`, `main 72a9d063` au départ, PR #23 à `242799a8` (base de travail). Branche de suivi empilée : `dev/apur-grid-site-local-20261016`, PR de revue à retrouver sur GitHub. **Aucune promotion main ni déploiement.**
- Le site VACANT possède désormais, **seulement sur localhost + `?apur_lab=1`**, deux nouvelles options : **grille privée de Paris 500 m — périodes** et **grille privée — hauteurs médianes en mètres**. Prévisualisation de 150 emprises conservée. Aucun bâtiment n'est désigné vacant.
- Contrat partagé `site/apur-grid-client.mjs`, laboratoire historique réexporté par `experiments/apur-grid/grid-client.mjs`. Manifeste SHA `bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c`, **456 cellules, 128 089 objets uniques**, 104 invalides GEOS et 13 clés métier nulles exclues à la source. Ressources privées sur VPS, jamais dans Git ni la release.
- Chargement à la demande de cellules visibles, plafond 12 cellules / 10 Mo / 5000 occurrences, SHA et dédoublonnage avant toute mutation. Périodes ↔ hauteurs change seulement la couleur (**0 requête**). Après déplacement, bouton de rechargement ; fichier cassé (503)/SHA non conforme préserve l'ancienne carte.
- Recette Chromium desktop 1280 et mobiles simulés 390/320 validée, et transitions Apur → IRIS → arrondissements → volumes validées. Tests JS **71/71**, tests Python **81/81** à reconfirmer sur commit final. Aucun appel API Apur, aucun débordement horizontal. Essais réseau **local**, pas de vrai smartphone/4G.
- Production inchangée `1e6d47c`, pas de modification Docker/BDD/DNS/SSH. Millésime Apur non confirmé ; ODbL et contrat de distribution de la base adaptée restent une condition de publication. Conserver PR #17–#23 tant que la revue n'a pas été faite. En fin de passe : vérifier état Git, libérer AgentCTL.

---

# VACANT — passation active : consolidation Apur (16/10/2026)

**Consulter d'abord [le checkpoint consolidé](checkpoint-apur-consolidated-20261016.md).** Les notes ci-dessous conservent le contexte historique, parfois devenu obsolète.

- Base GitHub `main=72a9d06377541b7b266e0d8153e89a7ae19afb95` ; branche de revue `dev/apur-consolidated-20261016`, PR à lire avant toute modification. Les PR #17–#22 ont été réunies **sans perdre leur ascendance Git**, et doivent rester ouvertes jusqu'à validation du remplacement.
- Tests d'assemblage initiaux : **66/66 Node**, **81/81 Python**. Recette sur la branche consolidée : Chromium desktop 1280×800 et mobile simulé 390×844, carte existante préservée, laboratoire invisible sans activation ; avec `?apur_lab=1`, fixture privée absente HTTP 404 refusée sans toucher aux volumes. Aucun débordement ni erreur JS. Les essais Apur réels complets restent ceux des PR sources. **Ne pas déployer avant revue.**
- Archive Apur privée SHA `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`. Grille 500m : **456 cellules**, **128 089 emprises uniques** ; **104 GEOS invalides et 13 clés métier nulles exclues**, compte rendu et manifeste dans le checkpoint. Les fichiers géographiques restent hors Git et hors site public.
- Interface VACANT : périodes et hauteurs Apur **uniquement sur localhost avec `?apur_lab=1`**, sur extrait de 150 objets ; grille Paris complète sous `experiments/apur-grid/` et **pas encore raccordée** au site. Aucune jointure de taux de vacance par bâtiment. Millésime scientifique Apur toujours non confirmé, ODbL à cadrer avant rediffusion.
- Production `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0` volontairement inchangée, ancienne release de secours préservée. Aucune migration, aucun déploiement ; gérer/verrouiller le dépôt via AgentCTL avant toute nouvelle écriture.

---

# VACANT — archives antérieures (16 octobre 2026)

**Point de reprise prioritaire : [checkpoint Apur du 16/10/2026](checkpoint-apur-20261016.md).** Ce document reflète le dernier état vérifié ; les rubriques ci-dessous constituent l'historique des passes précédentes et peuvent contenir des statuts anciens.

## Validation finale — 16/10/2026

- **PR #13 fusionnée et déployée** : code `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`, release de même SHA active sous `/srv/vacant/releases/<SHA>/site`. 25/25 Node, 40/40 Python, Chromium réel local **et public** (desktop/mobile, cartes des quatre millésimes, erreurs HTTP simulées) ; HTTP/HTTPS et deux GeoJSON historiques publics contrôlés, géométries candidates toujours HTTP 404. Ancienne release `2424a45ad590901e3c96c781e10d8b2309c874cb` conservée pour rollback. Pas d'évolution des données publiques.
- **PR #14 recherche Apur fusionnée** : dernier `main` `642538708c802eb551fcfecd48f1492d5fc0602e` avant cette mise à jour de passation. Audit agrégé Apur 128 206 emprises, 128 090 hauteurs médianes positives, 120 412 périodes renseignées, 47 056 années exactes manquantes. 25/25 Node et **48/48 Python**. Voir [audit Apur](apur-bati-audit.md), `scripts/audit_apur_emprises.py` et tests. **Aucune géométrie Apur extraite ni publiée**.
- Déploiement VACANT **volontairement au commit PR #13**, pas au `main` plus récent : la PR #14 ne touche qu'aux scripts d'audit et à la documentation. Ne pas redéployer inutilement.
- **Suite ordonnée** : exporter/sourcer précisément la couche Apur datée et vérifier les conditions ODbL, contrôler un échantillon de géométries/emprises et les trois hauteurs médianes au-delà de 200 m, puis prototype distinct « période de construction » et « hauteur médiane (m) » avec tests et mentions de limites ; ensuite retourner aux originaux IGN 2008/2018 et à la réponse IGN déjà sollicitée. Pas de taux de vacance par emprise/bâtiment.
- Branches locales sur VPS dédiées, non poussées directement ; contenus des commits publiés par connecteur GitHub avec identité de tree vérifiée. Agents/locks et services à revérifier à la prochaine reprise. Après cette passation, libérer toutes les leases `vacant`.

## Mise à jour — déploiement PR #13 et audit Apur (16/10/2026)

- **PR #13 fusionnée** au commit `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0` ; aucune action CI configurée. Tests 25/25 Node et 40/40 Python, recette Chromium locale puis **production** (quatre années, changement de couches, erreurs HTTP 503 simulées avec retour à la couche précédente, mobile 390 px) : `BROWSER_ALL_PASSED`.
- **Production effective** : release immuable `/srv/vacant/releases/1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0/site`, conteneur VACANT seul recréé via Compose, aucun redémarrage signalé. Certificat Let's Encrypt valide ; HTTPS 200 (accueil, fichiers JS et deux GeoJSON publics), HTTP 301→HTTPS ; fichiers historiques candidats HTTP 404. Données validées inchangées ; ancienne release `2424a45ad590901e3c96c781e10d8b2309c874cb` conservée comme retour arrière.
- **Audit Apur préliminaire** : 128 206 emprises EPSG:2154. `h_med` positive dans 128 090 cas ; `c_perconst` connue dans 120 412 ; `an_const` manquante dans 47 056 cas. Source, chiffres, limites et suites : `docs/apur-bati-audit.md`. Requêtes agrégées seulement, aucune donnée d'objet enregistrée ni publiée. Code : `scripts/audit_apur_emprises.py`, tests synthétiques.
- Branche pour cette étape `dev/apur-heights-dating-audit`, base `main` au commit de production. Vérifier le HEAD, PR, état local et locks avant toute écriture. **Aucune nouvelle couche Apur** en production. Ne jamais attribuer un taux de vacance territorial à une emprise.
- La demande IGN des archives 2008/2013/2018 a bien été **envoyée le 16/10/2026** ; consulter Gmail pour sa réponse, ne pas réexpédier un doublon.

## Passe 16/10/2026 — éditions historiques et correctif ergonomique

- **Contrôles réalisés** : Node 25/25, Python 40/40. Chromium réel sur clone de la branche avec dérivés agrégés publics aux SHA validés (IRIS 2023 `0b79e30a...`, arrondissements `97667772...`) : bascule de couches, quatre années, labels de géographie, retour aux volumes, deux échecs réseau simulés avec restauration de la couche précédente, mobile 390 px sans débordement ; résultat `BROWSER_ALL_PASSED` le 16/10/2026. Aucune archive géographique historique non autorisée employée dans la recette.
- **Publication** : la branche ne déploie pas automatiquement la correction UI. Contrôler revue/PR/CI avant fusion et obtenir l'accord de déploiement avant modification de la release publique.

- GitHub main de départ : b492ede6567d68cc6df1b18db852d68eb4cf09c5 ; aucune PR ouverte ; branche dev/iris-archive-readiness dans clone /srv/vacant/work-geography-readiness. À la reprise vérifier HEAD, travaux locaux/agents, PR, CI et leases AgentCTL.
- Recherche : IGN Contours…IRIS édition 2008 v1.0 ; édition 2018 = IRIS 2017 consolidés + 2018 provisoires ; édition 2019 = IRIS 2018 consolidés + 2019 provisoires. Livraison 2018-06-08 avec dossier FXX-2017 non assimilable automatiquement au fond RP2016 géographie 2018. AUCUNE nouvelle archive 2008/2018 acquise ; détails : docs/iris-archive-readiness.md.
- L'IGN a déjà reçu le courriel le 16/10/2026. Ne pas réexpédier. La provenance juridique/date 2013 du candidat RP2011 reste à confirmer.
- Code modifié : site/index.html, site/app.mjs, site/view-state.mjs, site/iris-contract.mjs, tests/view-state.test.mjs et tests/iris-contract.test.mjs. Titre et sous-titre de carte changent selon la couche réelle. Légende des taux à intervalles disjoints ; retrait du texte erroné sur le sélecteur. Publication d'une géographie IRIS autre que 2023 refusée explicitement jusqu'à levée formelle du blocage ; validation privée permise.
- Aucune nouvelle couche 2011 publiée. Production connue : release 2424a45ad590901e3c96c781e10d8b2309c874cb, HTTP à revalider. Aucun Docker/BDD/service modifié pendant cette passe ; tests à exécuter, PR à soumettre, pas de déploiement sans recette navigateur et validation de la portée.
- Suite : récupérer vrai 2008 et 2018 consolidé, vérifier les droits 2013 auprès IGN, tester UX dans Chromium réel sur candidate avant déploiement.

## IGN — demande envoyée le 16/10/2026

- La demande de géométries historiques **Contours…IRIS® 2008, 2013 et 2018 (Paris, 75)** a été **envoyée depuis le compte Gmail connecté** à `contact.geoservices@ign.fr` le 16 octobre 2026 ; Gmail a confirmé le statut `SENT`. **Ne pas envoyer de doublon.**
- Objet : « Demande d’archives Contours…IRIS® 2008, 2013 et 2018 — Paris (75) ». Le message demande également l'attestation que le jeu Atlasanté nommé **2014** correspond bien à la géographie Insee **2013**, et la licence historique de rediffusion de dérivés GeoJSON. Texte technique de référence : [demande-archives-ign.md](demande-archives-ign.md) (version proche du courrier envoyé).
- **Réponse IGN non encore obtenue** à la date d'envoi. Avant de relancer, rechercher ce fil dans Gmail ; ne pas considérer le silence comme un accord de licence. Le contenu de `site/`, les fichiers géographiques privés, le conteneur et la production n'ont pas changé pendant cette opération.
- Nouvelle piste de recherche indépendante : une documentation tierce cite `CONTOURS-IRIS_2-1__SHP__FRA_2018-06-08` avec un sous-répertoire `...FXX-2017`. La date de livraison **2018** ne prouve pas une géographie de référence **2018** : vérifier la notice, les codes et les géométries avant tout appariement à RP2016. Archive non acquise.
- Pendant l'attente : chercher les **fonds IGN officiels 2008 et 2018**, contrôler édition/CRS/SHA/conditions juridiques ; privilégier les améliorations UI et le contrôle mobile indépendants des anciennes licences. Les couches fines historiques secondaires restent **hors production**.

## Fin de passe — Atlasanté 2014 (16/10/2026)

- PR #10 **fusionnée** en squash sur `main` : `67648885c9996604fd539506c975a14050783c7e`. Source locale `dev/iris2014-atlasante-geometry` sans changement non commité ; arbre GitHub de la PR vérifié identique à Git local. La branche documentaire présente ajoute uniquement cet état final.
- Archive institutionnelle Atlasanté `IGN – Métropole – IRIS 2014` privée : SHA `5cefdde58d228b3f8643d01ef61c80c10bf4ce30a30e78b61e2dc48fdf9acf27`. Ancien candidat dit 2013 : `c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7`. Les **992 contours Paris** coïncident à mieux que `0,000009 m²` près après reprojection.
- Auditeur `scripts/audit_iris2014_atlasante.py` : lecture uniquement du SQL institutionnel, jamais exécuté ; revalide toutes les archives précédentes et les 992 appariements. Tests **22/22 JavaScript et 40/40 Python**.
- Contrôle final production : conteneur actif, 0 redémarrage, release inchangée `2424a45ad590901e3c96c781e10d8b2309c874cb` ; accueil, IRIS 2023 et arrondissements historiques HTTP 200 ; candidats RP2011/Atlasanté HTTP 404.
- **Blocage externe restant :** attestation de correspondance officielle édition 2013 et conditions IGN/Insee de rediffusion (notice Atlasanté date la *publication de notice* en 2013 mais intitule le jeu **2014**). La [demande IGN](demande-archives-ign.md) est prête, **non envoyée**. Ne pas déployer de polygones 2011 avant confirmation des droits et du millésime.
- Toujours aucune édition originale authentifiée 2008 ou 2018 ; conserver comparaison historique par 20 arrondissements.
- Vérifier à la reprise GitHub HEAD et tous locks AgentCTL avant toute écriture ; ne pas prendre les clones VPS pour source de vérité.

## Mise à jour — Atlasanté 2014 / candidat 2013

- GitHub main vérifié au début : 38a8db3cb25ec677ea1c029aeb8c8addd2dc1387 ; branche dev/iris2014-atlasante-geometry. Revérifier les commits et verrous AgentCTL avant nouvelle écriture.
- Archive institutionnelle Atlasanté « IGN – Métropole – IRIS 2014 » ZIP (16 411 555 octets), PostGIS EPSG:2154 et ISO XML ; SHA-256 5cefdde58d228b3f8643d01ef61c80c10bf4ce30a30e78b61e2dc48fdf9acf27 ; sauvegardée privée et manifestée sous /srv/vacant/data/raw/secondary/iris-2014-atlasante/ et /srv/vacant/data/manifests/.
- 992 géométries Paris, zéro invalide. Recoupement avec le candidat tiers 2013 : IoU minimale/médiane 100 % à dix décimales, différence surfacique maximale 0,000008961 m². Auditeur scripts/audit_iris2014_atlasante.py, tests unitaires ; preuves docs/iris-2014-atlasante.md.
- Métadonnées : jeu intitulé 2014 ; publication de notice 2013-09-16 et révision 2015-04-29. Ces dates ne prouvent pas l'édition géographique 2013. Conditions IGN/Insee spécifiques mentionnées : pas de republication sans confirmation.
- Demande IGN précisée dans docs/demande-archives-ign.md et non envoyée. Les éditions 2008 et 2018 restent à rechercher.
- Production non modifiée : https://vacant.kiwinokoto.fr, historique par 20 arrondissements et IRIS fins uniquement en 2023. Aucune couche 2011 ni donnée individuelle publiée.
- Suite : validation officielle du millésime et des droits ; si obtenue, PR ciblée couche RP2011 avec contrôles SIG/navigateur. Sinon conserver le dérivé privé.

## Fin de passe — contrôle indépendant des contours IRIS
- PR #8 fusionnée dans `main` : `2e4e53372bdfb31501149c00adfaff0b0ce86be8`. La nouvelle branche historique de travail `dev/iris-independent-crosscheck` n'a pas été déployée ; code, tests et documentation uniquement.
- 22/22 tests JavaScript et 33/33 tests Python réussis. Relecture de trois séries de 992 contours, IoU médian candidat2013/OSM2013 = 1,00000, candidat2013/secondaire2016 = 0,93688 et secondaire2016/IGN2025 = 0,98472.
- Archives secondaires à accès privé `/srv/vacant/data/raw/secondary/` et manifestes SHA `/srv/vacant/data/manifests/` : aucun transfert dans `site/data`, aucune publication des couches 2013/2016.
- Demande des archives originales IGN 2008/2013/2018 préparée dans `docs/demande-archives-ign.md`, **non envoyée** : accès Gmail indisponible. Les jeux secondaires demeurent non certifiés.
- Suite : obtenir et auditer les livraisons authentiques IGN ou leur provenance officiellement attestée, vérifier droits et concordances SIG, puis envisager seulement une carte IRIS historique par année.

## Source de vérité / état réel
- Dépôt public : `Kiwinokoto/vacant` ; dernière base `main` confirmée avant cette passe : `53837c7fb0fa35ac6eb3797eb3c190e921c6b604`, PR ouvertes : aucune. Travail courant sur `dev/iris-independent-crosscheck`. Revalider GitHub, HEAD, remotes, état local, CI/protections et leases AgentCTL avant écriture.
- Production inchangée : https://vacant.kiwinokoto.fr, VPS personnel `vmi2505789.contaboserver.net` via RDC LGC, release active au début `2424a45ad590901e3c96c781e10d8b2309c874cb`. HTTPS et conteneur à revérifier en fin/reprise. Aucun déploiement voulu pendant les audits privés.
- Sources et dérivés **privés** dans `/srv/vacant/data/raw`, `/srv/vacant/data/manifests`, `/srv/vacant/data/processed` ; ne pas les pousser vers GitHub ni les exposer au webroot.

## Produit publié et données validées
- Vacance résidentielle Insee aux recensements 2006/2011/2016/2023 : affichage historique par **20 arrondissements** ; les valeurs sont agrégées depuis les IRIS de leurs millésimes, sans les attribuer à d'autres contours.
- Couche précise IRIS : **2023 seulement**, contours IGN géographie 2025, 992 IRIS et 929 taux affichés (petits parcs masqués). Aucune identification de vacance par logement, immeuble ou volume bâti.
- Couche Paris Data volumes actuels : nombres d'étages, pas hauteur métrique, plafond API de 800 volumes avec avertissement, retour de zoom en quittant les statistiques. Tests Chromium validés précédemment.

## Recherche SIG terminée ou en cours
- Références Insee : archives géographies 2008/2013/2018/2025, 992 codes Paris inchangés, contreparties RP2006/RP2011/RP2016 appariées. **Code identique ≠ géométrie identique.**
- Source secondaire candidate 2013 (republication 2015) : ZIP privé SHA `c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7`, dix occurrences par code mais écarts de duplication infimes ; 992 polygones SIG valides. Dérivé RP2011 privé, SHA `a1ea1c1cb78172d1b6725d55307026b0f3b5ae0094a8c130dbfd52d7c8b5a2b2`. Voir `docs/iris-2013-candidate.md`. Jamais publié.
- **Nouveau contrôle indépendant** : archive 2013 modifiée par OSM (ODbL), SHA `deb1b378aefa823ad3f2b22700c5c12b8133f782ddb87f059b1dc7518207a2c2`, et archive secondaire « 2016 » (pas géographie RP2016 2018), SHA `843049e9af98c25bb74f9c8d8fe84348429596a3bf69fb6406b77fa8951436cd`. Chacune contient 992 codes Paris uniques et 0 forme invalide. Comparaison métrique Lambert-93 : IoU médiane 2013/OSM **1,00000**, 2013/2016 **0,93688**, 2016/IGN2025 **0,98472**. Voir `docs/iris-crosscheck.md` et `scripts/audit_iris_crosscheck.py`.
- Les trois jeux historiques demeurent des **sources secondaires non authentifiées comme livraisons IGN d'origine** ; ne pas les publier, ni attribuer une édition 2018 au fichier 2016.

## Décisions, blocages, prochaines étapes
1. Vérifier le dernier commit GitHub, fermer la PR de cette passe après tests, actualiser passation et libérer locks. Ressources AgentCTL verrouillées pendant l'écriture : `repo:Kiwinokoto/vacant`, `state:vacant`.
2. **Blocage externe :** obtenir les Contours…IRIS IGN d'origine pour les géographies 2008, 2013 et 2018 ou une attestation vérifiable de provenance de l'un des jeux secondaires. Voir `docs/demande-archives-ign.md`. Le texte est prêt mais **aucun courriel n'a été envoyé** (accès Gmail non autorisé lors du contrôle).
3. Après réception : audits CRS/SHA/licence, 992 codes et formes, géométrie GEOS, IoU et ruptures, provenance, métadonnées, puis seulement envisager une PR d'affichage IRIS année par année avec tests navigateur. En attendant garder la carte par arrondissement.
4. Sujets indépendants : UX mobile, popups, favicon ; audit hauteur/datation du bâti Apur/IGN sans confondre l'âge de fiche et l'âge de construction.

## Sécurité / passation
- Aucune migration BDD, service tiers, modification Docker, déploiement ou donnée LOVAC individuelle dans cette passe.
- Ancien clone VPS `/srv/vacant/source` est périmé, ne jamais le prendre comme vérité. Nouveau clone : `/srv/vacant/work-iris-independent-crosscheck`.
