# VACANT — passation actualisée du 17 octobre 2026 (LOVAC)

## Nouveau jalon BDCOM — PR #35

Étude du potentiel non résidentiel à partir de **données ouvertes BDCOM réellement interrogées** (17/10/2026) : **83 154** locaux de rez-de-chaussée Paris, `AA101`=**7 495 vacants hors travaux** ; `AA102`=**1 565 en travaux**, `type=V`=**9 060**, tandis que la note Apur indique **9 059**. L'écart **+1** reste à expliquer, aucune correction manuelle. Vingt arrondissements agrégés, aucune adresse, licence ODbL. Source et méthode `docs/bdcom-open-audit-20261017.md`.

**Bureaux** : Paris intra-muros ≈ **1,5 million de m² d'offre immédiate** fin juin 2026 (Colliers et Cushman & Wakefield). L'observation Colliers de mars 2026 (795 000 m²) semble incompatible avec celle de juin (1,542 million), ne pas relier ces points comme évolution observée avant clarification. Aucune conversion automatique en nombre de logements.

PR #35 brouillon empilée sur #34, chaîne **#29 → #30 → #31 → #32 → #33 → #34 → #35** ; IGN historique #28 autonome. Aucune modification de main ou prod. `docs/handoff.md` conserve la passation immédiate.


## Nouveau périmètre transverse (PR #34)

**Décision utilisateur :** comparer séparément les logements habitables et non habitables, mais conserver **bureaux vacants, commerces vacants et logements dégradés** dans la recherche sur les espaces sous-utilisés, afin d'étudier un éventuel accueil temporaire ou pérenne des personnes sans logement. Un local sans eau, lumière ni équipements peut être un **potentiel à étudier**, mais jamais un logement immédiatement habitable ou une solution de nuit sûre sans diagnostic de sécurité, hygiène, accès, évacuation et droit d'usage. Inconnu par défaut : les bases de vacance disponibles ne permettent pas de distinguer les logements effectivement prêts à habiter.

Première mesure non résidentielle : **Apur BDCOM 2023, 9 059 locaux de RDC vacants sur 83 154 recensés**, 10,9 %, champ distinct des logements RP/LOVAC et des bureaux en étage. **Ne pas additionner les trois mesures.** Source et protocole dans `docs/potentialite-locaux-20261017.md`, nouvelle page `site/potentiel.html`. Chercher ensuite des données de vacance de bureaux Paris intra-muros avec surfaces et dates, puis diagnostiquer la transformabilité. Pas de fiches individuelles.

PR #34 empilée sur #33 ; ordre de revue #29 → #30 → #31 → #32 → #33 → #34, #28 historique indépendante. Production toujours inchangée.


## Dernier état — PR #33, vacance de longue durée par arrondissement
**PR [#33](https://github.com/Kiwinokoto/vacant/pull/33)** en brouillon, branche `dev/lovac-long-duration-analysis-20261017`, empilée sur **#32**. Commit fonctionnel testé `717f5bdc55f5dc7f72b02fb65cf95de28fa31a0d`. Nouvelle carte/classement 20 arrondissements pour la proportion longue parmi les seuls logements privés fiscalement **déjà vacants**, ou les deux effectifs séparés. 2026 observé au **01/01/2025** : Paris **26 264 / 105 785 = 24,8 %**, 8e **41,2 %** parmi les vacants, 18e **2 449** vacants longue durée. **Jamais un taux sur tout le parc privé**. Ratio 2023 interdit (dates incompatibles). Ruptures GMBI 2024 et 2025. Aucun fichier individuel, aucune adresse.

**Recette sur code `717f5bd` : 98/98 tests JavaScript, 99/99 Python dans le venv ; Chromium réel avec contours IGN 2025 réels, 20 polygones, 20 lignes, 20 rangs, 5 classes, millésime 2023 refusé pour la part mais effectifs consultables, desktop 1440×900 et mobile simulé 390×844 sans débordement ; zéro erreur JavaScript applicative.** Correctif mobile du sélecteur vérifié : 432 → 390 px. Faible anomalie résiduelle : demande navigateur de `favicon.ico` donne 404 (hors fonctionnalité). Production et `main` inchangés.

**Chaîne de fusion à reviewer : #29 → #30 → #31 → #32 → #33**, #28 indépendante. Aucun déploiement. Prochaine étape : revue de la chaîne et choix du seuil de lecture de la vacance longue, puis éventuellement enrichissements statistiques IRIS à géographie datée, sans fausses localisations. Ne pas inférer une baisse réelle d'occupation de sa variation de mesure fiscale.

Document de reprise pour un nouveau chat. Lire aussi `docs/PASSATION-2026-10-17.md`, `ROADMAP.md`, `AGENTS.md` et `README.md`. **GitHub est source de vérité.**

**Vision :** vacance résidentielle Paris en priorité (~70 %), reconstruction documentée du bâti en parallèle (~30 %). Jamais de taux de vacance au bâtiment, jamais d'adresse ou propriétaire LOVAC. Ordinateur prioritaire.

**PR brouillon :** #29 vacance Insee 1968–2023 + IRIS ; #30 comparateur des 20 arrondissements, empilée sur #29 ; **#31 LOVAC public 2020–2026**, empilée sur #30 ; #28 recherche IGN 2008/2011/2018, indépendante. **Ordre de fusion : #29 → #30 → #31** après revue, #28 à part. Aucun déploiement de ces PR.

**V-04 réalisé sur branche #31 :** trois CSV publics Cerema juin 2026 figés et validés SHA-256 sur VPS (`/srv/vacant/data/raw/lovac/open-aggregate-20260625/`), vingt codes 75101–75120 sans secrétisation, sommes exactement identiques au département 75. `scripts/audit_lovac_open_paris.py` (6 tests Python), `site/data/lovac-paris-open-2026.json` (agrégats publics seulement, SHA-256 `383978506b23b21d75a22b84e6a4499e26a41b347e6e1108e833e86eb98fb326`), `site/lovac.html` et contrat JS (2 tests). Recette Chromium desktop 1440×900/mobile simulé 390×844, 7 barres, 20 lignes, zéro erreur.

**Chiffres et ruptures :** Insee RP2023 Paris = 139 075 logements vacants sur 1 402 024 (9,9 % du parc total) ; LOVAC 2026 = 105 785 logements du parc privé fiscal, dont 26 264 depuis plus de deux ans, **observation au 01/01/2025**. Le millésime 2023 « longue durée » observe 01/01/2022, « tous vacants » 01/01/2023. Pas de dénominateur 2026 aligné ; **aucun taux LOVAC 2026 calculable de manière justifiée**. Rupture méthodologique GMBI dès 2024 puis changement de traitement en 2025 : ne pas attribuer une baisse apparente à des remises en occupation. Source et dates : `docs/lovac-open-audit-20261017.md`.

**Production :** `https://vacant.kiwinokoto.fr` reste sur la release `8711f3071abd41b169c92dfe0daaa79708be9acf` ; aucune des PR #28–#31 n'est déployée. Ancienne release de rollback conservée. AgentCTL (`repo:Kiwinokoto/vacant`, `state:vacant`) avant modifications. Source de vérité GitHub ; ne jamais fusionner directement main ni exposer les originaux privés.

**Prochaine priorité :** revue et préparation de la **cartographie descriptive LOVAC à la maille des 20 arrondissements**, avec année de production *et* date de référence visibles, légendes adaptées et comparaisons méthodologiquement défendables seulement. En parallèle (rail B), continuer l'appariement géométrique IGN 2011–2018 et qualifier l'édition 2008 (non comparable directement). Vérifier d'abord les têtes des PR #28–#31, puis finir tests et recette avant toute fusion ou déploiement.

## Travail de reprise — carte descriptive LOVAC
Nouvelle branche empilée sur #31 : `dev/lovac-arrond-map-20261017`. Une carte de comptages absolus par arrondissement utilise le dérivé public LOVAC et les contours des arrondissements IGN 2025 déjà servis. Choix du millésime et de la mesure synchronisé avec le tableau et le graphique, légendes en classes absolues fixes selon la mesure, infobulles avec observation et source. Aucun taux ni projection sur un bâtiment. Les ruptures 2024/2025 restent visibles. La carte échoue proprement si les contours ne sont pas disponibles. Tests du contrat cartographique ajoutés. Faire la recette desktop avec le vrai GeoJSON et contrôler le HEAD/tests avant toute fusion. Ordre de dépendances : #29 → #30 → #31 → PR carte.

**Validation complémentaire PR #32 :** 94/94 tests JavaScript, 99/99 tests Python dans `/srv/vacant/venv` ; échec initial du Python système uniquement faute de Shapely. Contrat cartographique contrôlé contre le véritable `/data/arrond-history.geojson` HTTPS public : 20/20 contours IGN 2025 reconnus. Aucun navigateur Chromium accessible sur le VPS vérifié : recette UI desktop/mobile réelle à effectuer avant fusion. Production inchangée.

## Étape suivante — analyse de la vacance longue (PR #33)
Branche empilée sur #32 : `dev/lovac-long-duration-analysis-20261017`. Carte des 20 arrondissements : **part des vacants privés depuis >2 ans parmi l'ensemble des vacants privés**, nombre de longue durée, nombre total ; classement, dates, légendes, info-bulles et tests. Attention : ce ratio ne représente **pas** un taux rapporté au parc privé. Le 2023 est interdit pour ce calcul (variables datées du 01/01/2022 et du 01/01/2023). Paris 2026 : 26 264 / 105 785 = 24,8 %, 8e maximum en proportion 41,2 %, 18e maximum en effectif 2 449. Voir `docs/lovac-long-duration-20261017.md` et ses tests. Corrections incidentes : séquences littérales « \\n » dans CSS et passation de #32. Ne pas promouvoir sans recette navigateur complète. Chaîne désormais #29 → #30 → #31 → #32 → #33, #28 parallèle. Production inchangée.

### Recette de la PR #34 et état GitHub (17/10/2026)
Code `5d4cde688476c207fb1cd3a5a2aeb118a4e0e60e` : **102/102 tests JavaScript**, **99/99 tests Python** depuis le venv du VPS, `git diff --check` sans anomalie, clone éphémère sans changements locaux. **Chromium réel** (serveur statique local) : 3 indicateurs indépendants, 4 scénarios qualitatifs, navigation depuis index / évolution / LOVAC validée ; desktop 1440×900 sans débordement, mobile simulé 390×844 sans débordement (tableau défilant à l'intérieur), aucune erreur JavaScript applicative de la nouvelle page. Aucune source brute confidentielle. PR #34 reste en brouillon ; **aucune fusion ni déploiement**. Avant reprise : vérifier les HEAD et les locks, puis auditer la donnée BDCOM et les sources de vacance de bureaux Paris.

## Recette PR #35 (17 octobre 2026)
**Code `041c3bd43764553b074dad78f03600185e313f7a` : 105/105 tests JavaScript et 99/99 Python (venv VPS).** `node --check` et `git diff --check` valides. Chromium sur serveur temporaire : bureau 1440×900 (**4 familles, 20 lignes BDCOM, zéro débordement**), modalité « vacants hors travaux » classant le 18e en tête, modalité « travaux » classant le 8e en tête ; mobile émulé 390×844 sans débordement (tableau défilant dans son conteneur). Correction du lien vers la note n°236 testée. **Aucun fichier de points, adresse ou enseigne dans GitHub.** PR en brouillon, ni fusion ni déploiement. Écart de la note 9 059 vs source 9 060 non résolu.
