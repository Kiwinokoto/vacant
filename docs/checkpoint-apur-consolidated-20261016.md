# VACANT — checkpoint de consolidation Apur

**16 octobre 2026 — branche de revue `dev/apur-consolidated-20261016`.** Cette note remplace les passages « priorité suivante » devenus obsolètes dans les anciens checkpoints. **Pas de fusion vers `main` ni de déploiement** pendant cette passe.

## Git et périmètre

- **Source de vérité :** `Kiwinokoto/vacant`, base `main=72a9d06377541b7b266e0d8153e89a7ae19afb95`. Production maintenue sur `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0` (ancien code volontairement conservé).
- Les PR **#17, #18, #19, #20, #21 et #22** ont été assemblées en un **commit à sept parents** : `main` + la tête exacte de chacune des six branches. Ces commits restent dans l'ascendance Git, non réécrits.
- **Seul conflit réel :** `docs/handoff.md`, édité dans les six PR. Aucun conflit dans les scripts, tests, pages ou contrats. L'ancien historique du document est conservé une seule fois et cette note est la passation canonique.
- Branches/PR originales laissées intactes et en brouillon ; ne pas fermer, fusionner ou supprimer à ce stade. Nouvelle PR de consolidation à revoir séparément. Aucun workflow Actions détecté, ni règles de protection GitHub déclarées lors de cette passe : cela **n'équivaut pas** à une approbation de publication.

## Contenu regroupé — responsabilités distinctes

| Source | Fichiers principaux | Objet |
| --- | --- | --- |
| PR #17 | `scripts/sample_apur_geometry.py`, `docs/apur-geometry-sample-20261016.md` | Prélèvement géométrique borné, inspection des outliers |
| PR #18 | `experiments/apur-periods/`, `docs/apur-offline-browser-recipe-20261016.md` | Prototype périodes et recette locale SHA-256 sur 150 objets |
| PR #19 | `scripts/audit_apur_frozen_export.py`, `docs/apur-frozen-export-20261016.md` | Archive source immuable et audit GEOS exhaustif |
| PR #20 | `scripts/build_apur_period_candidate.py`, `docs/apur-private-candidate-20261016.md` | GeoJSON de 150 emprises, isolé et contrôlé |
| PR #21 | `site/apur-lab.mjs`, `site/apur-lab-contract.mjs` | Périodes et hauteurs **exclusivement sur localhost avec `?apur_lab=1`**, fixture absente du dépôt et de la production |
| PR #22 | `scripts/build_apur_private_grid.py`, `experiments/apur-grid/` | Grille Paris 500 m, manifeste, lecteur local sélectif et mobile |

Les PR #21 et #22 sont **complémentaires, pas encore raccordées** : l'interface VACANT du laboratoire reste basée sur **150 emprises** ; la grille Paris complète est un **explorateur autonome**. Ne pas prétendre que le site utilise déjà le lecteur multi-cellules.

## Résultats scientifiques et provenance

- Source : Apur `EMPRISE_BATIE_PARIS`, **ODbL 1.0**, archive SHP privée de 31 981 417 octets, SHA-256 `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`. Dossier privé : `/srv/vacant/data/raw/apur/frozen-2026-10-16/`. Original jamais versionné dans GitHub.
- Le **millésime scientifique est toujours non attesté** : la métadonnée Géocatalogue 2025-02 est contradictoire avec des dates d'édition d'objets jusqu'en septembre 2026. Demande déjà adressée à `data@apur.org` le 16/10 ; surveillance quotidienne Gmail existante, ne pas envoyer de doublon.
- Audit exhaustif des **128 206 emprises** : **104 géométries GEOS invalides** et **13 identifiants métier absents** exclus, donc **128 089 emprises uniques exploitables**. Les 104 géométries ne sont pas réparées silencieusement.
- Dérivé de 150 emprises : `/srv/vacant/data/processed/apur/experiment-heights-20261016/apur-period-height-local.geojson`, SHA-256 `ba14be71c3cb58afcae935bcdc3f775f63ad043d12ecb20f42bdf2da759afaf9` ; destiné exclusivement à la recette localhost.
- Grille privée 500 m : `/srv/vacant/data/processed/apur/paris-grid-experiments/cells-500m-original/`, **456 cellules, 91 515 440 octets**, **138 381 occurrences pour 128 089 objets distincts**, manifeste SHA-256 `bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c`. Les emprises qui traversent des cellules doivent être dédoublonnées par `OBJECTID`.
- Les hauteurs Apur `h_med` sont en **mètres** ; les `H_ET_MAX` Paris Data sont des **étages**. `c_perconst` décrit une période **attribuée à des emprises actuelles**, pas une géographie historique attestée.

**Interdictions :** jamais de vacance attribuée au bâtiment, ni de rapprochement automatique Apur/LOVAC/Insee/Paris Data, ni de géométries IGN historiques non autorisées. Les sources et dérivés Apur ne doivent pas entrer dans `site/`, GitHub, une release ou une URL publique avant qualification des droits.

## Validation et réserves

- Assemblage testé en lecture sur clone isolé **66/66 JavaScript et 81/81 Python**. Le test local est à rejouer depuis la nouvelle branche de consolidation après publication du checkpoint ; le rapport final doit noter son résultat.
- Recettes Chromium précédentes individuelles : laboratoire de 150 objets sur desktop/mobile, et grille 456 cellules avec chargement **uniquement des cellules visibles**, SHA, refus 503, dédoublonnage. Latences mesurées en **local**, non représentatives d'une connexion 4G ni d'un téléphone physique.
- Obligations ODbL de redistribution de la base adaptée utilisée publiquement à documenter avant publication ; transparence sur les transformations, les exclusions, le millésime et l'accès à la base dérivée. Pas de publication automatique.

## Prochaines actions

1. Valider la **PR consolidée**, revue du différentiel et recette navigateur sur son commit exact. Conserver les six PR sources tant que leur remplacement n'est pas approuvé.
2. Préparer une **PR ultérieure** reliant le lecteur 500 m à l'interface VACANT, en mode laboratoire local désactivé par défaut, sans perdre les couches IRIS/arrondissements/volumes ; tester 404/503, SHA, mémoire, navigation et cohérence mobile.
3. Préparer séparément le contrat ODbL, la politique de distribution de la base adaptée et le plan de versionnement. La réponse Apur n'est pas nécessaire pour continuer les essais privés.
4. Envisager seulement ensuite une activation publique avec contrôle explicite des risques et accord de déploiement.
