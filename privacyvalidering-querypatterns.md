# Påstående: Unikt identifierbara dns-fråge-mönster i TAPIR Core aggregat är extremt osannolikt

---- UTKAST ----

## Hitta frågemönster utifrån ovanlig HLL-representation

HyperLogLog-sketcher kan innehålla ovanliga representationer. Sannolikheten är ungefär 2% på 100 000 klienter att en klient får en representation i HLL-sketchen som är såpass ovanlig att det skulle kunna gå att hitta frågemönster baserat på den representationen. Se avsnittet "Implicita IP-adresser" i teknisk bilaga samt beräkning här: [privacyvalidering-teknisk-bilaga.md](privacyvalidering-teknisk-bilaga.md)

Personen kan inte identifieras med bevisbarhet när IP-adresser krypteras innan beräkning av HLL och bryter alltså inte mot GDPR.  Se [teknisk bilaga](privacyvalidering-teknisk-bilaga.md)
 för information om hur IP-adresser krypteras på resolvernivå i DNS TAPIR Edge.  

Däremot väljer DNS TAPIR att ha en högre integritetsnivå än GDPR och avser  att ta bort möjligheten till att hitta frågemönster genom ytterligare anonymiseringsåtgärder.

För att hitta ett frågemönster tillhörande en eller ett fåtal individer så skulle analysen ungefär se ut:

- Hitta ovanliga representationer i HLL-sketcherna under vald tidsrymd.
- Ta en sådan representation och hitta alla domäner/HLL-sketcher som denne representation ingår i, inom tidsrymden
- Analysera mönstret och korrelera med annan känd information för att göra antaganden om vilken person detta skulle kunna vara

Vissa frågemönster är ointressanta, medan andra mönster potentiellt skulle kunna misstänkas tillhöra en person.

Exempel på ovanligt frågemönster:

- intranet.min-enskilda-firma.exempel.se
- min-hemby.exempel.se
- kanslig-forening-i-hembyn.exempel.se

## DNS TAPIR anonymiseringsåtgärder

För att göra det omöjligt att hitta ett ovanligt frågemönster så planeras ett ytterligare steg innan beräkning av HLL-sketch: 

- Vid kryptering av IP-adressen på TAPIR Edge (resolvern) så används även den frågade domänen som parameter till krypteringen.  Det gör att samma klient får olika krypterade hashar innan beräkning.
- Konsekvens för analysförmåga blir att det inte går att uppskatta (HLL-merge) antal klienter mellan olika domäner
