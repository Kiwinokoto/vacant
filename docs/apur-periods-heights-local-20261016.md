# VACANT — intégration expérimentale des périodes et hauteurs Apur

**16 octobre 2026 — laboratoire strictement local, non publié.**

## Base GitHub et décisions

- Dépôt canonique : `Kiwinokoto/vacant`. `main` vérifiée au départ : `72a9d06377541b7b266e0d8153e89a7ae19afb95`.
- Travaux existants en brouillon : PR **#17** (échantillonnage), **#18** (recette périodes), **#19** (archive source + audit GEOS), **#20** (dérivé de 150 emprises). Aucune n'a été fusionnée dans cette passe.
- Branche : `dev/apur-periods-heights-local-20261016`. **Aucun changement d'architecture serveur, de conteneur ni de base de données.** La nouvelle fonctionnalité doit rester invisible sur les noms de domaine publics, même si la PR devait être fusionnée par erreur.
- La production garde sa release `1e6d47c6df13faf83b5b9e7e2d752ce02d9897d0`. Ne pas déployer cette branche avant contrôle des droits et validation explicite.

## Provenance et hypothèses scientifiques

Source : Apur, `EMPRISE_BATIE_PARIS`, [jeu public](https://opendata.apur.org/datasets/emprise-batie-paris), licence **ODbL-1.0**, [documentation](https://www.apur.org/open_data/EMPRISE_BATIE_OD.pdf). Source privée déjà figée sur le VPS : `/srv/vacant/data/raw/apur/frozen-2026-10-16/EMPRISE_BATIE_PARIS.shp.zip`, SHA-256 :

`f6d612844829dbf610fabf89dd442f6c50b4d8b04b33745e55e3e983c6e74e11`.

Les dates de mise à jour documentaire, géocatalogue et de modification des objets **ne constituent pas un millésime scientifique certifié unique**. Courriel envoyé à l'Apur le 16 octobre, réponse en attente. La période `c_perconst` est une catégorie attribuée à une **emprise bâtie actuelle**, non une preuve d'état à une date passée. Une emprise peut comprendre plusieurs bâtiments.

- Classes périodes : `1,2,3,5,6,7,8,9,10,11,12,99`, dont `11=2000–2007` et `12=2008 et après` selon fiche et codedValues, malgré une légende amont ambiguë.
- `h_med` est une **hauteur médiane en mètres**, jamais le nombre d'étages `H_ET_MAX` de Paris Data.
- Hauteurs nulles, absentes, nulles à zéro ou contradictoires avec `h_min/h_max` : représentées comme **indisponibles**. Pas de correction silencieuse, ni plafond arbitraire : les rares édifices de plus de 200 m restent possibles.
- Aucune vacance Insee, LOVAC ou adresse associée aux 150 emprises. Pas d'inférence de vacance à l'immeuble.

## Dérivé local privé et chaîne de calcul

Le générateur `scripts/build_apur_lab_heights.py` rapproche uniquement les `OBJECTID` d'un **dérivé privé déjà validé** (PR #20) avec les enregistrements du SHP Apur figé, puis ajoute `height_m` à `period_code`. Il vérifie en amont les deux SHA-256, le CRS EPSG:2154, la cardinalité 128 206 et la correspondance des 150 identifiants. Une erreur ferme l'exécution sans écrire de résultat. La sortie est créée sans possibilité d'écrasement dans un répertoire `0700`, avec mode `0600`.

Sources privées :
- Dérivé périodes : `/srv/vacant/data/processed/apur/experiment-20261016/paris-neighborhood-periods.geojson` — SHA-256 `f3ea9035458c777a0424ab1e68874c20ea49e03ed3616df54157f416ef365340`.
- Nouveau dérivé périodes + hauteurs : `/srv/vacant/data/processed/apur/experiment-heights-20261016/apur-period-height-local.geojson` — **92 993 octets**, SHA-256 `ba14be71c3cb58afcae935bcdc3f775f63ad043d12ecb20f42bdf2da759afaf9`.

Le résultat couvre les **150 mêmes emprises**, toutes avec hauteur `h_med` exploitable sur ce secteur particulier (pas une garantie pour Paris entier). Aucune donnée/forme Apur individuelle n'est copiée dans Git.

## Interface intégrée, verrouillée par défaut

Modifications dans `site/` :
- `index.html` : groupe `#apur-local` **hidden**, choix périodes / hauteurs, avertissements ODbL, lien direct vers la carte sur mobile.
- `app.mjs` : ne charge le module expérimental que si `labEnabled(window.location)` est vrai.
- `apur-lab-contract.mjs` : n'active le mode que sur `localhost`/`127.0.0.1`/`[::1]` avec `?apur_lab=1`. Exige le SHA-256 fixé, 150 objets, CRS déclaré, droits et statut expérimental ; refuse données de vacance, champs inattendus, valeurs et géométries manifestement non conformes.
- `apur-lab.mjs` : couches Leaflet exclusives ; légendes distinctes, popups sans HTML fourni par la source, synchronisation de la case des volumes, passage périodes ↔ hauteurs **sans nouveau téléchargement**, retour à la carte volumes. L'IRIS et les arrondissements restent des observations statistiques territoriales distinctes.
- `site/data/.gitignore` : exclut le dérivé privé `apur-lab.geojson`. Le chemin relatif de chargement `./data/apur-lab.geojson` doit rester **absent de la production**.

La condition sur l'hôte n'est **pas un mécanisme d'autorisation serveur** : l'absence du fichier privé hors de la machine de test reste essentielle. Une vraie diffusion nécessitera une revue ODbL, un contrat de version scientifique et une stratégie explicite de distribution/tuilage avec attribution.

## Recette réalisée

Vérifications sur clones GitHub neufs de la branche. Suite Node : **36/36** (11 tests nouveaux) ; Python **56/56** (8 tests nouveaux). Génération effective depuis le ZIP privé : **150 emprises**, **150 hauteurs exploitables**, sortie SHA-256 vérifiée.

Recette Chromium 154 via serveur HTTP strictement en boucle locale sur le poste Linux connecté, avec copie SCP temporaire de la fixture et dépendance Leaflet locale, tuiles OSM interceptées. Emprises affichées dans l'interface réelle de VACANT sur **1280 × 800**, **390 × 844** et **320 × 720** :

- Deux vues chargées et 150 emprises affichées ; changement de mode sans nouvelle lecture de fichier ; 12 entrées de légende de périodes et 6 classes métriques.
- Aucun débordement horizontal ni erreur JavaScript. Les couleurs, les unités et les avertissements sont lisibles sur captures examinées.
- Retour à « volumes actuels » : contrôles et titre restaurés, état « volumes » réellement reflété par sa case.
- Mode Apur invisible sur `/site/index.html` sans le paramètre localhost ; consultation publique inchangée.
- Échecs simulés 404 et altération du fichier → refus, sans fausse donnée ni remplacement de carte.
- Le test en format mobile utilise un navigateur de bureau émulant la taille d'écran, **pas un téléphone physique**. Le rendu très long de la colonne pédagogique place encore la carte sous la documentation sur mobile, défaut UX connu à traiter à l'intégration publique.

**Limites :** l'essai n'évalue que 150 emprises du secteur local ; l'extrapolation aux 128 206 objets demanderait un découpage spatial, traitement explicite des **104 invalides GEOS** et **13 ID métier absents**, gestion des droits d'une base adaptée et tests de performances réalistes. Le script n'effectue **aucune modification sur le service public**.

## Suite

- Garder la PR en **brouillon**, pas de merge ni déploiement.
- Attendre ou documenter indépendamment les obligations ODbL et l'attribution du millésime exact.
- Préparer une ingestion cartographique par secteur/tuiles, avec dérivés versionnés et exclusions traçables, **avant** d'exposer une couche Apur au public.
- Une éventuelle activation après revue devra rester séparée des couches Insee de vacance.
