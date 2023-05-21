SELECT Ingredienten.ingredient, SUM(Ingredienten.hoeveelheid) AS total_hoeveelheid, Ingredienten.eenheid 
FROM maaltijden 
INNER JOIN Ingredienten ON maaltijden.ID = Ingredienten.ID_maaltijden 
WHERE maaltijden.recept_naam IN ('Fusilli met gehakt en mozarella', 'Spaghetti alla carbonara', 'Gehaktbrood met boontjes en aardappelen', 'Hete bliksem', 'Parmentier van bloemkool, aardapappeln en kippengehakt', 'Lasagne', 'Macaroni met ham en kaas')
GROUP BY Ingredienten.ingredient, Ingredienten.eenheid
ORDER BY Ingredienten.ingredient ASC;
