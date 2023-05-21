SELECT maaltijden.recept_naam, Ingredienten.ingredient, Ingredienten.hoeveelheid, Ingredienten.eenheid
FROM maaltijden
INNER JOIN Ingredienten
ON maaltijden.ID = Ingredienten.ID_maaltijden
ORDER BY Ingredienten.ingredient ASC;
