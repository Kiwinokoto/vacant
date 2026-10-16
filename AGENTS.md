# Instructions de contribution à VACANT

1. Lire README.md, docs/sources.md, docs/architecture.md et docs/handoff.md avant modification.
2. GitHub fait autorité : vérifier HEAD, branches, PR ouvertes et protections avant tout commit. Ne pas écraser de travail local/agent ; réutiliser les éventuels locks/leases AgentCTL.
3. Le dépôt est public : ne publier **aucune** donnée nominative ou individuelle LOVAC, même sous forme d'« échantillon ».
4. Toute couche doit indiquer source exacte, licence, millésime, date d'extraction, transformation, précision géographique, mesure et incertitude. Pas de jointure spatiale qui attribue la vacance d'un IRIS à un bâtiment.
5. Un volume bâti de Paris Data n'est pas nécessairement un bâtiment entier ; H_ET_MAX = nombre d'étages au-dessus du sol, pas mètres ; D_CRE = date de création de la fiche, pas construction.
6. Avant activation UI d'une couche, valider champs réels, géométrie, couverture, unité, chaîne de téléchargement, attribution, ruptures de séries et licences des dérivés.
7. Petits commits sur dev/*, tests locaux, PR, pas de déploiement automatique ni de promotion main sans revue de la portée. Mettre à jour docs/handoff.md.
