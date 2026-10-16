# VACANT — double contrôle indépendant des contours historiques (16/10/2026)

## Décision

**Recherche privée uniquement.** Le recoupement de sources secondaires confirme l'intérêt des contours candidats 2013, mais **ne certifie pas** leur conformité à une livraison IGN d'origine. Aucun fichier ci-dessous ne doit servir de couche publique ou permettre l'inférence d'un logement vacant.

### Sources secondaires archivées sur le VPS

| Jeu | Source | Archive privée / SHA-256 | Restrictions |
|---|---|---|---|
| Contours 2013 adaptés aux communes OpenStreetMap | [data.gouv.fr](https://www.data.gouv.fr/datasets/decoupage-iris-combine-aux-limites-communales-openstreetmap), Vincent de Château-Thierry, 17/07/2015 | `raw/secondary/iris-2013-osm-secondary/source.zip` — `deb1b378aefa823ad3f2b22700c5c12b8133f782ddb87f059b1dc7518207a2c2` | **ODbL**. Le diffuseur dit avoir conservé les limites infracommunales IGN 2013 et remplacé des limites communales par OSM. Ce n'est pas l'original IGN. |
| Contours IRIS « 2016 V2.1 » reprojetés | [data.gouv.fr](https://www.data.gouv.fr/datasets/contours-iris-2016-version-2-1-france-dom-en-wgs84), publication 21/10/2017 | `raw/secondary/iris-2016-secondary/source.zip` — `843049e9af98c25bb74f9c8d8fe84348429596a3bf69fb6406b77fa8951436cd` | Licence Ouverte **déclarée par le tiers**. Archive sans fichier `.prj` : CRS WGS84 inféré de sa notice, vérifié par les coordonnées. **Ne pas l'utiliser pour les données RP2016 géographie 2018.** |
| Candidat 2013 préalable | [rapport](iris-2013-candidate.md) | `raw/secondary/iris-2013-candidate/iris-2013-01-01.zip` — `c6afee56f81b3a9d08316034f0f48259162276a3d7a0d11388c2472f2fd5d3a7` | Republication non attribuable à une archive IGN originale, 10 lignes/IRIS géométriquement équivalentes, audit privé uniquement. |

Toutes les archives sont hors du webroot et pourvues de manifestes source/taille/SHA-256 sous `/srv/vacant/data/manifests/`. Aucun changement de `site/` ni du conteneur public.

## Comparaisons réelles des polygones Paris en EPSG:2154

Un polygone par code IRIS après contrôle (992 codes communs, aucun invalide), calcul du recouvrement **IoU = aire(intersection) / aire(union)**. Les formes sont reprojetées en Lambert-93 pour mesurer les surfaces.

| Paire de sources | Codes appariés | Recouvrement médian | Minimum | IoU inférieur à 0,99 | IoU inférieur à 0,95 |
|---|---:|---:|---:|---:|---:|
| Candidat 2013 / adaptation OSM 2013 | 992 | **1,00000** | 0,78036 | 224 | 16 |
| Candidat 2013 / redistribution 2016 | 992 | **0,93688** | 0,66641 | 992 | 657 |
| Redistribution 2016 / IGN 2025 validé | 992 | **0,98472** | 0,65665 | 652 | 186 |

Pour la première paire, le résultat est **compatible avec** les modifications de limites communales décrites par le diffuseur OSM, mais l'emplacement exact des 224 écarts n'a pas encore été caractérisé. Il ne constitue donc pas une authentification de la livraison originale de 2013.

Le deuxième contrôle montre une évolution cartographique nette entre les deux sources secondaires 2013/2016. Le troisième rappelle que même des contours très proches de 2025 ne prouvent pas leur compatibilité avec l'année 2018 du recensement RP2016. Les distributions IoU ne séparent pas un changement statistique réel d'un recalage géographique.

## Réexécution

```sh
/srv/vacant/venv/bin/python scripts/audit_iris_crosscheck.py --data-root /srv/vacant/data
node --test tests/*.test.mjs
/srv/vacant/venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

Le script exige les manifestes, SHA-256 et la structure exacte des deux archives, extrait les Shapefiles dans des répertoires temporaires avec liste blanche, vérifie les 992 codes uniques, et recharge la géométrie 2025 au SHA-256 validé. Il ne génère **aucune** carte ou donnée publiée.

## Original IGN : piste officielle et blocage restant

- [IGN / data.gouv.fr — produit Contours…IRIS](https://www.data.gouv.fr/datasets/contours-iris-r-2) : données de l'édition courante, licence ouverte.
- [Catalogue officiel d'offres IGN](https://cartes.gouv.fr/aide/fr/partenaires/ign/referentiels-description-territoire/limites-administratives-reglementaires/decouverte-offre-produit/) : les anciennes éditions 2008/2013/2018 ne sont pas exposées ici comme téléchargements identifiables.
- [Insee — fonds de carte IRIS](https://www.insee.fr/fr/information/2017372) : depuis janvier 2016, l'IGN diffuse les fonds IRIS.
- La documentation IGN historique nomme explicitement **Contours…IRIS Version 1 / édition 2013** et les éditions 2008–2012 ; elle ne fournit pas automatiquement leurs archives binaires authentifiées.
- Contact officiellement indiqué : `contact.geoservices@ign.fr`. La demande technique prête à vérifier et transmettre est dans [demande-archives-ign.md](demande-archives-ign.md), **non envoyée**.

**Prochaine condition de promotion d'une couche 2011 à l'IRIS :** livraison officielle 2013 (ou validation écrite de l'IGN identifiant exactement le jeu secondaire), confirmation des conditions de rediffusion, comparaison des 992 géométries en EPSG:2154 et test SIG/navigateur. Pour 2006 et 2016, rechercher distinctement les contours des géographies 2008 et 2018. Jusqu'alors, garder l'historique **par arrondissement** et la couche IRIS fine uniquement en 2023.
