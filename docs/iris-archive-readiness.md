# VACANT — préparation des archives IGN 2008 et 2018

Recherche du 16 octobre 2026. Inventaire des preuves, pas validation de géométries non acquises.

## Attention aux millésimes de livraison

Dans le suivi des évolutions officiel de Contours… IRIS® (IGN, septembre 2019) :
- **2008** : création du produit Contours… IRIS® version 1.0, successeur de Base-Îlots 2.0. Un fond spécifique d'époque existe historiquement, distinct des contours IGN récents.
- **Édition 2018** : IRIS **2017 consolidés** et nouveaux IRIS **2018 non consolidés**.
- **Édition 2019** : IRIS **2018 consolidés** et nouveaux IRIS **2019 provisoires**.

Une référence publique de livraison nommée CONTOURS-IRIS_2-1__SHP__FRA_2018-06-08 pointe vers un sous-répertoire CONTOURS-IRIS_2-1_SHP_LAMB93_FXX-2017. Un fichier daté 2018 ne prouve donc pas qu'il convient pour le RP2016 en géographie Insee **2018**.

Sources :
- IGN, suivi des éditions : https://geoservices.ign.fr/sites/default/files/2021-07/SE_Contours-IRIS.pdf
- IGN, limites d'IRIS : https://geoservices.ign.fr/sites/default/files/2022-08/SE_Limites_IRIS_0.pdf
- Exemple de téléchargement 2017 : https://claudegrasland.github.io/DataMiningProject2021/11-data.html
- Exemple d'arborescence 2018/FXX-2017 : https://github.com/aelessa/ile-de-france/blob/develop/docs/population.md
- Référentiels Insee 2008/2018 : https://www.insee.fr/fr/information/7708995

## État des quatre couples recensement / géographie

| RP | Géographie Insee cible | 992 codes Insee | Fond de géométrie cible authentifié | Diffusion IRIS |
| --- | --- | --- | --- | --- |
| 2006 | 2008 | Oui | **Non** | Non |
| 2011 | 2013 | Oui | Candidat fortement corroboré par Atlasanté 2014 ; année officielle/licence à confirmer | Non |
| 2016 | 2018 | Oui | **Non** ; 2016 et FXX-2017 ne conviennent pas sans audit | Non |
| 2023 | 2025 | Oui | Oui | Oui |

**Aucun nouvel original 2008/2018 n'a été obtenu** pendant cette passe. Ne jamais réutiliser silencieusement une ancienne géométrie candidate comme fond d'une autre année.

## Critères d'admission pour toute nouvelle archive

1. Archive officielle ou provenance institutionnelle attestée, URL, millésime réel des données, édition/version, notice et licence de l'édition, date de collecte et SHA-256.
2. Inspection sûre de l'archive et des sous-répertoires ; ne pas prendre la date du conteneur 7z pour la géographie.
3. Codes Paris : 992 identifiants uniques, types IRIS concordants avec la référence Insee du millésime, CRS déclaré et contrôlé.
4. Géométries : validité GEOS, topologie, couverture, comparaison surfacique en Lambert-93 avec les autres éditions et identification des écarts.
5. Compatibilité RP2006/2008 ou RP2016/2018, pas d'attribution de la vacance à un immeuble.
6. Licences de rediffusion explicites, seuils de masquage, attribution, tests unitaires et navigateur avant publication.

La demande IGN a déjà été envoyée le 16/10/2026. Ne pas la doubler ; rechercher sa réponse dans Gmail.

## Correctif de l'interface préparé

Le titre de carte précise dorénavant volumes actuels / IRIS 2023 / arrondissements et distingue année du recensement, géographie IRIS du recensement et limites d'arrondissement IGN 2025. La légende utilise des intervalles non ambigus. Le contrat de publication bloque les couches IRIS historiques non autorisées ; leurs contrôles privés restent permis. Ce correctif ne publie pas de nouvelles données historiques.
