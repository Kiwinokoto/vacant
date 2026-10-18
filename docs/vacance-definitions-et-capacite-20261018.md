# VACANT — Définition des stocks et estimation du potentiel d’accueil (18 octobre 2026)

## Question

À Paris, **139 075 logements sont statistiquement vacants au RP2023**. Ce chiffre est fondé mais ne signifie ni 139 075 logements libres aujourd'hui, ni un nombre de personnes pouvant être logées. L'objectif est de caractériser les situations durablement inoccupées, les logements remis en usage sans travaux et ceux transformables après travaux, sans recouper des univers incompatibles.

## Définitions et états mesurés

| Univers | Date de référence | Nombre | Mesure | N'infère pas |
|---|---|---:|---|---|
| Insee RP2023 | Recensement 2023 (données publiées en 2026) | **139 075** | Logements inoccupés au sens du recensement, 9,9 % des **1 402 024** logements parisiens | Durée, habitabilité, disponibilité |
| Insee RP2023 | Même période | **138 426** | Résidences secondaires et logements occasionnels, catégorie **distincte** des vacants | Logements vides ou réaffectables |
| Insee RP2023 | Même période | **1 124 522** | Résidences principales | — |
| LOVAC, production 2026 | **01/01/2025** | **105 785** | Logements privés fiscalement déclarés vacants | Vacance au sens Insee, occupation physique certaine |
| LOVAC, production 2026 | **01/01/2025** | **26 264** | Sous-ensemble précédent vacant depuis plus de deux ans ; 24,8 % **parmi les vacants privés fiscaux** | Vacance structurelle certaine, logements remis à disposition |
| Apur BDCOM, note 2026 | Avril 2026 | **8 323** | Locaux de RDC vacants hors travaux (83 115 locaux étudiés) | Logements ni locaux habitables |
| Apur BDCOM, note 2026 | Avril 2026 | **1 402** | Locaux de RDC en travaux, séparés | Réutilisation immédiate |
| Cushman & Wakefield / ImmoStat T3 2026 | Septembre 2026 | **1 578 000 m²** | Offre immédiate de bureaux à Paris intra-muros | Bureaux physiquement déserts depuis longtemps, logements ou places |

**Calcul contrôlable Insee** : 139 075 + 138 426 = **277 501**, soit **19,8 % de 1 402 024** logements qui ne sont pas des résidences principales. Les catégories sont disjointes *au sein du tableau Insee*, mais cela ne transforme pas les résidences secondaires en logements vacants. Aucun autre chiffre du tableau ne doit être ajouté à LOVAC, BDCOM ou aux m² de bureaux.

**Définition Insee** : proposé à la vente/location ; attribué mais en attente d'occupation ; succession ; réserve d'employeur ; laissé sans affectation, éventuellement vétuste. Ces situations incluent une **vacance frictionnelle** liée au roulement locatif. Sources :
- https://www.insee.fr/fr/metadonnees/definition/c1059
- https://www.insee.fr/fr/statistiques/2011101?geo=DEP-75

## Vacance durable : observations historiques et limites

Selon **Apur, note 2021 / étude juillet 2022**, la première livraison LOVAC identifie **18 648 logements vacants depuis plus de deux ans en 2020**, contre 117 082 logements vacants Insee au **RP2017**. Ces dates, méthodes et parcs sont différents : la juxtaposition illustre les périmètres, **pas** un calcul harmonisé du pourcentage de vacance frictionnelle.

La distribution du **LOVAC 2020** étudiée par l'Apur renseigne mieux l'idée de personnes logeables :
- **8 102 T1 = 43,4 %** du groupe durablement vacant (18 648) ;
- **8 211 logements = 44 %** avaient moins de 30 m² ;
- **surface médiane de 32 m²**, moyenne 49 m².
Ces résultats ne peuvent pas être appliqués sans examen au stock **26 264 de LOVAC 2026** ; structure du parc et méthode GMBI ont évolué. Ils excluent de multiplier indistinctement chaque vacant par 2 ou 3 personnes.

Sources :
- https://www.apur.org/fr/logement-hebergement/parc-prive/18-600-logements-durablement-vacants-paris-2020
- https://www.apur.org/sites/default/files/logements_durablement_vacants_paris.pdf
- https://doc-datafoncier.cerema.fr/doc/guide/lovac/lobservation-de-la-vacance-des-logements
- https://doc-datafoncier.cerema.fr/doc/guide/lovac/differenciation-entre-vacance-fiscale-et-vacance-au-sens-de-linsee

Le seuil **plus de deux ans** est une **approximation opérationnelle** de la vacance structurelle : il existe des vacances de longue durée non structurelles et des vacances de moins de deux ans qui deviendront structurelles. L'Insee observe par enquête et LOVAC par déclarations fiscales : **aucune division croisée Insee/LOVAC** ne doit servir de taux de vacance structurelle.

## Modèle de mobilisation — inconnu par défaut

Le passage du « stock vacant » à des places de logement impose :
1. **Dénominateur** du même univers, même géographie et date ; statut de vacance *réellement observé* et durée ;
2. **Habitabilité / sécurité** : surface, sanitaires, lumière, ventilation, risques, travaux, accessibilité ; un logement très dégradé n'est pas automatiquement irrécupérable ;
3. **Disponibilité juridique / économique** : propriétaire, occupation légale, succession, financement, autorisations et éventuel changement de destination, sans publier de données individuelles ;
4. **Capacité** : seulement après typologie des surfaces/pièces et usages adaptés, en respectant la composition des ménages et les conditions d'hébergement ;
5. **Délai** : immédiatement disponible / travaux légers / transformation lourde / potentiel non vérifié.

**Aucun facteur moyen du type « logements × 2 personnes » n'est autorisé** sans distribution actuelle et hypothèses sourcées. Les nombres mobilisables et de personnes pouvant être logées sont **inconnus** à ce stade ; ils ne sont ni zéro, ni l'ensemble des stocks administratifs.

## Prochain chantier prioritaire

1. Demander / retrouver des agrégats autorisés LOVAC récents ventilés à Paris par durée, taille, nombre de pièces et confort **sans microdonnée**. Vérifier les changements GMBI 2023–2026 avant comparaison.
2. Faire une matrice de **faisabilité technique** sur échantillons documentaires anonymisés : immédiatement habitable / réparable / convertible / état inconnu ; tester la sensibilité aux hypothèses, sans annoncer une capacité fictive.
3. Pour locaux RDC et bureaux, garder unités et périmètres séparés : vérifier inoccupation réelle, état du bâti, disponibilité et changement de destination avant une quelconque conversion en logements ou places.
4. Préserver les droits de diffusion LOVAC : seul l'agrégé ouvert est public ; pas d'adresse ni de propriétaire publiés et pas d'application de la vacance IRIS à un bâtiment.

**Source complémentaire bureaux** : https://www.cushmanwakefield.com/fr-fr/france/news/2026/10/reactions-immostat-t3-2026
