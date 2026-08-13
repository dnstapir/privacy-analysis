# Test och validering av dataintegritet i DNS TAPIR dataset

*** WORK IN PROGRESS ***

## Mål:
- Ha bekräftat att det är väldigt osannolikt att identifiera enskilda individer i datasetet
- Ha bekräftat att all insamlade data anonymiseras innan den överförs till mottagaren DNS TAPIR i Core samt att eventuella risker för återidentifiering är hanterade på ett tillfredsställande sätt.
  

## TAPIR Core Dataset

Datasetet i TAPIR Core består av 1-minuters-aggregat/räknare av DNS-uppslag för välkända domäner (Well Known Domains). Dessa aggregat, histogram, innehåller data för hur ett domännamn på en resolver (TAPIR Edge) användes under tidsfönstret. Hur populär domänen var: antal uppslag (antal frågor), en uppskattning av hur många olika användare som slog upp det (antal klienter) och om uppslagen fungerade normalt eller misslyckades. 

Ett DNS-uppslag sker varje gång någon (eller deras enhet) besöker en webbplats, skickar ett mejl eller öppnar en app.    

## HyperLogLog

Algoritmen HyperLogLog (HLL) används för uppskattning av antal klienter. Den används i samverkan med andra åtgärder som exempelvis 1-minuters-aggregat, Well-known-listor etc så att summan av åtgärder blir privacy-säkert 

Fullständig beskrivning av hur datasetet hanteras finns här: [https://www.dnstapir.se/docs/tapir-info-mgmt-sv/](https://www.dnstapir.se/docs/tapir-info-mgmt-sv/)
 

## TEST 1: Koppla ihop multipla domännamn till samma singulära individ med hög säkerhet

**Hypotes: Det går att koppla ihop multipla domännamn till samma individ med hög säkerhet**

**Frågeställning:** 
- Genom att identifiera ett specifikt värde i en s.k HLL-hink, går det att via detta värde identifiera ett beteendemönster (en följd av DNS-frågor) för detta värde?
- Kan detta mönster i sin tur identifiera en individ? (i ett efterföljande test). Ger det en profil som kan användas för att identifiera en verklig individ?


### Metod-idéer:

Applicera en Membership Inference-algoritm på ett urval av dataset:et.

Steg 1: Hitta en singulär individ (uniquely discernible individual) i uppskattningen av antalet klienter (HLL-sketchen) (Membership cohort inference)
- Undersök om det går att hitta en singulär individ (unique discernible individual), eller en tillräckligt liten grupp, alltså en ny typ av svag identifierare (weak identifier). Sannolikt ja enligt Membership Inference-teori.
- Räkna ut murmur-hashar, kan vi se vad individen gör?  
- Hitta en kombination hink + siffran i hinken som är såpass unik eller liten, hur vanlig är den givet att man har x klienter i sitt nätverk.
- Bucket-nummer + innehållet i bucketen, kör inferensen, använd de som har få i
- Om den syns på flera ställen ökar sannolikheten för att det är samma individ. 

Steg 2: Identifiera ett antal domännamn under ett valt tidsintervall som går att koppla ihop med denna individ.
- Finns det  individer som utmärker sig - gör en inferens - vilka domäner har de tittat på? 

Steg 3 (separat test): Analysera huruvida dessa välkända domäner kan användas för att identifiera en verklig individ. 
- Är det mönstret tillräckligt för att skapa en identifierande profil?  
- Undersök logiken för vilka domäner som finns i wellknown, och är cutoff på 20 klienter tillräckligt? 

### Teori
Membership Inference Attacks on Machine Learning: A Survey

[https://arxiv.org/abs/2103.07853](https://arxiv.org/abs/2103.07853)

