# Teknisk bilaga: testskript, schema och exempel

Bilaga till [privacyvalidering.md](privacyvalidering.md). Dataschema, exempeldata och notebook-referenser. Bakgrund och revisionsprocess beskrivs i huvuddokumentet.

## Påstående: Explicita IP-adresser existerar inte i TAPIR Core dataset

Undantag är domännamn som innehåller IP-adresser, vilket ligger utanför TAPIRs kontroll och ansvar.

Exempel på sådana domännamn:

- `4.4.8.8.in-addr.arpa`
- `4.3.3.7.0.7.3.0.e.2.a.8.0.0.0.0.0.0.0.0.3.a.5.8.8.b.d.0.1.0.0.2.ip6.arpa`

Andra aktörer kan koda IP-adresser eller andra identifierare i domännamn/frågan, vilket ligger utanför DNS TAPIRs databehandling. Tillgängliggörandet av DNS-frågor för analys innebär bland annat att kunna hitta dessa typer av domännamn för rapportering av läckage av personlig data.

Exempel: spamhouse-tjänsten kodar IP-tjänster. Telefonnummer kan kodas i domännamn (t.ex. enum, gotanet). En aktör kan även base64-koda IP-adress + fråga.

**Validering**:

- Dataschemat inklusive datatyper (se nedan)
- Utdrag dataset Core 5-min-aggregat (se nedan)
- Utdrag dataset Core 1-min aggregat, [Samples av parquet-filer (1-minutersaggregat)](samples/)
- Utdraget som CSV (exkl HLL) för egen analys, vid förfrågan
- Publikt tillgänglig notebook med kod-exempel för att presentera dataschemat: [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Publikt tillgänglig notebook med kod-exempel för att söka efter IP-adress (IPv4, IPv6): [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Notebooks kan exekveras mot verklig datakälla (under förutsättning att behörigheter finns)

### Schema aggregates

I framtiden, när det för privata aktörer finns en konfiguration för att skicka med IP-adresser, kommer det också synas i schemat vilken konfiguration Edge har.

Schemat är formatterat enligt PySpark output och hämtas genom en fråga mot 5-minutershistogram i TAPIR Core Delta-tabeller. 

``` 
delta_db_path = "s3a://<path>/type=delta/wk_histogram_5m"
delta_table = DeltaTable.forPath(spark, delta_db_path)
df0 = delta_table.toDF()
df0.printSchema()

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

En verklig IP-adress lagras som en sträng eller ett binärfält. Det enda binärfält som existerar i datasetet är HLL-sketcher (se ovan). HLL-sketcher kan per definition inte innehålla explicita IP-adresser. Referens: <https://datasketches.apache.org/docs/HLL/HllSketches.html>

### Verifiera att inga explicita IP-adresser finns i TAPIR Core

IPv4-mönster utökas vid behov. Todo: Utöka med oktalprefix IPv4 `0.14`.

![img35](img/img35.png)

![img22](img/img22.png)

![img5](img/5.png)

IPv6-mönster utökas vid behov, alla IPv6-format täcks inte i detta exempel.
(todo: konvertera först till upper case för enklare pattern)

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

Källa ipv6-format: [ ipv6-representation](https://www.networkacademy.io/ccna/ipv6/ipv6-address-representation)
## Påstående: Implicita IP-adresser existerar inte i TAPIR Core dataset

IP-adresser krypteras före HLL-beräkning. Detta gör att det inte går att härleda en IP-adress från en HLL-sketch och sketchen är alltså är irreversibel.
#### Problemet utan kryptering:
Utan kryptering lämnas spår av IP-adresser i HLL-sketchen som för vissa IP-adresser kan vara igenkännbara. Vissa IP-adresser kan hashas till "många 0:or i mitten". Vilka IP-adresser som får detta kan räknas ut på förhand, givet att man känner till hur HLL:en är uppbyggd. Med rainbow table går det då att återskapa IP-adress. För att göra detta behöver kunskap finnas om konfigurationsparametrar till HLL-strukturen; det går även att göra kvalificerade gissningar.

Simulering och beräkningar av problemet: [/becoming-uniquely-identifiable-in-a-hyperloglog-sketch](/becoming-uniquely-identifiable-in-a-hyperloglog-sketch)
### Validering

- Verifiera att kryptering faktiskt sker före HLL-inmatning
- Verifiera att resultatet är irreversibelt
#### Verifiera att kryptering faktiskt sker före HLL-inmatning
1. **Källkodsgranskning i EDM**. Dataflödet från `client_ip` -> HLL-insert. Kontrollera att raw IP aldrig når `hll.add()`.  Kodrad: ... 
2. **Enhetstest i EDM-repo** (finns?)
3. Test som verifierar att EDM inte aggregerar om krypteringsnyckeln saknas. (Annars kan en felkonfigurerad Edge tyst publicera oskyddade sketcher.)

#### Verifiera att resultatet är irreversibelt
**Rainbow-table-simulering med och utan kryptering**. Fortsätt befintligt arbete i becoming-uniquely-identifiable-in-a-hyperloglog-sketch. 

- _Utan kryptering_: enumerera IP-rymd (t.ex. hela /24 eller /16), beräkna HLL-bidrag, mät hur många IP-adresser som ger unika register-signaturer. Detta är baseline-hotet.
- _Med kryptering (samma seed)_: repetera. Förväntat resultat: 

Mätvärde: andel IP-adresser i subnätet vars register-avtryck är särskiljbart, före vs efter kryptering.
#### Anteckningar
Med den kryptering av IP-adress som sker före HLL-beräkning uppmanas Edge-operatörer att använda samma "hemlighet" (seed) på alla Edge hos en operatör, för att kunna merga HLL-sketcher mellan dessa och beräkna antal klienter utan dubbletter.

## Påstående: Sekund-tidsstämplar existerar inte i TAPIR Core dataset

Tidsstämplar i TAPIR Core avrundas eller sammanställs i intervaller om 1 minut. Den enda sekund-tidsstämpeln som existerar är i metadatat Core, vilket visar när minut-intervallet startar. Detta gör att en extern logg med sekundupplösning (t.ex. en webbservers `access_log`) inte deterministiskt kan matchas 1-till-1 mot en enskild TAPIR-observation hos en tillräckligt stor operatör. 

**Vidareutveckling för mindre operatörer**
Skapa en Aggregations-Edge.

### Motivering: Frånvaro av sekund-tidsstämpel som anonymiseringsmetod

Att TAPIR Core saknar sekundupplösning på tidsstämplar är ett aktivt anonymiseringsval. 
Det uppfyller GDPR:s tröskel för anonym data (skäl 26: "extremt osannolikt att identifiera"). 

**1. RFC 9076 - DNS Privacy Considerations.**
Identifierar granulariteten på tidsstämplar och aggregering av trafik som centrala faktorer för om DNS-data kan användas för spårning av enskilda klienter. Aggregerad data med grov tidsupplösning listas som en av de åtgärder som minskar risken. Källa: <https://www.rfc-editor.org/info/rfc9076>

**2. RFC 6973 - Privacy Considerations for Internet Protocols (IAB).**
Definierar hotmodeller: *korrelation* (kombinera datamängder från olika källor för att härleda information om en individ) och *länkbarhet* (avgöra om två observationer avser samma individ). 

En sekund-tidsstämpel på en DNS-fråga är ett typiskt korrelationsattribut som kan matchas 1-till-1 mot t.ex. en webbservers `access_log`. En minut-tidsstämpel delas av alla klienter som ställt frågor på samma domän under samma minut, vilket bryter den 1-till-1-relationen. Källa: <https://www.rfc-editor.org/info/rfc6973>

**3. k-anonymitet (Sweeney, 2002) - kvantitativ grund.**
För att en observation ska vara anonym enligt k-anonymitetsmodellen ska varje kombination av kvasi-identifierare, här `<Well Known-domän, minut, creator>`  delas av minst *k* distinkta individer. Om *k* ≥ 2 kan en extern sekundupplöst logg inte deterministiskt länkas till en enskild TAPIR-observation; ju högre *k*, desto lägre sannolikhet för korrekt länkning. 

Källa: L. Sweeney, *k-anonymity: A model for protecting privacy*, International Journal of Uncertainty, Fuzziness and Knowledge-Based Systems, 10(5), 2002.

**4. Mätning på TAPIR Core operatörsdata**
Uppmät *k* för befintliga TAPIR-Edge-installationer. Förslag:

- För varje `<Well Known-domän, minut, creator>`-histogram i ett representativt urval: rapportera fördelningen av uppskattat antal distinkta klienter, k. andel histogram med k < 5, k<10, mm
- Publicera notebook: `samples/kAnonymityCheck.ipynb` (todo).

**Kvarstående hot och åtgärder.**

- Små operatörer där *k* == 1 för många histogram: hanteras via planerad Aggregations-Edge.
- Well Known-domäner med extrem popularitetsobalans (frågas nästan bara av en typ av klient): hanteras via Well Known-granskning, se separat påstående.

### Validering

- Exempel på dataschemat inklusive datatyper (se ovan)
- Utdrag dataset Core (1-min aggregat, parquet-format) [samples](samples/)
- Utdraget av 1-min-aggregat som CSV (exkl HLL) för egen analys, vid förfrågan
- Publikt tillgänglig notebook med kod-exempel för att presentera dataschemat: [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb)
- Publikt tillgänglig notebook med kod-exempel för att söka efter sekund-tidsstämplar [samples/PrivacyCheck.ipynb](samples/PrivacyCheck.ipynb) 
- k-anonymitetsmätning `samples/kAnonymityCheck.ipynb` (todo)


Todo: Distinct. Se flera minuter + creator.

Tidsstämpeln som syns i 1-minutersaggregat är när aggregatet publicerades till TAPIR Core. Samma minut - samma Edge. (förslag: EDM forcerar tidsstämpeln till `YYYY-MM-DD-HH-MM` för enhetlighet, vill vi det?)

Tidsstämplar skickas binärkodade enligt parquet-tidsstämpelformat.

![img7](img/7.png)

- Notebook finns tillgänglig publikt med sample parquet-fil: [samples/ViewParquet.ipynb](samples/ViewParquet.ipynb)
- Utökas med fler verifieringar vid behov.

![img8](img/8.png)

## Påstående: TAPIR Core dataset innehåller endast domäner från Well Known-listan

Upplösningen på datasetet i TAPIR Core är låg — alla frågor finns inte i datasetet.

Antal domäner i den i installationspaketet föreslagna Well Known-listan är: minst x.
Antal nya domäner (dvs ej i Well Known och ej i 1-minutersaggregat) som observeras under en minut är: y för `<operatör>`.

En stor mängd domänförfrågningar finns alltså inte i 1-minutersaggregaten.

**Referenser, omvärld**
I analyser av beteendeavtryck ("fingerprints") på DNS-frågor där individer har identifierats, har de dataset som används en betydligt högre tidsupplösning än DNS TAPIR — ofta på sekundnivå. Där ingår också alla DNS-förfrågningar/domänuppslag i datasetet som analyseras, till skillnad från den lägre upplösningen i TAPIR Core som enbart innehåller Well Known-domäner.

Exempel: `A_User_DNS_Fingerprint_Dataset.pdf`, Zápotocký et al.

Well Known-filen styr vilka domännamn som är tillgängliga i aggregaten för analys.
För att bekräfta att det inte förekommer unika domännamn i Well Known gör projektet regelbundna kontroller av vilka domäner som finns i Well Known-filen.

### Validering

- Jämför antal domäner i Well Known med antal nya observerade domäner.
- Undersök att aktuell Well Known-fil används: [https://dnstapir.github.io/techdocs/postinstall.html#maintaining-the-well-known-domains-filter](https://dnstapir.github.io/techdocs/postinstall.html#maintaining-the-well-known-domains-filter)
- Publicera Well Known-filen så att operatörer och allmänheten kan slå upp ovanliga eller integritetskänsliga domännamn. Publicera dokumentation och kod för att undersöka Well Known efter sin adress.

#### Anteckningar

- Verifiera att alla kända contentnätverk (CDN) är inlagda på rätt sätt i Well Known. Kanske kan TAPIR publicera listan på kända CDN:er och annonsnätverk och logiken för hur de hanteras med wildcard (?)

## Påstående: Ovanliga domän-förfrågningar existerar en gång i TAPIR Core

En unik domän är en domän som bara får frågor från en eller ett fåtal användare. Det kan bero på att domänen har få besökare (t.ex. en personlig webbsida) eller att domänen används för att spåra individer genom unika sub-domäner (exempelvis annonstjänster).

Att unika domäner blir en enda observation av ny domän är inte ett problem eftersom ingen information följer med i observationsdatat som kan användas för identifiering.

Exempel:

- `87rxrdobfl4goostvxilqmxnm36bmqou.ad.example.com`
- `nissetuta.familjenswebsida.exempel.se`
- Domäner som inte används längre

Event för ny domän lagras separat från aggregaten, alltså inte i 1-minuters-aggregaten. Event lagras en gång per Edge som sett frågan en gång.

- domännamn
- creator (TAPIR Edge)
- tidsstämpel när eventet publicerades

### Validering

- Koden för hur EDM publicerar events: [github.com/dnstapir/edm...](github.com/dnstapir/edm...)
- Undersök dataset efter domäner med fåtal frågor och besluta om den ska uteslutas ur Well Known och endast hanteras som event. Publicera notebook för att hitta dessa domäner.
- Senare: Publicera ett urval av 5-minuters-aggregat publikt, med regelbundenhet.
- Eventuellt: Visa sample från NATS key-value store.
- Eventuellt: Kod-exempel för att leta efter ett eller många kända unika domännamn i TAPIR Core Dataset.

## Påstående: Unikt identifierbara DNS-frågemönster i TAPIR Core aggregat är extremt osannolikt

Se: [privacyvalidering-patterns.md](privacyvalidering-patterns.md)

## Datalagring

### TAPIR Core Dataset - 1 minuters-aggregat

### TAPIR Core Events och observationer
