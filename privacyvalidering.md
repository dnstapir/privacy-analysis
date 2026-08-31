# Grundläggande validering av det aggregerade datasetet i TAPIR Core

--DETTA ÄR ETT UTKAST. WORK IN PROGRESS--

## Bakgrund

- GDPR kräver inte att det ska vara absolut omöjligt att kunna identifiera en individ, men möjligheten till identifiering behöver vara extremt osannolik för att datan ska klassas som anonym.
- Anonymiserade uppgifter anses inte längre vara personuppgifter och faller därmed utanför GDPR:s tillämpningsområde.
- Anonymiseringen ska vara irreversibel.
- Det finns tre huvudrisker för avidentifiering: särskiljbarhet, länkbarhet samt inferens

DNS TAPIR anonymiserar data redan på DNS-operatörsnivå. DNS TAPIR behandlar inte några personuppgifter, utan får tillgång till anonymiserade datapaket. I DNS TAPIR-projektet genomförs anonymiseringen genom en kombination sekvensbrytning, anonymiseringstekniker och successiv aggregering.

Uppskattning av unika domän-förfrågningar görs med algoritmen HyperLogLog (HLL) utan att lagra hela datasetet

## Påstående: Explicita IP-adresser existerar inte i TAPIR Core dataset

IP-adresser är en av de primära och indirekta identifierarna i en DNS-förfrågan

**Validering**:

- Exempel på dataschemat inklusive datatyper
- Utdrag dataset Core (1-min aggregat, parquet-format)
- Utdraget som CSV (exkl HLL) för egen analys
- Publikt tillgänglig notebook med kod-exempel för att presentera dataschemat
- Publikt tillgänglig notebook med kod-exempel för att söka efter ip-adress i strängfält IP-adress (IPv4, IPv6)

**Schema**

Ersätt med parquet-schema



Nedan är ett exempel på 5-minuters-aggregat. Todo: Ersätt med exempel på 1-minuters-aggregat

![](img/dataset_sample_pt1.png)

![](img/dataset_sample_pt2.png)

![](img/dataset_sample_pt3.png)

![](img/dataset_sample_pt4.png)

En verklig IP-adress skulle lagras som en sträng eller ett 32 bytefält (?). De sträng-fält som finns är: creator, fqdn, r_fqdn. Samtliga är domännamn eller resolver-identifierare.

**Schema aggregates**

```
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

Script är tillgänligt på: github.com..... Data-sample fås vid förfrågan i parquet-format, alternativt  tillgång till den faktiska datakällan under förutsättning att behörighet finns. 

**Verifiering av att inga explicita IP-adresser finns i TAPIR Core**

Fråga: Hur stort sample behöver det vara?

![[Pasted image 20260826151631.png]]

![[Pasted image 20260826152118.png]]


## Påstående: Implicita IP-adresser existerar inte i TAPIR Core dataset

Implementering pågår av kryptering med CryptoPAN före hashning
IP-adresser krypteras innan de hashas.

**Validering**
...


## Påstående: Exakta tidsstämplar existerar inte i TAPIR Core dataset

Tidsstämplar kan utgöra en identifieringsrisk om de är exakta, eftersom de potentiellt kan matchas mot annan loggdata för att spåra en individs aktivitet. Tidsstämplar i TAPIR Core avrundas eller sammanställs i intervaller.

I TAPIR Core existerar endast 1-minuters-aggregat, dvs inga exakta tidsstämplar.

För att en exakt tidstämpel ska vara relevant behövs: datum, timme, minut, sekund
Finns sekund-tidsstämpel (i metadatat, när aggregatet togs emot, när intervallet startar)

**Validering**

- Exempel på dataschemat inklusive datatyper (se ovan)
- Utdrag dataset Core (1-min aggregat, parquet-format) (se ovan)
- Utdraget som CSV (exkl HLL) för egen analys
- Publikt tillgänglig notebook med kod-exempel för att presentera dataschemat
- Förslag: Öppen notebook. Ta fram en sample-parquet, sätt upp webserver på Github pages och använd ett enkelt verktyg, exempelvis Hyparquet för att visa schemat och datasample.


## Påstående: Unikt identifierbara domäner, förfrågningar, existerar inte i aggregat som publiceras till TAPIR Core. Unika domäner kan existera som event

Exempel, case:  nisseikatthultsdeviceid.bigtechgiant.com. (tidsstämpel när eventen skickades)
lagras i key-value-store men utan mer information

kodsnutt när EDM publicerar event, länk till koden.

Hur visa att det inte finns unikt identifierbara domäner i aggregaten? 
1 person som frågar efter den regelbundet..

Alla domäner finns publik kunskap om. 
Well Known : Micke publicerar scripten som genererar well known 

För att en domän ska finnas i aggregat behöver den finnas i well known-listan. Baserad på openpagerank och liknande publika källor. Även om en unikt identiferbar domän finns, går det inte att identifera individ. Unikt utseende på hll-sketchen plus unikt identiferbar domän

Titta i well-known-filen
Operatörer kan använda vilken wellknown de vill, inkl alla domäner i världen.
Visa var well-known-filen finns.

Förslag på lösning om det är ett problem: Endast domäner med x antal förfrågningar kan existera i wellknown.

Exempel: En individ har ställt frågan, kan inte korrelera med någon annan.

Unika domäner via events: kalletuta.com  - tar vi emot tidsstämpel? EDM skickar events men ej exakt, fördröjd. tidsstämpel Validering: visa kod. Domänen lagras i NATS/store.

nissatuta.com - sparas en gång att den har setts av en ny creator. vilken creator, tidsstämpel (?)

Visa sample från NATS.

## Påstående: Unikt identifierbara dns-fråge-mönster i TAPIR Core aggregat är extremt osannolikt

**Förändringar som planeras, säkerhetsåtgärd:** 
Dela upp Well Known Domains i: 
- Well well known. 
- Less well known. Annan metodik för HLL-sketchen, går inte jämföra kardinalitet mellan domäner. IP+domänen

Varför är det viktigt? 

Hantering av longitudinell analys...  ska inte kunna leta upp intressant i aggregaten, kommer inte kunna lägga ihop 1 timme och 5 min.

**Validera**
Genomför en membership inference attack (kostar)
Micke visar om en PoC, 9/9, spela in




Går det att hitta en frågeställare, en avsändaridentitet, som skulle kunna vara t.ex ett hushåll i HLL-sketchen? Och utifrån den avsändaridentiteten följa ett mönster t.ex:  internetstiftelsen.se -> gnestafågelskådare -> gnestalillaförskola -> skobesgnesta?

Förutsätter att de domänerna finns i wellknown +  otur med den hashade adressen?

Vad är sannolikheten att ens identifiera en enskild “avsändaridentitet”?  (Leon dokument … ) Hur stor får sannolikheten vara för ett unikt fingeravtryck? Räcker det med att det är ett ovanligt fingeravtryck?
Är beräkningarna korrekta, återspeglar det verkligheten? 
Beräkna utifrån hur många kunder en ISP kan ha i sitt nät? x procent kan vara unika … i tal. Är det acceptabel nivå? 
Går det att se ett mönster från den enskilda entiteten

Undersök
Hur göra för att hitta en unikt identifierbar frågeställare i HLL-sketch?
Ta fram ett frågemönster för denna avsändar-identitet
Är det tillräckligt ovanligt för att anses som osannolikt?

Om det är ett problem
Om det är ett problem så är en föreslagen lösning: kryptera ip + domännamn = HLL-hash  
