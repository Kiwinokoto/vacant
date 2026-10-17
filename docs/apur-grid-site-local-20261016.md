# VACANT — raccordement local de la grille Apur 500 m à l'interface

**16 octobre 2026 — recherche et recette privée, aucune publication.**

## État Git / release

- Dépôt canonique : `Kiwinokoto/vacant`. `main=72a9d06377541b7b266e0d8153e89a7ae19afb95` au contrôle. Production volontairement maintenue sur la release `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`.
- Base de cette passe : PR **#23** consolidée, commit `242799a83c4846d3ad55da948b7405a832dbd5b3`, qui conserve l'ascendance des PR #17–#22. **Nouvelle branche empilée** `dev/apur-grid-site-local-20261016`. Cibler la PR de suivi sur cette branche consolidée (non `main`) ; ne pas fusionner directement la chaîne.
- Vérification préalable AgentCTL : aucune autre session/lease VACANT active. Verrou exclusif `repo:Kiwinokoto/vacant` acquis avant écriture. Ancien clone de travail VPS propre, aucune modification non attribuée. Aucun changement Docker, VPS, service, BDD ni version publique.

## Contrat SIG

Le jeu Apur source est le même export officiel figé : SHA-256 ZIP `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`, `128 206` enregistrements, **104 géométries GEOS invalides** et **13 clés métier nulles** exclues. Grille Paris 500 m : **456 cellules**, **128 089 emprises uniques**, **138 381 occurrences** dont les répétitions sont dédoublonnées par `OBJECTID`. Manifeste privé SHA-256 `bb02fe9ac9ef7919018118659e12ac533b098234250eba540c6975e7b273bb0c`.

- Source privée conservée : `/srv/vacant/data/processed/apur/paris-grid-experiments/cells-500m-original/` sur le VPS, **pas** dans le dépôt ni sous la racine publiée.
- Le navigateur utilise le manifeste et les cellules sous **`site/data/apur-grid/` uniquement sur le poste de recette**. Le répertoire complet est ignoré par Git via `site/data/apur-grid/.gitignore`. Aucune géométrie Apur, capture ou manifeste n'est committé. Il n'existe pas de repli vers l'API Apur.
- Deux modes de coloration : **périodes attribuées** (`c_perconst`) et **hauteur médiane en mètres** (`h_med`, valeur indisponible conservée). Les emprises correspondent au bâti **actuel** ; ni reconstruction chronologique des bâtiments ni attribution d'une vacance à une emprise. Paris Data `H_ET_MAX` représente des **étages**, jamais des mètres.
- Le millésime métier reste non confirmé par l'Apur ; l'extraction date du 16/10/2026 et l'ODbL impose attribution et étude des obligations de distribution d'une base adaptée avant mise en ligne. La demande Apur est déjà envoyée ; ne pas la répéter.

## Intégration technique (petits correctifs)

- `site/apur-grid-client.mjs` centralise le client déjà testé de `experiments/apur-grid/grid-client.mjs`, qui le réexporte désormais. Les deux appels acceptent exclusivement `./_local/` (ancien laboratoire) ou `./data/apur-grid/` (site local) ; URL HTTP(S) et chemins relatifs libres rejetés.
- `site/apur-lab.mjs` reprend le même `L.geoJSON` que le mode des 150 emprises : choix `grid-period` ou `grid-height`, contrôle du SHA-256 du manifeste et de **toutes** les cellules visibles, plafonds **12 cellules / 10 Mo / 5 000 occurrences**, dédoublonnage, rendu seulement après validation complète, popup sans HTML injecté, légendes distinctes. Bouton de **rechargement manuel** après navigation ; aucun préchargement des 456 cellules.
- Passage entre périodes et hauteurs de la même zone = **simple changement de couleur**, sans nouvelle requête. Le bouton de rechargement relit les cellules après un déplacement. En cas de 404/503, empreinte incorrecte, zone trop large ou mutation de carte pendant le chargement : **préserver la couche précédente** et afficher une erreur.
- `site/index.html` et `site/style.css` ajoutent les deux choix et le bouton sans affecter la UI publique. Mode **strictement invisible hors localhost/`?apur_lab=1`** ; absence du fichier privé en production volontaire. Les couches IRIS, arrondissements, volumes bâtis restent des couches **indépendantes et exclusives**.
- `tests/apur-grid-site.test.mjs` couvre chemins locaux autorisés, SHA-256, fichier absent/altéré, provenance et refus d'une URL API.

## Contrôles effectués

- Tests sur branche avec correctif : **71/71 JavaScript** dont cinq nouveaux, **81/81 Python** du socle consolidé à rejouer après finalisation du checkpoint.
- Recette **Chromium sur Linux** en boucle locale ; vraie copie SHA-256 du manifeste, **48 cellules réelles dans la zone de test** (sur 456 ; les autres restent privées sur VPS) et les deux GeoJSON publics IRIS/arrondissements de la release de référence. Ressources Leaflet 1.9.4 interceptées en fichiers locaux, tuiles externes bloquées.
- Desktop **1280×800** et mobiles simulés **390×844** / **320×720** : chargement initial de la grille (jusqu'à **2 284 emprises uniques** en zone), légende des 12 périodes, puis six classes de hauteur ; **zéro téléchargement supplémentaire au changement de coloration**. Pas de débordement horizontal ni erreur JavaScript.
- Simulations de panne : HTTP **503** pendant rechargement de cellules → carte et mode précédents conservés ; absence/corruption des fichiers couverte par tests Node. Passage à la **preview privée 150 emprises** conservé.
- Suite de transition réelle Chromium : Apur grille → **IRIS 2023** → **arrondissements 2023** → **volumes Paris Data** : modes et témoins d'interface correctement exclusifs, aucune erreur JS.
- Les temps locaux (environ 56 à 101 ms lors du premier essai) ne préjugent ni d'une connexion 4G ni de smartphones physiques. Les données de la grille entière ne sont **pas toutes copiées sur le poste** pendant cette recette.

## Limites et suite

**Ne pas fusionner ni déployer automatiquement.** PR empilée de recherche ; faire une revue de données ODbL et du millésime avant publication. Évaluer ensuite sur vrai mobile, mesurer la mémoire et le débit, étudier compression/tuiles vectorielles et disponibilité de la base adaptée. Aucun droit IGN historique supposé, aucune vacance attribuée aux emprises. Après toute passe, revérifier GitHub et AgentCTL et libérer le lock.
