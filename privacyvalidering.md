# Validering av personlig integritet i TAPIR Core dataset

---DETTA ÄR ETT UTKAST. WORK IN PROGRESS---

## Bakgrund

- GDPR kräver inte att det ska vara absolut omöjligt att kunna identifiera en individ, men möjligheten till identifiering behöver vara extremt osannolik för att datan ska klassas som anonym.
- Anonymiserade uppgifter anses inte längre vara personuppgifter och faller därmed utanför GDPR:s tillämpningsområde.
- Anonymiseringen ska vara irreversibel.
- Det finns tre huvudrisker för avidentifiering: särskiljbarhet, länkbarhet samt inferens

DNS TAPIR anonymiserar data redan på DNS-operatörsnivå. DNS TAPIR behandlar inte några personuppgifter, utan får tillgång till anonymiserade datapaket. I DNS TAPIR-projektet genomförs anonymiseringen genom en kombination av sekvensbrytning, anonymiseringstekniker och successiv aggregering.

Uppskattning av unika domän-förfrågningar görs med algoritmen HyperLogLog (HLL) utan att lagra hela datasetet

## Påstående: Explicita IP-adresser existerar inte i TAPIR Core dataset

IP-adresser är en av de primära och indirekta identifierarna i en DNS-förfrågan
Inga explicita IP-adresser existerar i TAPIR Core dataset, med undantag för sådana som kan förekomma i domännamn vilket är utanför TAPIRs kontroll och kan inte kopplas till användare

Exempel på sådana domännamn och tjänster som använder dessa är:
4.4.8.8.in-addr.arpa
4.3.3.7.0.7.3.0.e.2.a.8.0.0.0.0.0.0.0.0.3.a.5.8.8.b.d.0.1.0.0.2.ip6.arpa

Exempel: Andra kan använda/koda IP-adress till domännamnet/frågan
Om ip-liknande data som finns i frågematerialet, utanför 

Exempel: spamhouse-tjänsten, kodar ip-tjänster
Exempel: enum (telefonnummer), gotanet...

**Validering**:

- Dataschemat inklusive datatyper
- Utdrag dataset Core 5-min-aggregat 
- Utdrag dataset Core 1-min aggregat,[Samples av parquet-filer (1-minutersaggregat)](samples/).
- Utdraget som CSV (exkl HLL) för egen analys, vid förfrågan
- Publikt tillgänglig notebook med kod-exempel för att presentera dataschemat.  [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Publikt tillgänglig notebook med kod-exempel för att söka efter ip-adress (IPv4, IPv6) [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Notebooks kan exekveras mot verklig datakälla (under förutsättning att behörigheter finns)

### Schema aggregates

```text
root
 |-- date: date (nullable = true)
 |-- creator: string (nullable = true)
 |-- label0: string (nullable = true)
 |-- label1: string (nullable = true)
 |-- label2: string (nullable = true)
 |-- label3: string (nullable = true)
 |-- label4: string (nullable = true)
 |-- label5: string (nullable = true)
 |-- label6: string (nullable = true)
 |-- label7: string (nullable = true)
 |-- label8: string (nullable = true)
 |-- label9: string (nullable = true)
 |-- hour: byte (nullable = true)
 |-- minute: byte (nullable = true)
 |-- tagstring: string (nullable = true)
 |-- fqdn: string (nullable = true)
 |-- r_fqdn: string (nullable = true)
 |-- idn_fqdn: string (nullable = true)
 |-- a_count: long (nullable = true)
 |-- aaaa_count: long (nullable = true)
 |-- mx_count: long (nullable = true)
 |-- ns_count: long (nullable = true)
 |-- other_type_count: long (nullable = true)
 |-- non_in_count: long (nullable = true)
 |-- ok_count: long (nullable = true)
 |-- nx_count: long (nullable = true)
 |-- fail_count: long (nullable = true)
 |-- other_rcode_count: long (nullable = true)
 |-- deltas: array (nullable = true)
 |    |-- element: integer (containsNull = true)
 |-- ok: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- nx: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- fail: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- other_rcode: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- other_type: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- non_in: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- v4_clients: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- v6_clients: array (nullable = true)
 |    |-- element: long (containsNull = true)
 |-- v4clients_hll: binary (nullable = true)
 |-- v6clients_hll: binary (nullable = true)
 |-- v4clients_avg: double (nullable = true)
 |-- v6clients_avg: double (nullable = true)
 |-- v4client_count_hll: integer (nullable = true)
 |-- v6client_count_hll: integer (nullable = true)
```

Utdrag 5-minuters-aggregat.

![img1](img/1.png)

![img1](img/2.png)

![img1](img/3.png)

![img1](img/4.png)

En verklig IP-adress lagras som en sträng eller ett binärfält. Det enda binärfält som existerar i datasetet är HLL-sketcher (se ovan). HLL-sketcher kan per definition inte innehålla explicita IP-adresser. Referens:  https://datasketches.apache.org/docs/HLL/HllSketches.html

(todo: nämna spamhouse-exemplet?)
någon annan kan ta ip-adressen + koda med byte64 - fråga efter) 
### Verifiera att inga explicita IP-adresser finns i TAPIR Core

Todo: Beskriv samplet.
Todo: Hur ofta bör detta köras? 1 ggn/mån?  En minut/Edge. 

Kom ihåg: När det finns en konfig för att skicka med IP-adresser, behöver också synas vilken konfig Edge har. 
 
ipv4-mönster utökas vid behov.
oktalprefix ipv4 0.14

![img5](img/5.png)

ipv6_pattern utökas vid behov, exakt alla ipv6-format täcks inte i detta exempel.
(konvertera upper case)
```python
ipv6_pattern = (
    r"([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}|"
    r"([0-9a-fA-F]{1,4}:){1,7}:|"
    r"([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|"
    r"([0-9a-fA-F]{1,4}:){1,5}(:[0-9a-fA-F]{1,4}){1,2}|"
    r"([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|"
    r"([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|"
    r"([0-9a-fA-F]{1,4}:){1,2}(:[0-9a-fA-F]{1,4}){1,5}|"
    r"[0-9a-fA-F]{1,4}:(:[0-9a-fA-F]{1,4}){1,6}|"
    r":(:[0-9a-fA-F]{1,4}){1,7}|"
    r"::"
)

ipv6_nibble_pattern = r"[0-9a-fA-F](\.[0-9a-fA-F]){31}"
```

![img6](img/6.png)

## Påstående: Implicita IP-adresser existerar inte i TAPIR Core dataset

Fråga: Är det här ett GDPR-problem eller inte? 

För att inga implicita IP-adresser ska gå att identifiera i HLL-sketch så implementeras kryptering av IP-adress med t.ex AES före beräkning av HLL-sketch. Då går inte att reversera till IP-adresser.

(uppmaning att använda samma "hemlighet" seed på alla Edge hos en operatör för att kunna merga HLL-sketcher - beräkna antal klienter utan dubbletter)

Utan kryptering lämnas spår av IP-adresser i HLL-sketchen som  för vissa IP-adresser kan vara igenkännbara. Hashas till "många 0:or i mitten". Vilka IP-adresser detta är kan räknas ut på förhand, givet att man känner till hur HLL:en är uppbyggd.  (Med rainbow table går det att återskapa IP-adress). Behöver känna till konfigurationsparametrar till HLL-strukturen, går att göra kvalificerade gissningar. 

Simulering och beräkningar finns här:
[/becoming-uniquely-identifiable-in-a-hyperloglog-sketch](/becoming-uniquely-identifiable-in-a-hyperloglog-sketch)x

**Validering**
- Källkodsgranskning i EDM. Repo (bilaga)


## Påstående:  Sekund-tidsstämplar existerar inte i TAPIR Core dataset 

- Sekundtidsstämplar ... RFC... Matcha tidsstämplar
- 
Tidsstämplar kan utgöra en identifieringsrisk om de är exakta, eftersom de potentiellt kan matchas mot annan logg-data för att spåra en individs aktivitet. Tidsstämplar i TAPIR Core avrundas eller sammanställs i intervaller om 1 minut.

Webblogg-matchning med 1 minuts aggregat blir svårt på en "större" operatör. Större = ... 
Liten mängd användare lättare att matcha. 
för små operatörer: skapa en Aggregations-Edge

Baserat på .... minutaggregat i kombination med att datasetet endast innehåller domäner i Well Known så är identifiering av individuellt beteende 

Låg upplösning i TAPIR Core.
Jämförelsevis DNS FIngerprinting-paper är upplösningen mycket högre.. 

Vilka kända attacker finns? Vilken upplösning krävs?

I TAPIR Core existerar endast 1-minuters-aggregat

Den enda sekund-tidsstämpeln som existerar är i metadatat Core, vilket visar när minut-intervallet startar.

### Validering

- Exempel på dataschemat inklusive datatyper (se ovan)
- Utdrag dataset Core (1-min aggregat, parquet-format) [samples](samples/)
- Utdraget av 1-min-aggregat som CSV (exkl HLL) för egen analys, vid förfrågan
- Publikt tillgänglig notebook med kod-exempel för att presentera dataschemat.  [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Publikt tillgänglig notebook med kod-exempel för att söka efter ip-adress (IPv4, IPv6) [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Notebooks kan exekveras mot verklig datakälla (under förutsättning att behörigheter finns) eller egen installation.

**Utdrag 1-min aggregat**

Todo: Distinct. Se flera minuter + creator
(förslag - EDM forcerar tidsstämpeln till YYYY-MM-DD-HH-MM för enhetlighet)

Formatet i parquet-filen... Tidsstämplar skickas binärkodade enligt parquet-stämplar. 

Tidsstämpeln är när aggregatet publicerades till TAPIR Core. Samma minut - samma Edge. Samma tidsstämpel på varje rad (!)

![img7](img/7.png)

- Notebook finns tillgänlig publikt med sample parquet-fil  [samples/ViewParquet.ipynb](samples/ViewParquet.ipynb)
- Utökas med fler verifieringar vid behov.

![img8](img/8.png)


## Påstående: Unika domän-förfrågningar existerar en gång i TAPIR Core

Hur kopplas detta till privacy-problemet?

 Tidigare osedda domäner,  genererar en observation av ny domän i TAPIR Core. Dessa kan potentiellt användas för att . TAPIR Core aggregat innehåller endast domäner som existerar i Well Known. 

En unik domän är en domän som bara får frågor från en eller ett fåtal användare. Detta kan bero på att domänen har få besökare, t.ex en personlig websida, eller att domänen används för att spåra individer genom unika subdomäner. Exempelvis annonstjänster kan använda sig av det. 

Att unika domäner blir en observation av ny domän är inte ett problem...

Exempel: 87rxrdobfl4goostvxilqmxnm36bmqou.advertising.example.com
Exempel: nissetuta.familjenswebsida.exempel.se

Exempel:  domäner som inte används längre 

Eventen lagras separat från aggregaten, en gång per resolver som sett frågan en gång. Samt enda information:
- domännamn
- creator (TAPIR Edge)
- Tidsstämpel när eventet publicerades 

Det gör att dessa unika domäner inte kan användas för att göra identifierande analys.
Dessa lagras alltså inte i 1-minuters-aggregaten (parquet-filerna), och existerar inte i datasetet.

### Validering

Det är Well Known-filen som styr vilka domännamn som är tillgängliga i aggregaten för analys. 
För att bekräfta att det inte förekommer unika domännamn i Well Known gör projektet regelbundna kontroller av vilka domäner som finns i Well Known-filen. 

- Undersök att aktuell Well Known-fil används: https://dnstapir.github.io/techdocs/postinstall.html#maintaining-the-well-known-domains-filter
- Verifiera att alla kända contentnätverk (CDN) är inlagda på rätt sätt i Well Known. Kanske kan TAPIR publicera listan på kända CDNS och annonsnätverk och logiken för hur de hanteras med wildcard (?)
- Publicera Well Known-filen så att operatörer och allmänheten kan slå upp ovanliga eller integritetskänsliga domännamn.  Publicera dokumentation och kod för att undersöka Well Known efter sin adress.
- Undersök dataset efter domäner med fåtal frågor och besluta om den ska uteslutas ur Well Known och endast hanteras som event. Publicera notebook för att hitta dessa domäner. 
- Granskande analytiker kan erbjudas konton
- Publicera 5-minuters-aggregat publikt
- 


https://dnstapir.github.io/techdocs/postinstall.html



- Koden för hur EDM publicerar events finns här: [github.com/dnstapir/edm...](github.com/dnstapir/edm...)  
- Eventuellt: Visa sample från NATS key-value store.
- Eventuellt: Kod-exempel för att leta efter ett eller många kända unika domännamn i TAPIR Core Dataset
- 

## Påstående: Unikt identifierbara dns-fråge-mönster i TAPIR Core aggregat är extremt osannolikt

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
