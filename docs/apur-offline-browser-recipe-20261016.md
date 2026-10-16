# VACANT — recette cartographique locale sur l'export Apur figé

**16 octobre 2026 — labo hors ligne ; pas de déploiement, pas d'appel ArcGIS.**

## Provenance et périmètre

- Repo GitHub : `Kiwinokoto/vacant`, PR #18 (`dev/apur-period-experiment-20261016`) ; PR #17/#19/#20 toujours distinctes au début de la passe. La PR #18 a été étendue **sans modifier son prototype en ligne** (`experiments/apur-periods/index.html`).
- Données personnelles/de vacance : **aucune**. Extrait privé de 150 emprises actuelles classées par `c_perconst`, pas un inventaire historique ou des logements vacants.
- Apur, `EMPRISE_BATIE_PARIS`, ODbL-1.0, source ZIP privé : SHA-256 `f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`. Date d'acquisition : 16/10/2026 ; **millésime scientifique inconnu** (en attente de la réponse `data@apur.org`, demande déjà envoyée le 16/10).
- Candidat figé : `/srv/vacant/data/processed/apur/experiment-20261016/paris-neighborhood-periods.geojson`, **150 objets**, 90 771 octets ; SHA-256 `f3ea9035458c777a0424ab1e68874c20ea49e03ed3616df54157f416ef365340`. Le contrôle préalable avait validé **150/150** géométries GEOS sur le VPS. Aucune géométrie Apur versionnée ou rediffusée.

## Nouvel outil pour recette, sans API

- `experiments/apur-periods/offline.html` : page Leaflet de test, fond **neutre sans tuiles réseau**, légende colorée des 12 catégories dont code 11 = **2000–2007**, attribution et avertissements sur la datation.
- `experiments/apur-periods/offline-contract.mjs` : charge uniquement `./_local/fixture.geojson`, vérifie SHA-256 côté navigateur, schéma, origine, nombre exact 150, `OBJECTID` uniques, codes, forme des anneaux et propriétés strictement limitées. **Aucune solution de repli vers le service Apur**. Échec HTTP, schéma altéré ou empreinte erronée = erreur explicite, couche antérieure conservée.
- `experiments/apur-periods/.gitignore` ignore `_local/` pour éviter toute inclusion de la géométrie ou des fichiers temporaires dans une PR.
- `tests/apur-offline.test.mjs` : tests synthétiques sans réseau ni fixture Apur réelle ; validation de l'empreinte, des cardinalités, champs, géométries et provenance.
- `offline.html` requiert des copies **locales** de Leaflet 1.9.4 (`_local/leaflet.js` et `_local/leaflet.css`) ; aucune nouvelle dépendance/package du dépôt. Le fichier privé est fourni uniquement au poste de recette via SCP chiffré depuis le VPS autorisé.

### Mode opératoire reproductible (sur poste autorisé)

1. Dans un répertoire temporaire privé `0700`, cloner la branche GitHub de la PR #18. Ne pas utiliser les anciens clones comme source de vérité.
2. Placer les trois fichiers sous `experiments/apur-periods/_local/`, modes `0600` :
   - `fixture.geojson` : dérivé privé figé depuis le VPS, empreinte à revérifier contre `f3ea903...365340` ;
   - `leaflet.js` : `https://unpkg.com/leaflet@1.9.4/dist/leaflet.js` ;
   - `leaflet.css` : `https://unpkg.com/leaflet@1.9.4/dist/leaflet.css`.
3. Lancer un serveur HTTP **exclusivement sur 127.0.0.1**, avec racine sur le clone éphémère, sans exposer son port, puis naviguer vers `/experiments/apur-periods/offline.html`. Ne pas utiliser de serveur lié à `0.0.0.0`.
4. Dans Chromium, cliquer « Afficher les 150 emprises figées » et contrôler légende, couleurs, popups, avertissements, intégrité SHA, cardinalité, absence de trafic externe et absence de débordement sur 1280×800, 390×844 et 320×720.
5. Tester un HTTP 404, une altération de fixture (SHA-256), puis un HTTP 503 après affichage. Vérifier que la couche déjà chargée n'est pas remplacée par une fausse réponse partielle.
6. Arrêter le serveur et effacer uniquement les copies et captures temporaires créées pour cette recette ; conserver l'original privé sur VPS.

**Attention :** les contrôles de géométrie dans le navigateur sont structurels ; la preuve de topologie **GEOS** de ce snapshot provient de l'audit de l'archive dans la PR #20. Ce laboratoire ne constitue pas une validation des droits de rediffusion d'une nouvelle couche publique.

## Résultats contrôlés le 16/10/2026

Chromium **154.0.8037.97**, poste Linux Mint connecté via RDC, copie SHA-256 vérifiée, serveur HTTP **en boucle locale uniquement**. Scripts et tuiles chargés depuis le système local. Captures examinées visuellement en desktop et mobile ; **non committées**.

| Vue | Résultat | Latence affichage observée | Hauteur carte | Débordement horizontal |
|---|---|---:|---:|---|
| Desktop 1280×800 | 150/150 emprises | 66 ms (de clic à confirmation) | 672 px | Aucun |
| Mobile simulé 390×844 | 150/150 | 53 ms | 456 px | Aucun |
| Petit mobile simulé 320×720 | 150/150 | 45 ms | 389 px | Aucun |

La page présente les **12 entrées de légende**, dont le code 11 `2000–2007` en `rgb(94, 172, 179)`. Les cartes utilisent un canvas Leaflet, sans appel extérieur détecté. Les couleurs, la visibilité des informations de provenance et la disposition mobile ont été inspectées sur captures. Sur mobile, la carte se situe naturellement **sous** le texte et la légende : c'est approprié pour le laboratoire, mais un placement plus direct sera souhaitable avant une intégration produit.

**Interaction cartographique** : clic sur une emprise colorée dans Chromium desktop → popup ouverte avec identifiant, période attribuée et avertissement « Ni date certaine, ni indication de vacance ». Aucun champ supplémentaire exposé.

**Échecs contrôlés** : rechargement avec HTTP **503** (la couche précédente reste affichée), fichier absent **404** et fichier altéré (échec SHA-256), sans crash JavaScript. Chromium a loggé l'erreur ressource HTTP 503 *attendue* lors de l'injection de panne : ne pas confondre ce log intentionnel avec un échec inattendu de la recette. Aucun accès externe pendant les tests, pas de tentative de secours vers l'API Apur.

Tests Node sur clone branché PR #18 : **45/45 réussis** (10 nouveaux). Les latences locales de quelques dizaines de millisecondes ne préjugent **ni des téléphones physiques, ni des données Paris entières, ni de l'hébergement public**.

## Décision et suite

**Recette fonctionnelle et visuelle locale validée**, non suffisante pour publication. Prochaine décision : consulter la réponse officielle Apur (millésime/ODbL), étudier le traitement documenté des 104 géométries GEOS invalides et 13 identifiants absents au niveau Paris, puis proposer une intégration optionnelle séparée de VACANT avec recette réseau/mobile physique. **Ne pas déployer la PR #18 ni exposer le fichier `_local/fixture.geojson`**. La production publique reste `1e6d47c`.
