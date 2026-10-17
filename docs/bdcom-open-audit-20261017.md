# VACANT — Audit BDCOM 2023 et indicateurs de bureaux (17/10/2026)

**Statut** : données publiques agrégées vérifiées à Paris, PR #35 en brouillon, sans diffusion de points/adresses. Code/ressource : `site/data/bdcom-paris-arrond-2023.json`.

## 1. Source BDCOM vérifiée

- Source institutionnelle : Apur, [BDCOM 2023](https://opendata.apur.org/datasets/Apur::bdcom-2023/about) ; licence **ODbL**, attribution « © Apur, BDCOM 2023 », dérivés BDCOM à partager sous les mêmes conditions.
- API institutionnelle : [ArcGIS MapServer, couche 1 « Local »](https://carto2.apur.org/apur/rest/services/BDCOM/bdcom2023/MapServer/1), couche source à **83 154** objets (relevés de locaux avec vitrine et accès depuis espace public ou équivalent). **Ne pas utiliser la couche 0**, filtrée sur 60 845 commerces/services, comme dénominateur des locaux vacants ; le rapport publié donne 60 846 commerces/services, autre écart d'une unité.
- Recensement Apur annoncé en **avril 2023** dans la [note n°236](https://www.apur.org/sites/default/files/8p236_bdcom_2023.pdf), mais le descriptif open data mentionne juin 2023 pour l'enquête. Ces dates divergent : utiliser **« enquête BDCOM 2023 »** sans interprétation plus fine jusqu'à confirmation Apur.
- Requêtes statistiques exécutées le **17 octobre 2026 à 09:35:51 UTC** (indépendantes des données individuelles) :
  - total : `where=1=1`, `returnCountOnly=true` -> **83 154** ;
  - `groupByFieldsForStatistics=arro`, statistique `count(OBJECTID)` -> vingt totaux par arrondissement ;
  - `codact='AA101'` (« Local vacant ») -> **7 495** ;
  - `codact='AA102'` (« Local en travaux ») -> **1 565** ;
  - les deux regroupés dans `type='V'` / `niv18=213` : **9 060** enregistrements (10,9 % arrondi des 83 154). `type='V'` **ne signifie donc pas « vacant hors travaux »** ;
  - `type='B'` désigne **6 898 bureaux en boutique dans le champ BDCOM**, catégorie différente de `type='V'`, **sans mesure de bureaux vacants en étage**.
- Groupements calculés côté serveur avec `outStatistics=[{"statisticType":"count","onStatisticField":"OBJECTID","outStatisticFieldName":"n"}]` et `returnGeometry=false`. **Aucune adresse, coordonnée, enseigne ni détail de commerce lu, enregistré ou publié** dans les fichiers dérivés. La couche brute ne doit pas être versée dans le dépôt.

### Contradiction documentaire (non corrigée artificiellement)

La note Apur n°236 annonce **9 059 locaux vacants**, dont **1 565 en travaux**, sur **83 154** en 2023. L'API ouverte expose **9 060** classés `type='V'` en les séparant en 7 495 `AA101` + 1 565 `AA102`. Écart : **+1** par rapport à la note, et non une simple erreur d'arrondi prouvée. Il peut provenir d'un état de fichier ou de conventions éditoriales : **cause inconnue**. Garder le chiffre de la note comme référence éditoriale et celui de l'API comme vérité du dérivé. Ne pas soustraire 1 local arbitrairement.

### Indicateurs à afficher

- **Vacance hors travaux** : `AA101 / total arrondissement` pour chaque arrondissement ; total Paris **7 495 / 83 154** (environ 9,0 %). Ce n'est **pas** le « taux de vacance commerciale Apur » regroupé (10,9 %) publié dans sa note.
- **En travaux** : `AA102 / total arrondissement` ; 1 565 locaux, environ 1,9 %.
- **Regroupement historique** : `AA101 + AA102` = 9 060 dans l'API ; note = 9 059.
- Le dénominateur de chaque arrondissement comprend tous les locaux du **périmètre BDCOM**, et non tous les locaux d'activité ni toutes les surfaces bâties. **Aucun statut individuel, aucun potentiel de logement**, pas d'addition aux ménages ni au parc LOVAC. La grille `surf` décrit seulement trois **classes**, pas des mètres carrés directement convertibles.

## 2. Bureaux Paris intra-muros — surfaces d'offre immédiate

- [Colliers, S1 2026](https://www.colliers.com/fr-fr/etudes/2026-2t-etude-marche-bureaux), daté du 9 juillet 2026 : **1,542 million de m² de bureaux dits vacants** dans *Paris intra-muros* fin juin 2026 ; indicateur de **marché locatif / offre disponible**, ne mesure pas la disponibilité pour habitation.
- [Cushman & Wakefield, T2 2026](https://cw-prod-gblgws-a-cm.cushwake.com/fr-fr/france/news/2026/07/immostat-s1-2026) : **environ 1,5 million de m²** d'offre immédiate, en hausse de 8 % en trois mois, dans Paris intra-muros. Confirmation indépendante de l'ordre de grandeur à fin juin.
- [Colliers, T1 2026](https://www.colliers.com/fr-fr/etudes/2026-1t-etude-marche-bureaux) annonçait pourtant **795 000 m²**, soit près de deux fois moins ; la hausse trimestrielle de 8 % donnée par Cushman ne correspond pas à ce changement. **Divergence importante non résolue ; ne pas publier de série ou variation T1→T2 Colliers**.
- [Colliers, T3 2026](https://www.colliers.com/fr-fr/etudes/2026-3t-etude-marche-bureaux) annonce **6,59 millions de m² pour l'Île-de-France** fin septembre, **pas** de total Paris-ville publiquement extrait dans sa page. Ne pas remplacer le chiffre parisien de juin par le total régional.
- **Ne pas mélanger surfaces proposées à la location, vacance réelle, vacance longue structurelle, stock total ou capacité d'hébergement.** Le rapprochement en 2026 se fait par *ordre de grandeur*, pas par addition au BDCOM ni aux logements.

## 3. Limites et suite

Enquête BDCOM 2026 réalisée en avril selon Apur, mais dataset ouvert accessible toujours 2023 (avec précédents 2017 et 2020). Auditer 2020/2017 à schémas et définitions cohérents avant historique. Demander à l'Apur la cause de la différence d'une unité et la date terrain précise. Pour les bureaux, demander le découpage Paris-ville T1/T2 2026 et les définitions d'« offre immédiate » ; chercher données publiques de vacance structurelle et travaux, sans présumer convertibilité. Retenir les propriétés d'enquête, unité, champ, géographie, licence, date d'extraction et incertitudes.

## 4. Contrôles automatiques

`site/bdcom-contract.mjs` rejette données sans 20 arrondissements, totaux non égaux au département, doublons, codes erronés, champs individuels, classement inconnu, provenance différente. `tests/bdcom-2023.test.mjs` vérifie ces interdictions. Le JSON dérivé est un jeu de 20 agrégats ; **aucune position de local n'est fournie**. Mise à jour manuelle ou script de collecte futur soumis à une nouvelle vérification SHA/date.
