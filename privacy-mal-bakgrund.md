
# Test och validering av dataintegritet i DNS TAPIR dataset

--- WORK IN PROGRESS ---

## Mål

- Ha bekräftat att det är väldigt osannolikt att identifiera enskilda individer i datasetet
- Ha bekräftat att all insamlade data anonymiseras innan den överförs till mottagaren DNS TAPIR i Core samt att eventuella risker för återidentifiering är hanterade på ett tillfredsställande sätt.
  
## TAPIR Core Dataset

Datasetet i TAPIR Core består av 1-minuters-aggregat/räknare av DNS-uppslag för välkända domäner (Well Known Domains). Dessa aggregat, histogram, innehåller data för hur ett domännamn på en resolver (TAPIR Edge) användes under tidsfönstret. Hur populär domänen var: antal uppslag (antal frågor), en uppskattning av hur många olika användare som slog upp det (antal klienter) och om uppslagen fungerade normalt eller misslyckades.

Ett DNS-uppslag sker varje gång någon (eller deras enhet) besöker en webbplats, skickar ett mejl eller öppnar en app.

## HyperLogLog

Algoritmen HyperLogLog (HLL) används för uppskattning av antal klienter. Den används i samverkan med andra åtgärder som exempelvis 1-minuters-aggregat, Well-known-listor etc så att summan av åtgärder blir privacy-säkert

Fullständig beskrivning av hur datasetet hanteras finns här: [https://www.dnstapir.se/docs/tapir-info-mgmt-sv/](https://www.dnstapir.se/docs/tapir-info-mgmt-sv/)
