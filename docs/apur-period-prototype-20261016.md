# VACANT — laboratoire Apur : datation des emprises bâties par période

**16 octobre 2026, 19 h 20 (Europe/Paris).** Recherche et prototype **hors production**, sans modification de `site/`, sans export des 128 206 polygones ni attribution de vacance. Dépôt source : `Kiwinokoto/vacant`, branche `dev/apur-period-experiment-20261016`, partie de `main=72a9d06377541b7b266e0d8153e89a7ae19afb95`. PR #17 demeure une revue de qualité géométrique indépendante, non fusionnée.

## Provenance et licence vérifiées

- Apur, **fiche officielle** [EMPRISE BATIE (DECOMPOSEE) PARIS](https://www.apur.org/open_data/EMPRISE_BATIE_OD.pdf), dernière version de la *fiche* datée du **01/09/2019**. Elle indique explicitement **ODbL** comme droits d'usage/diffusion (p. 1), les codes de construction (p. 2), les sources de datation et leur imprécision (pp. 4–5), et la « Date de l'information : **2019** », actualisation ponctuelle (p. 5). Cette date n'est **pas** celle d'un export de géométries actuellement téléchargé.
- [Présentation officielle Apur](https://www.apur.org/fr/open-data-cartes/open-data/emprises-baties-paris-metropole-une-lecture-tissu-urbain) de **septembre 2024** : emprise possiblement multiple pour plusieurs bâtiments, documentation publique. Ce n'est pas une date probante de la dernière révision SIG.
- [Catalogue de données Apur](https://opendata.apur.org/datasets/emprise-batie-paris), et service interrogé [ArcGIS couche 0](https://carto2.apur.org/apur/rest/services/OPENDATA/EMPRISE_BATIE_PARIS/MapServer/0), polygonal Lambert-93 (EPSG:2154), restitué en WGS84 pour affichage. Le service ne renvoie pas de date d'édition d'objet ou `editingInfo` exploitable, ni de `serviceItemId`.
- Un **miroir** [SmartIDF](https://data.smartidf.services/explore/dataset/emprise-batie-paris/) annonce une modification du catalogue au 30/07/2026 et un traitement de données en septembre 2026. Ces dates de traitement du **miroir** ne démontrent **pas** un millésime Apur. La version précise du jeu servi, l'archive officielle immuable, la date du fichier source et son SHA-256 restent **non confirmés**.
- ODbL : la consultation ponctuelle via API, avec attribution visible et lien vers le producteur, n'est pas ici présentée comme une autorisation pour republier une base dérivée complète. Avant tuilage/hébergement d'une base adaptée, clarifier la qualification de base dérivée, le partage à l'identique, l'attribution et la notice de licence. Le dépôt ne redistribue aucune géométrie Apur.

## Légende de périodes (dictionnaire documentaire)

| Code | Libellé |
|:--:|---|
| 1 | Avant 1800 |
| 2 | 1801–1850 |
| 3 | 1851–1914 |
| 5 | 1915–1939 |
| 6 | 1940–1967 |
| 7 | 1968–1975 |
| 8 | 1976–1981 |
| 9 | 1982–1989 |
| 10 | 1990–1999 |
| 11 | **2000–2007** |
| 12 | 2008 et après |
| 99 | Non daté |

`c_perconst=null` apparaît aussi dans le service et reste **non daté**. Les codes 1,2,3,5,6,7,8,9,10,11,12 et 99 concordent entre la fiche et les **codedValues** de la couche ArcGIS. **Anomalie de présentation amont :** le moteur de légende graphique ArcGIS (`drawingInfo.renderer.uniqueValueInfos`) annonce **« 2000 et plus » pour le code 11**, alors que les attributs codés et la fiche donnent 2000–2007. Le prototype s'appuie sur **les codedValues et la fiche** et n'interprète pas le texte du renderer.

Les périodes sont attribuées aux emprises existantes, elles ne permettent **pas** de représenter le bâti disparu ou l'état réel du territoire à une année historique. La fiche 2019 reconnaît les incertitudes individuelles (documents anciens, parcelles, enquêtes et classement automatique) ; pas de transfert automatique de période entre objets ou de jointure avec les volumes Paris Data.

## Fonctionnement et limites du prototype

- Chemin **non déployé** : `experiments/apur-periods/index.html` et `periods.mjs`. Ouvrir localement après lancement de `python3 -m http.server 8000` à la racine du dépôt, puis `http://localhost:8000/experiments/apur-periods/`.
- Chargement **uniquement au clic**, périmètre de quelques rues (latitude au plus 0,004°, longitude au plus 0,006°, enveloppe prudente de Paris). Requête REST `returnCountOnly=true` puis, si et seulement si **0 à 200** objets, GeoJSON trié par `OBJECTID`. Pas de pagination trompeusement présentée comme exhaustive ; refus explicite si trop d'emprises.
- Seuls `OBJECTID`, `n_sq_eb`, `c_perconst` sont sollicités. Normalisation et liste blanche locales vers identifiant + code, sans donnée de logement, adresse, hauteur ni vacance. Polygones WGS84 à anneaux fermés, bornes et nombre de sommets bornés ; catégories et cardinalités contrôlées. Contrôle JS structurel **pas** équivalent à la validation topologique GEOS d'un export complet.
- Pas de données GeoJSON Apur en Git, pas de stockage disque ou serveur, pas de jointure Insee/LOVAC/Paris Data ; données directement tirées du service public dans le navigateur. Le déploiement de VACANT copie uniquement `site/`, donc **aucune activation de ce prototype** en production.
- © Apur, licence ODbL, lien source et documentation sont visibles, ainsi que la mention d'incertitude. Carte OSM pour consultation limitée, pas pour trafic industriel.

## Validation effectuée

1. Requête de contrôle sur `2.373–2.376 E ; 48.854–48.856 N` : **153** emprises, ~**97 732 octets** en GeoJSON, retour réseau observé ~**0,16 s** sur le VPS (sans navigateur). CORS : origin `http://localhost:8000` admise pour la réponse GeoJSON.
2. Tests sur clone propre de la branche, Node 22 : **35/35** (10 tests nouveaux). Python 3 / venv : **48/48**. Tests couvrant classes, champs autorisés, zone, anneaux, nombre maximal, doublons, pagination tronquée, échec réseau et zéro objet.
3. Chromium 154 réel sur poste Linux Mint, chargement via serveur HTTP local :
   - **Desktop 1280×800** : **84 emprises** et 12 entrées de légende ; environ **357 ms** pour les deux appels et traitement affiché ; carte de 637 px, pas de débordement horizontal, aucune erreur JS.
   - **Mobile 390×844** : **37 emprises**, environ **148 ms**, carte de 473 px, pas de débordement horizontal, aucune erreur JS.
   - Un défaut de hauteur de la carte desktop, puis un excès d'objets dans la vue initiale ont été détectés et corrigés (hauteur contenue ; zoom initial 19). L'ancien défaut refusait 236 objets à la vue zoom 18 : **refus sûr**, pas publication partielle.
4. Latences locales sur petite zone **non extrapolables** à l'ensemble de Paris, au débit réel des utilisateurs ni aux téléphones physiques. Le navigateur affiche directement l'API Apur : disponibilité, CORS ou changement de schéma peuvent interrompre l'expérience. Aucune mesure de performances avec 200 polygones ou sur plusieurs dizaines de sessions simultanées.

## Blocages avant activation sur VACANT

- Obtenir une **archive Apur officiellement datée**, calculer son SHA-256, archiver la notice des droits et comparer la cardinalité et le dictionnaire au service vivant.
- Contrôler la licence ODbL pour un éventuel dérivé hébergé (base adaptée / partage à l'identique) et son attribution ; vérifier la politique de requêtes et CORS.
- Étendre QA SIG sur échantillon spatial représentatif (arrondissements, classes rares), vérifier géométries GEOS, doublons, données manquantes et exactitude des classes.
- Tester accessibilité mobile, failover réseau, typologies, charge et retour utilisateur ; évaluer des tuiles vectorielles seulement avec droits et version cohérents.
- Ensuite seulement PR dédiée à une intégration UI explicite (couche **période d'emprise Apur** indépendante de la vacance), avec recettage et validation avant déploiement.
