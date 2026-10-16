# VACANT — candidat privé Apur par période (16 octobre 2026)

**État : validation SIG d'un prototype privé ; aucune couche Apur publiée.**

## Reprise et source de vérité

- GitHub canonique : `Kiwinokoto/vacant` ; base au lancement : `main=72a9d06377541b7b266e0d8153e89a7ae19afb95`. Travaux existants : PR #17 (contrôle géométrique), #18 (laboratoire cartographique), #19 (gel de l'archive) — tous **en brouillon**, non fusionnés lors du contrôle de départ.
- Nouvelle branche indépendante `dev/apur-private-period-candidate-20261016`, sans réécriture de `main`, aucun fichier `site/`, aucun changement Docker/Traefik/BDD.
- `AGENTS.md`, checkpoint Apur et passation ont été relus avant intervention. La ressource `repo:Kiwinokoto/vacant` et le stockage `state:vacant` ont été verrouillés via AgentCTL avant écriture et exécution.
- Production vérifiée inchangée : release `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`, conteneur actif, 0 redémarrage.

## Source figée, conditions d'usage

- Apur : `EMPRISE_BATIE_PARIS`, source officielle du portail ArcGIS Hub, licence **ODbL-1.0**. Archive privée `/srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip`, **31 981 417 octets**.
- SHA-256 original : `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11` ; manifeste figé associé. L'auditeur vérifie avant transformation la taille, l'empreinte, les cinq composants SHP, CRC et `.prj=EPSG:2154`.
- Dates différentes : métadonnée du Géocatalogue `lastUpdate=2025-02`, édition de lignes jusqu'en septembre 2026, export daté HTTP octobre 2026. **Millésime scientifique non attesté**. Courriel déjà envoyé à `data@apur.org` le 16/10/2026 ; aucune relance en doublon.
- Un objet Apur est une emprise ou portion bâtie actuelle, **pas nécessairement un bâtiment distinct**, encore moins un logement vacant. Ni jointure Insee/LOVAC, ni publication de données individuelles. Avant diffusion d'une base adaptée, revoir obligations de licence ODbL, attribution et modalités de partage.

## Générateur privé et filtrage

- Script `scripts/build_apur_period_candidate.py` ; test `tests/test_build_apur_period_candidate.py`. **Hors réseau** ; aucun GeoJSON ni emprise individuelle en Git.
- Emprise WGS84 du laboratoire : **longitude 2.373 à 2.376, latitude 48.854 à 48.856**. Sélection par intersection avec le contour géographique densifié et reprojeté en Lambert-93, non la bbox Lambert-93 (qui inclurait trois objets supplémentaires). Les polygones ne sont **pas découpés** à cette fenêtre.
- Refuse si la sélection source dépasse **200** objets avant d'écrire. Ne garde que les formes GEOS valides, emprises avec `n_sq_eb` renseigné, `OBJECTID` unique, codes de période connus (y compris non daté). Aucun `make_valid`, `buffer(0)`, nettoyage silencieux, date inventée ou hauteur non demandée.
- Sortie atomique **sans remplacement concurrent** (`os.link`), répertoire privé `0700`, fichier `0600`, interdiction des sorties dans `site/`, `.git/`, `raw/`, `releases/` ou vers un lien symbolique préexistant. La sortie inclut `public_release_allowed=false`, `scientific_vintage=not confirmed by Apur`, la provenance et des compteurs.

## Exécution sur l'archive réelle

Commande exécutée depuis le clone propre de cette branche, dans le venv VACANT :

```sh
/srv/vacant/venv/bin/python scripts/build_apur_period_candidate.py \
  /srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip \
  /srv/vacant/data/raw/apur/frozen-2026-10-16/manifest.json \
  /srv/vacant/data/processed/apur/experiment-20261016/paris-neighborhood-periods.geojson \
  --bbox 2.373 48.854 2.376 48.856
```

- **150 emprises intersectent** cette zone, **150 sont conservées**, 0 exclusions.
- Contrôle indépendant du GeoJSON : **150/150 géométries GEOS valides**, 150 identifiants `object_id` distincts, champs propriétés autorisés uniquement, toutes les emprises intersectent bien la zone WGS84, métadonnées strictement privées et sans vacance.
- Catégories dans la zone : `1=4, 2=38, 3=56, 5=8, 6=3, 7=2, 8=2, 9=2, 10=28, 11=7`. Ce sont des **emprises actuelles classées par période**, pas un état historique reconstitué.
- Sortie **90 771 octets**, mode `0600`, SHA-256 :
  `f3ea9035458c777a0424ab1e68874c20ea49e03ed3616df54157f416ef365340`.
- **Tests sur clone GitHub frais : 56/56 Python, 25/25 JavaScript.** Tests nouveaux : cas de dépassement de limite sans écriture, empreinte source altérée, topologie invalide, clé métier absente, sortie privée, lien symbolique, attributs. Aucun test navigateur ni déploiement de ce dérivé lors de cette passe.

## Suite et conditions bloquantes

1. Examiner la réponse de l'Apur sur la date scientifique et les conditions de rediffusion ODbL avant publication de la moindre base dérivée.
2. Préparer **sans publier** un protocole de contrôle cartographique sur copie locale de ce GeoJSON privé (légende, attribution, avertissement sur la datation, erreurs et mobile).
3. À l'échelle de Paris, les **104 polygones invalides** et les **13 `n_sq_eb` absents** restent signalés/filtrés ; aucun nettoyage silencieux ni dénombrement de logements.
4. Vérifier revue des PR et protections GitHub, tester intégration de la couche indépendante, puis décision distincte de publication. **Ne pas modifier `site/` ni la release existante par réflexe.**
