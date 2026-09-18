# Påstående: Unikt identifierbara dns-fråge-mönster i TAPIR Core aggregat är extremt osannolikt

---- WORK IN PROGRESS ----

**Vad är problemet**

**Hur stort är problemet?**

**Vilka lösningar finns?**

**Är operatören GDPR-compliant även innan detta eventuella problem är löst?**  
Dvs kan operatören gå i produktion med TAPIR som TAPIR:en fungerar

Går det att hitta en frågeställare, en avsändaridentitet, som skulle kunna vara t.ex ett hushåll i HLL-sketchen? Och utifrån den avsändaridentiteten följa ett mönster t.ex:  internetstiftelsen.se -> gnestafågelskådare -> gnestalillaförskola -> skobesgnesta?

Förutsätter att de domänerna finns i wellknown +  otur med den hashade adressen, HLL-sketchen

För att en domän ska finnas i aggregat behöver den finnas i well known-listan som är baserad på Open Page Rank och liknande publika källor.  
(Well-known-filen finns här: [github.com/dnstapir/...](github.com/dnstapir/...)  Edge-operatören kan ersätta med valfri.)

Även om en unikt identitiferbar domän finns i Core dataset, så går det inte att identifera individ. För att det ska hända så behöver en kombination av unikt utseende på hll-sketchen plus unikt identiferbar domän existera. 1 person med unikt utseende på hll-sketchen frågar efter samma unika domän regelbundet..

**Förändringar som planeras, ytterligare säkerhetsåtgärd så att det inte ska kunna ske:**
Dela upp Well Known Domains i:

- Well well known.  (google.com, apple.com osv)
- Less well known. Annan metodik för HLL-sketchen, går då inte jämföra kardinalitet mellan domäner. HLL-sketchen genereras utifrån IP-adress+domänen

Förslag på ytterligare säkerhetsåtgärder om det skulle anses nödvändigt:

- Endast domäner med x antal förfrågningar kan existera i wellknown.

Varför är det viktigt?

Hantering av longitudinell analys...  ska inte kunna leta upp intressant i aggregaten, kommer inte kunna lägga ihop 1 timme och 5 min.

### Validera

- Vi vill visa operatören att detta är extremt osannolikt, att det inte ett problem för GDPR-compliance och att det är ett avancerat case som vi undersöker för att DNS TAPIR har särskilda egna integritetskrav på datasetet.
- Genomför en membership inference attack (kostar, akademi)
- M visar en PoC på en membership inference attack, 9/9, spela in
- Beräkna sannolikheten att  identifiera en enskild “avsändaridentitet” i HLL-sketcher
- Förtroende byggs upp över tid genom att DNS TAPIR granskar sig själv och med DNS-community och akademin.

**Sannolikhet för att identifiera en ensild användaridentitet**

Sannolikheten har beräknats enligt... och är ...

Simulering och beräkningar finns här:
[/becoming-uniquely-identifiable-in-a-hyperloglog-sketch](/becoming-uniquely-identifiable-in-a-hyperloglog-sketch)x

Frågor:

- Hur stor får sannolikheten vara för ett unikt fingeravtryck? Räcker det med att det är ett ovanligt fingeravtryck?
- Är beräkningarna korrekta, återspeglar det verkligheten?
- Beräkna utifrån hur många kunder en ISP kan ha i sitt nät? x procent kan vara unika … i tal. Är det acceptabel nivå?
- Går det att se ett mönster från den enskilda entiteten
- Beskriv: Hur göra för att hitta en unikt identifierbar frågeställare i HLL-sketch. Ta fram ett frågemönster för denna avsändar-identitet (= Membership inference attack?).
- Är det tillräckligt ovanligt för att anses som osannolikt?

[/privacyvalidering-testscripts.md](/privacyvalidering-testscripts.md)