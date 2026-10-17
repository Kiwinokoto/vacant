# VACANT — Vacance résidentielle, locaux non résidentiels et potentiel d'accueil

**17/10/2026 — première étude.** Page `site/potentiel.html`, PR #34 empilée sur #33 ; aucun déploiement.

## Hypothèse de recherche et limite

Ne pas traiter au même titre un logement habitable, un logement vétuste, un commerce vide ou un bureau inoccupé, mais ne **pas éliminer** ces derniers du champ. Les espaces non résidentiels peuvent mériter une étude de transformation ou d'accueil temporaire. **Possibilité théorique ≠ disponibilité réelle ≠ sécurité ≠ conformité ≠ autorisation juridique**. La lutte contre le sans-abrisme ne permet pas de recommander sans diagnostic l'occupation d'un lieu présentant des risques sanitaires ou d'incendie. Un logement dégradé n'est pas pour autant irrécupérable.

Cinq dimensions indépendantes : (1) destination, (2) occupation et date, (3) état/risques physiques, (4) autorisations/accès, (5) délais/coûts et usages (habitation durable versus hébergement temporaire). **Statut inconnu par défaut**, jamais habitable/inutilisable déduit d'un agrégat. Le nombre de locaux transformables en logements ou places d'hébergement reste **inconnu**.

## Observations disponibles, non sommables

| Source | Date | Champ | Mesure | Limite |
| --- | --- | --- | --- | --- |
| Insee RP2023 Paris | Recensement 2023 | Parc des logements total | **139 075 logements vacants / 1 402 024 logements** (9,9 %) | État d'habitabilité et disponibilité immédiate inconnus |
| DGALN/Cerema LOVAC | Millésime 2026 ; **situation au 01/01/2025** | Parc privé fiscal | **105 785 vacants**, dont **26 264 >2 ans** | Pas de taux de vacance 2026 sur tout le parc à date alignée ; GMBI 2024/2025 ; pas de diagnostic des locaux |
| Apur BDCOM | Terrain **avril 2023** | Locaux de rez-de-chaussée avec vitrine/accès public | **9 059 vacants / 83 154 locaux**, soit **10,9 %** | Pas les bureaux des étages ; pas des logements ni 9 059 possibilités d'accueil |

**Apur :** [note n°236, page 2](https://www.apur.org/sites/default/files/8p236_bdcom_2023.pdf). Le texte donne 9 059, alors qu'un graphique arrondit à 9 060. Le rapport compte aussi **13 249** anciennes boutiques aujourd'hui occupées par d'autres activités (dont bureaux/cabinets médicaux) : **pas un nombre de bureaux vacants**. [Jeu BDCOM](https://www.apur.org/fr/open-data-cartes/open-data/base-donnees-commerces-parisiens) : 2017/2020/2023, licence ODbL indiquée pour la base ouverte ; vérifier les droits de réutilisation de chaque fichier/rapport avant redistribution.

Ne jamais additionner Insee et LOVAC (champs résidentiels partiellement recouvrants) ni ajouter les locaux Apur aux logements. Même deux décomptes de locaux distincts ne sont pas nécessairement sommables si leur couverture se recoupe. Aucun taux territorial appliqué au bâtiment.

## Mise à jour audit vérifié des locaux non résidentiels (PR #35)

**Attention à la définition « vacant »** : BDCOM 2023 utilise `type='V'` pour **7 495 locaux vacants hors travaux (AA101) et 1 565 en travaux (AA102)**, soit **9 060** dans le service de données contre 9 059 dans la note Apur (écart de 1 inexpliqué). Ces deux statuts ne doivent plus être confondus dans les classements. Une lecture à 20 arrondissements est disponible sous forme de **statistiques agrégées uniquement**, sans coordonnées ni adresses. Le dénominateur est le parc des locaux BDCOM recensés (83 154), pas les bureaux ou logements de Paris. La ligne de référence du tableau précédent (9 059) représente **le chiffre éditorial incluant des travaux**, pas un décompte de 9 059 locaux vacants hors travaux. Voir [audit complet](bdcom-open-audit-20261017.md).

**Bureaux** : environ **1,5 million de m²** d'offre immédiatement disponible à Paris intra-muros au 30/06/2026 (Colliers 1,542 million, Cushman & Wakefield ≈1,5 million) ; **offre locative, non capacité d'hébergement**. Incohérence entre Colliers T1 (795 000 m²) et T2 (1,542 million), interdiction de tracer une courbe T1→T2 tant que les définitions ne sont pas éclaircies. Distinction **offre en m² / nombre de bureaux / vacance réelle / adaptabilité** maintenue.

## Cadre de faisabilité avant tout scénario d'accueil

- [Insee : logement vacant](https://www.insee.fr/fr/metadonnees/definition/c1059) inclut les logements vétustes : aucune preuve d'habitabilité dans le décompte.
- [Service-Public : changement de destination des bureaux/commerces en logements](https://www.service-public.fr/particuliers/vosdroits/F2416) : PLU, déclaration préalable/permis selon travaux, autorisations d'autres titulaires de droits selon le cas.
- [Service-Public : logement décent](https://www.service-public.fr/particuliers/vosdroits/F2042) : sécurité, ventilation, éclairage, équipements, etc. Règles du logement locatif **non assimilables directement** au cadre juridique d'un accueil temporaire/collectif ; expertise spécifique requise.

## Suite priorisée et réversible

1. Auditer l'open data BDCOM réelle : champs, types de vacance, en travaux, dates, licence, géographie, et possibilité de produire une **statistique agrégée non identifiante**.
2. Rechercher des bureaux réellement vacants à **Paris intra-muros** : source fiable, unité **m²** vs **nombre**, dates, périmètre (pas Île-de-France substituée), offre immédiate vs taux de vacance, licence.
3. Étudier la littérature sur conversions bureaux → logements / accueil temporaire et, en cas de source licite, les exigences de sécurité, coûts et délais. **Pas de nombre de places inventé** à partir des seuls m².
4. Aucun inventaire d'adresses/propriétaires de logements vacants ni join IRIS→bâtiment ; contrôle juridique avant toute donnée fine.

L'histoire du bâti IGN/Apur reste distincte des deux études de vacance et réemploi.

### Recette de la PR #34 et état GitHub (17/10/2026)
Code `5d4cde688476c207fb1cd3a5a2aeb118a4e0e60e` : **102/102 tests JavaScript**, **99/99 tests Python** depuis le venv du VPS, `git diff --check` sans anomalie, clone éphémère sans changements locaux. **Chromium réel** (serveur statique local) : 3 indicateurs indépendants, 4 scénarios qualitatifs, navigation depuis index / évolution / LOVAC validée ; desktop 1440×900 sans débordement, mobile simulé 390×844 sans débordement (tableau défilant à l'intérieur), aucune erreur JavaScript applicative de la nouvelle page. Aucune source brute confidentielle. PR #34 reste en brouillon ; **aucune fusion ni déploiement**. Avant reprise : vérifier les HEAD et les locks, puis auditer la donnée BDCOM et les sources de vacance de bureaux Paris.
