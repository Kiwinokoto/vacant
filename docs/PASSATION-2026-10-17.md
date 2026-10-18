# Mise à jour de la passation — V-03, 17 octobre 2026

**Lire cette section en premier en cas de reprise dans un nouveau chat.** Le présent fichier existe dans la branche de développement **`dev/vacancy-arrondissement-compare-20261017`**, qui part de la branche **PR #29** (non directement de main), et figure désormais dans la **[PR #30 empilée](https://github.com/Kiwinokoto/vacant/pull/30)** en brouillon. Les anciennes mentions ci-dessous de « V-03 prochaine tâche » sont historiques ; **V-03 est maintenant codé et recetté hors production**.

- **Priorité immédiate désormais V-04 : LOVAC ouvert et agrégé 2020–2026**, à la seule maille Paris commune et pour le **parc privé** ; *répartir en deux séries/points distincts si les méthodologies sont non comparables*. Rechercher et vérifier les **fichiers publics d'origine, dictionnaires des variables, définitions et licences**, puis contrôler les ruptures GMBI (LOVAC 2024) et extraction fiscale (2025). **Ne jamais utiliser ni chercher à publier LOVAC détail adresses/propriétaires**, jamais joindre ces données à un immeuble Apur/IGN.
- **V-03 terminé sur branche** : code `site/arrondissement-compare.mjs` + commandes intégrées à `site/index.html` et `site/app.mjs` + `tests/arrondissement-compare.test.mjs`. Comparaison de **deux RP choisis parmi 2006/2011/2016/2023**, colorimétrie en **points de pourcentage** ou **nombre de logements**, popups sourcés et classement vingt arrondissements. Base : 20 agrégats des **IRIS de leur géographie propre**, dessinés sur contours des **arrondissements IGN 2025** ; jamais une vacance au bâtiment.
- **Recette vraie donnée + vrai navigateur** : sur machine Linux autorisée, Chromium 1440×900 et 390×844 simulé, source `https://vacant.kiwinokoto.fr/data/arrond-history.geojson` copiée uniquement en dossier temporaire local. 20 arrondissements, 5 classes, 20 rangs, dates, changement points↔nombre, périodes invalides refusées, switch vers IRIS 2023, zéro exception JS et overflow. Variation Paris 2006→2023 : **+16 408 logements** et **+0,7 point**, 13 arrondissements avec taux en hausse, 7 en baisse. Correction de précision : pour le total Paris on reprend les **totaux officiels** Insee (2011→2023 **+40 377**, car somme IRIS fractionnaire pouvait différer de 1).
- **Tests JavaScript** : V-03 a cinq nouveaux tests, première relance après correctifs **89/89 JS et 93/93 Python** (rejouer sur le HEAD final), plus tests du DOM et validation des années / des sources. Pas de données confidentielles dans Git.
- **Documentation précise** : [V-03 protocole, géographies, classes et limites](vacance-arrond-comparison-20261017.md), puis [ROADMAP.md](../ROADMAP.md) et `docs/handoff.md`. La **PR #28** de géométries IGN reste un chantier parallèle en brouillon.
- **GitHub/ordre des PR :** #29 = série 1968–2023 + distribution IRIS + backlog + cette passation, base `main`; branche empilée V-03 = `dev/vacancy-arrondissement-compare-20261017`, **PR #30 cible `dev/vacancy-timeline-and-roadmap-20261017`**, puis fusionner **#29 avant #30** lors de la promotion, sans écraser les travaux historiques #28. Vérifier les SHA HEAD et le statut des PR avant toute action.
- **Production** : toujours l'ancienne release Git `8711f3071abd41b169c92dfe0daaa79708be9acf`, HTTPS 200, aucune nouvelle fonctionnalité V-01/V-02/V-03 déployée ; conservée sans redémarrage lors du travail. **Ne pas confondre une recette locale avec la publication**.
- **À la prochaine reprise**, vérifier les PR et poursuivre **V-04 LOVAC agrégé**. Côté B : apparier spatialement les IDs différents du référentiel 2011/2018 et vérifier la source du millésime 2008 avant de représenter Paris « qui apparaît ». Les deux rails demeurent indépendants scientifiquement.

---

# VACANT — PASSATION DE REPRISE (17 octobre 2026)

**Document de reprise prioritaire**, prévu pour un **nouveau chat** ; GitHub constitue la source de vérité. Ce document est mis à jour sur la **branche de PR #29**. Il fait foi pour les prochaines interventions sous réserve d'un contrôle frais de `main`, des PR et de la production.

## 1. Vision validée par l'utilisateur

**VACANT sert en priorité à comprendre et cartographier la vacance résidentielle à Paris, avec la meilleure finesse géographique et temporelle scientifiquement défendable.** Deux rails :
- **V — Vacance (environ 70 % du temps)** : mesurer les logements vacants en nombre absolu et en % du parc, comparer Paris entier / 20 arrondissements / IRIS quand les géographies sont valides, et identifier les ruptures de sources.
- **B — Bâti historique (environ 30 %)** : reconstruire *de façon documentée* l'apparition et l'évolution visuelle de Paris en couleur, à partir d'états géométriques véritables. Le beau rendu reste bienvenu mais ne doit jamais faire croire que l'on connaît la vacance d'un appartement, ni fabriquer des dates de construction.
- L'utilisateur préfère une **approche autonome, « go, continue »** et des mises à jour utiles, mais **veut une passation suffisamment tôt avant la limite de chat**. Développement principalement **desktop** ; responsivité raisonnable, pas de recette obligatoire sur téléphone physique.
- **Pas de publication de LOVAC individuel, de liste d'adresses vacantes ou de croisement de taux IRIS avec une emprise de bâtiment.**

## 2. Références et PR

- GitHub : [Kiwinokoto/vacant](https://github.com/Kiwinokoto/vacant), public. **Lire `AGENTS.md`, `README.md`, `ROADMAP.md`, `docs/handoff.md`, `docs/sources.md`, `docs/architecture.md` avant tout changement.**
- **`main` observé au début de cette passe** : `22f0ad1a07f0c8ea5bc6931c6369df410fac65bc`. Relire son HEAD avant les modifications.
- **PR #28 : [audit IGN historique](https://github.com/Kiwinokoto/vacant/pull/28)**, branche `dev/ign-bdtopo-historic-audit-20261017`, **brouillon non fusionné**, code et tests de recherche du rail B.
- **PR #29 : [vacance 1968–2023, IRIS et backlog](https://github.com/Kiwinokoto/vacant/pull/29)**, branche `dev/vacancy-timeline-and-roadmap-20261017`, **brouillon non fusionné**. Elle crée le backlog `ROADMAP.md`, la page `site/evolution.html`, les 9 jalons officiels Paris 1968–2023, et améliore la lecture de la carte IRIS 2023. Dernier checkpoint code avant ce document : `023607ae7f037138d0ae30c432055b6e5f7db01c`. Les deux PR sont **indépendantes, basées sur main**.
- **Priorité technique suivante** : V-03, comparateur de **deux millésimes** des 20 arrondissements (2006, 2011, 2016, 2023), en nombre et en taux, avec différences de pourcentage en **points**, non en %. Développer en petite branche **empilée sur #29**, avec PR dont la base est la branche #29, ou fusionner #29 au préalable seulement après revue. Pas de push direct à main ; ne pas déployer automatiquement.
- **Ensuite V-04** : LOVAC **agrégé public** 2020–2026, seulement à la maille **commune** et pour le **parc privé**, sans raccordement à la série Insee. Ruptures méthode LOVAC 2024 (GMBI) et 2025. Puis V-05 : anciennes limites IRIS exactes / licences historiques.
- En parallèle **B-02 puis B-03** : appariements spatiaux n:m des IDs IGN 2011/2018 différents, qualifier l'édition 2008, vérifier mars/septembre 2018. Ne pas présenter des révisions du référentiel comme des constructions/démolitions.

## 3. Production et confidentialité

- Production : [https://vacant.kiwinokoto.fr](https://vacant.kiwinokoto.fr).
- **Release actuellement déployée** au début de cette passe : commit `8711f3071abd41b169c92dfe0daaa79708be9acf` ; code GitHub main documentaire plus récent. Container Docker `vacant-vacant-web-1` sur **VPS personnel**, montée `/srv/vacant/releases/8711f3071abd41b169c92dfe0daaa79708be9acf/site`, contrôlé `running`, **0 restart**, HTTPS 200. **Laisser cette version en place**, tant que les PR ne sont pas auditées et autorisées pour release.
- Rollback : release `/srv/vacant/releases/1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0/site`, procédure dans [PV déploiement Apur ODbL](apur-odbl-deployment-20261017.md). Garder les sources privées / releases existantes intactes.
- Données publiques Apur sous ODbL : 456 GeoJSON de 500 m, 128 089 emprises uniques, **ZIP téléchargeable + manifeste SHA**, [notice](https://vacant.kiwinokoto.fr/data/apur-grid/NOTICE.md) ; source attribuée © Apur. **Datation d'emprise contemporaine ≠ photographie historique**, et hauteur médiane en **mètres ≠ nombre d'étages**.
- Les fichiers **IGN historiques** SHP/7z et extraits sont conservés uniquement dans `/srv/vacant/data/raw/ign/bdtopo-historical-20261017/` et `/srv/vacant/data/processed/ign/bdtopo-historic-audit-20261017/` ; pas de copie dans Git, pas de publication sans provenance/licences contrôlées.
- Les originaux Insee et IGN sont conservés sous `/srv/vacant/data/raw`; le site sert seulement des agrégats audités. Données LOVAC individuelles interdites.

## 4. Sources/statistiques déjà validées

- **IRIS 2023** : 992 quartiers (Insee RP2023 / IGN géographie 2025), données préparées sous licence ouverte et inspectées GEOS. **2023 Paris : 139 075 logements vacants sur 1 402 024, soit 9,9 %**. La colorimétrie IRIS est désormais calculée depuis le ratio **non arrondi**, pas depuis `vacancy_percent` arrondi : 77 quartiers <5 %, 241 à 5–<8 %, 362 à 8–<12 %, 237 à 12–<20 %, 12 ≥20 %, 63 masqués pour parc <50 logements. Donc **852/929 IRIS à taux affichable ≥5 %**, 249/929 ≥12 %. Le taux national Paris est **pondéré par le nombre de logements**, jamais moyenne des classes.
- **Chronologie Paris entier 1968–2023** dans la **PR #29** : Insee LOG T1, années **1968, 1975, 1982, 1990, 1999, 2007, 2012, 2017, 2023**, histogramme discret (taux et nombre) et tableau. Rupture **dénombrements anciens jusqu'à 1999 / recensements rénovés à partir de 2007**, aucun faux point annuel. [Méthode et données](vacance-evolution-1968-2023.md).
- **Carte arrondissements déjà publiée** : **4 recensements distincts** 2006 / 2011 / 2016 / 2023, dérivé `site/data/arrond-history.geojson` (servi en production), source privée sous `/srv/vacant/data/processed/arrond-history/`. Les données ont été agrégées depuis les IRIS **de leur année**, puis affichées sur les contours IGN 2025 des **20 arrondissements**. **2007/2012/2017 de la courbe Paris entier ≠ 2006/2011/2016 de la carte**, ne pas permuter les séries.
- Modèles JS : `site/timeline.mjs` (4 jalons cartes), `site/arrondissement-history.mjs` (`validateArrondissementSeries`, `statForYear`, `buildArrondissementPopup`), `site/app.mjs` (Leaflet), `site/iris-colors.mjs` (taux exact), `site/iris-insights.mjs`. Toute nouvelle comparaison doit être calculée **à partir de `feature.properties.series[year].vacant_count/housing_count`** des 20 arrondissements, avec validation du dataset, jamais des seules couleurs ni d'un IRIS actuel.
- **IGN bâtiment, PR #28** : archives Paris D075 2008 (25 738 objets), 2011 (117 430), 2018 (116 772) retrouvées via miroir `data.cquest.org`, SHA vérifiés. Édition 2008 **non comparable directement**. 2011↔2018 : 113 634 IDs communs, 112 567 géométries exactes inchangées, 1 067 modifiées (IoU médian 0,908579), **3 796** IDs seulement 2011, **3 138** seulement 2018, **pas** un décompte de destructions/constructions. Voir `docs/ign-bdtopo-historic-20261017.md` sur PR #28. Licence d'archives à confirmer avant redistribution.

## 5. Qualité, essais déjà réalisés et procédure

- PR #29 avant ce document : **84/84 tests JS et 93/93 Python**, `git diff --check` propre. Chromium vrai navigateur en **local** sur 1440×900 desktop et 390×844 mobile simulé : graphique 9 barres, bascule taux/nombre, tableau, IRIS 2023 réel, résumé 852/929 et 249/929, 9,9 %, zéro erreur JS/overflow ; l'encadré IRIS se masque après désactivation. **Pas encore déployé**.
- PR #28, dernière passe : **79/79 tests JS et 102/102 Python**, comparaison complète sur VPS, SHA/GEOS valides, pas de donnée GIS publiée.
- Pour V-03 : tests synthétiques des variations *en points* et absolus, incompatibilité des années, absence des données, inversion dates, total pondéré, comparateur exclusif aux **20 arrondissements**, popup non injectable ; contrôle Chromium avec **vrai dérivé 20 arrondissements** et cache privé. Tests `node --test tests/*.test.mjs` et `/srv/vacant/venv/bin/python -m unittest discover -s tests -p 'test_*.py'` depuis un clone éphémère de la branche.
- Respecter **AgentCTL** pour les ressources mutables `repo:Kiwinokoto/vacant` et `state:vacant` avant modifications, puis **release et finish**. Éviter les multiples appels RDC ; GitHub connector en priorité. Tester en vrai navigateur sur une machine Linux autorisée si l'UI change. Ne jamais écraser une sortie audit privée ou une release.
- Les **PR #28 et #29** sont encore en brouillon ; recommencer par vérifier leurs HEAD/statuts/CI et si d'autres agents ont modifié `main`. Source de vérité : GitHub, ne pas s'appuyer sur de vieux clones du VPS.

## 6. Ce qui reste à faire à la prochaine reprise

1. Vérifier **GitHub HEAD + PR #28/#29** et la présence d'une éventuelle **PR #30 V-03** (créée), lire ce document et le dernier `docs/handoff.md`.
2. Relire la **PR #30 V-03** déjà recettée (20 arrondissements, taux/counts, Chromium), la fusionner seulement après la **PR #29** et ses propres contrôles, sans déploiement implicite.
3. Préparer **V-04 LOVAC agrégé** en contrôlant le fichier public, le dictionnaire des colonnes et les ruptures de définition avant tout graphique.
4. Sur B, poursuivre l'appariement spatial n:m et l'étude des géographies fiables ; penser à une animation historique **esthétique mais documentée**.
5. Lorsque la PR vacance est prête et le périmètre validé, préparer la release depuis le SHA Git exact, préflight Nginx/Traefik et données brutes privées exclues, puis **demander/obtenir l'autorisation appropriée si le déploiement n'est pas explicitement autorisé**.

**Phrase de reprise utilisable dans un nouveau chat** : « Reprends VACANT depuis `docs/PASSATION-2026-10-17.md` dans GitHub, vérifie les PR #28/#29 et les éventuelles PR empilées, puis continue en priorité la comparaison temporelle de vacance par arrondissement. Garde la reconstruction IGN en deuxième rail ; aucune inférence au bâtiment, GitHub source de vérité, pas de déploiement sans recette. »
