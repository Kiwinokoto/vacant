# VACANT — procès-verbal de mise en production Apur ODbL

**17 octobre 2026 — déploiement exécuté, contrôlé et conservé.**

## Versions GitHub et VPS

- Référentiel canonique : [Kiwinokoto/vacant](https://github.com/Kiwinokoto/vacant).
- Les PR **#23, #24, #25 et #26** ont été fusionnées sur `main` par de vrais **merge commits** dans cet ordre, sans squash. Les six commits sources Apur #17–#22 sont atteignables dans l'ascendance de la PR #23.
- Commit de code **effectivement déployé** : `8711f3071abd41b169c92dfe0daaa79708be9acf`.
- Nouvelle release statique immuable : `/srv/vacant/releases/8711f3071abd41b169c92dfe0daaa79708be9acf/site`.
- Configuration Nginx de la release : `/srv/vacant/work-release-8711f307/deploy/nginx.conf`, servie dans `vacant-vacant-web-1` via Docker Compose `-p vacant`.
- Release précédente **conservée pour rollback** : `/srv/vacant/releases/1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0/site`, avec l'ancienne config `/srv/vacant/work-release-pr13/deploy/compose.yml`.

## Licence et données publiques

Le jeu d'origine `EMPRISE_BATIE_PARIS`, © **Apur**, est diffusé sous **ODbL 1.0**. VACANT distribue sa **base adaptée** sous la même licence, avec documentation de provenance, modifications et exclusions. Source d'extraction : **16/10/2026**, **millésime métier exact toujours non confirmé**.

- [Manifeste adapté](https://vacant.kiwinokoto.fr/data/apur-grid/manifest.json) : SHA-256 `2b0683c33e236b906163c73786133f300182ccc4f00c70485bbcf1e84eb75711`.
- [Archive intégrale ODbL](https://vacant.kiwinokoto.fr/data/apur-grid/apur-paris-grid-500m-2026-10-16-odbl.zip) : **28 106 318 octets**, SHA-256 `9bef60651f2b0f20158392157ffe2e0a6757257a57757532348384e4521e9e24`, contenant 456 GeoJSON, manifeste et notice.
- [Notice et licence](https://vacant.kiwinokoto.fr/data/apur-grid/NOTICE.md) : © Apur, lien ODbL, exclusions, géographie, datation et procédure de reconstruction.
- Chaque cellule GeoJSON est publiquement téléchargeable, avec SHA-256 individuel vérifiable par le manifeste. **459 fichiers** dans `site/data/apur-grid/` ; aucun GeoJSON Apur dans Git.

**Limites :** 128 206 emprises source ; **104 géométries GEOS invalides** et **13 identifiants métier manquants** exclus ; **128 089 emprises uniques**, 456 cellules de 500 m et 138 381 placements à dédoublonner. Les périodes décrivent **des emprises bâties actuelles**, sans reconstruction historique certaine. Hauteurs médianes `h_med` **en mètres**, pas en étages. **Aucune vacance au bâtiment ni au logement** n'est fournie ou déduite de la base Apur.

## Tests réalisés le 17/10/2026

- Nouvelle copie GitHub de `main` au SHA de release, **75/75 tests JavaScript et 93/93 tests Python**.
- `scripts/recipe_nginx_gzip_loopback.py` réussi sur le VPS, et tests d'en-têtes dans un conteneur Nginx **isolé lié à 127.0.0.1** servant exactement la nouvelle release : `Content-Encoding: gzip`, `Vary: Accept-Encoding`, décompression SHA conforme, ZIP intégral SHA conforme, HTTP 404 sur chemin brut privé.
- Préparation via **`scripts/stage_reviewed_release.py --publish-apur`** avec trois empreintes figées. Release préparée hors du répertoire servi, fichiers suivis Git uniquement + deux agrégats publics validés + paquet adapté Apur explicitement autorisé.
- Après bascule Docker Compose : `https://vacant.kiwinokoto.fr/` = HTTPS 200 ; `manifest.json` et ZIP = 200 avec SHA-256 exacts ; notice et cellule de test = 200 ; route source brute = 404. Conteneur **running**, zéro redémarrage.
- **Chromium sur le site HTTPS réel**, desktop 1280×800 et largeur mobile simulée 390×844 : 2 284 emprises uniques affichées dans le secteur de recette, 12 classes périodes et 6 classes hauteurs, **aucune requête supplémentaire** pendant la recoloration, zéro exception JavaScript et zéro débordement horizontal. Passage Apur → IRIS 2023 validé ; le mode Apur revient à `off`, l'IRIS s'active.
- Aucune publication de géométrie Apur brute, de LOVAC individuel ou de prévisualisation privée. Les **150 emprises laboratoire** restent indisponibles publiquement.
- **Pas d'essai sur téléphone physique : choix explicite de l'utilisateur ; desktop prioritaire.**

## Retour arrière

En cas d'incident, **acquérir les verrous AgentCTL** `repo:Kiwinokoto/vacant`, `deploy:vps-personal/vacant`, `service:vacant`, `host:vps-personal/docker` puis, après validation que les chemins de référence sont toujours corrects :

```sh
VACANT_WEBROOT=/srv/vacant/releases/1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0/site \
  docker compose -f /srv/vacant/work-release-pr13/deploy/compose.yml \
  -p vacant up -d --no-deps vacant-web
```

Puis revérifier HTTPS, montages, réponse 200, absence de redémarrage répété. **Ne pas supprimer les archives ODbL publiques après diffusion**, car les utilisateurs peuvent avoir le droit de les réutiliser ; si retrait nécessaire, documenter les raisons et assurer le respect des licences.

## Suite scientifique

1. Continuer la recherche des véritables jalons géométriques antérieurs (2006, 2011, 2018), **sans les déduire** des périodes de construction Apur.
2. Vérifier la réponse officielle `data@apur.org` au sujet de la datation scientifique précise et améliorer les métadonnées si elle arrive ; l'ODbL ne nécessite pas d'attendre cette réponse pour l'exploitation des emprises.
3. Améliorer la navigation desktop (sélection spatiale et chargement par zones, cache, éventuelle pagination) ; mobile secondaire.
4. Conserver un pipeline reproductible et les distinctions entre **états du bâti**, **statistiques de vacance** et **reconstructions historiques**.

L'utilisation de la licence libre et la publication du dérivé ne constituent pas un avis juridique exhaustif sur tous les droits de contenus tiers.
