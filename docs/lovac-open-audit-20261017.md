# VACANT — Audit LOVAC 2020–2026 (17 octobre 2026)

Source publique officielle : https://www.data.gouv.fr/datasets/61816c6e23197bb34835228e (DGALN/Cerema, Licence Ouverte 2.0).

Trois CSV publics (communes, départements, dictionnaire) ont été téléchargés sur le VPS personnel et vérifiés par SHA-256. Le jeu comporte vingt lignes parisiennes, codes 75101–75120, sans suppression statistique pour leurs indicateurs. Leurs sommes correspondent exactement à la ligne du département 75.

**Attention aux ruptures de méthode GMBI dès le millésime 2024, puis changement de sélection en 2025.** Les grandes variations ne sont pas des flux de logements libérés. LOVAC couvre le parc privé fiscal ; le RP Insee le parc total. Les dates de référence diffèrent aussi des millésimes : 2026 correspond au 01/01/2025 ; la vacance longue 2023 au 01/01/2022. Ne pas construire de taux de vacance 2026 à partir de `ff_pp_total_25`, date 01/01/2024.
