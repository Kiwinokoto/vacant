# VACANT — passation actualisée du 17 octobre 2026 (LOVAC)

Document de reprise pour un nouveau chat. Lire aussi `docs/PASSATION-2026-10-17.md`, `ROADMAP.md`, `AGENTS.md` et `README.md`. **GitHub est source de vérité.**

**Vision :** vacance résidentielle Paris en priorité (~70 %), reconstruction documentée du bâti en parallèle (~30 %). Jamais de taux de vacance au bâtiment, jamais d'adresse ou propriétaire LOVAC. Ordinateur prioritaire.

**PR brouillon :** #29 vacance Insee 1968–2023 + IRIS ; #30 comparateur des 20 arrondissements, empilée sur #29 ; **#31 LOVAC public 2020–2026**, empilée sur #30 ; #28 recherche IGN 2008/2011/2018, indépendante. **Ordre de fusion : #29 → #30 → #31** après revue, #28 à part. Aucun déploiement de ces PR.

**V-04 réalisé sur branche #31 :** trois CSV publics Cerema juin 2026 figés et validés SHA-256 sur VPS (`/srv/vacant/data/raw/lovac/open-aggregate-20260625/`), vingt codes 75101–75120 sans secrétisation, sommes exactement identiques au département 75. `scripts/audit_lovac_open_paris.py` (6 tests Python), `site/data/lovac-paris-open-2026.json` (agrégats publics seulement, SHA-256 `383978506b23b21d75a22b84e6a4499e26a41b347e6e1108e833e86eb98fb326`), `site/lovac.html` et contrat JS (2 tests). Recette Chromium desktop 1440×900/mobile simulé 390×844, 7 barres, 20 lignes, zéro erreur.
