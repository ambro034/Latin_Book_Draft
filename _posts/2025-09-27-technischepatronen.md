---
title: Technische patronen
author: lg
date: 2025-09-27 14:00:00
category: Jekyll
layout: post
---

> ##### Consultatie
{: .block-warning }

Kernpatronen
-------------

Opdracht, Inzage en Gebeurtenissen zijn functionele patronen. In dit onderdeel zijn de technische patronen beschreven waarmee deze functionele samenwerkpatronen kunnen worden gerealiseerd en op hun beurt daarmee de functionele samenwerkfuncties.

Kortom de samenwerkfuncties zijn op te bouwen uit de samenwerkpatronen en  de samenwerkpatronen uit de volgende technische patronen:

- Command
- Query
- Event

Het Command patroon levert een toestandswijzing op (change of state).

Het Query patroon voert een leesoperatie uit (read of state).

Het Event patroon geeft aan dat een feit of toestandsverandering heeft plaatsgevonden. Zie ook onderstaande vergelijk.

| Aspect | Command | Query | Event |
| --- | --- | --- | --- |
| Doel | Toestandswijziging | Leesoperatie | Declaratie dat iets heeft plaatsgevonden |
| Type | Doorgaans synchroon | Doorgaans synchroon | Doorgaans asynchroon |
| Adressering | Specifieke bestemming | Specifieke bestemming | Meerdere geabonneerden of broadcast |
| Communicatie | request-response | request-response | fire and forget |
| Actie | Initieert een verandering (state change) | Leesoperatie (read of state) | Beschrijft een toestandsverandering |
| Return response | Success/failure acknowledgment | Success/failure acknowledgment | Geen directe response verwacht |


Binnen het Afsprakenstelsel worden deze patronen concreet toegepast in de vormen:

| Patroon | Protocol | Methode | Response | Type |
| --- | --- | --- | --- | --- |
| Command | HTTPS REST API call | POST, PUT, PATCH, DELETE | 200, 201, 400, 401, etc. | Synchroon |
| Query | HTTPS REST API call | GET | 200, 204, 400, 401, etc. | Synchroon |
| Event | HTTPS REST API call* | POST (event versturen), GET (even lezen) | 200, 400, 401, etc. | Asynchroon |

_\* Events kunnen worden gedeeld via o.a. AMQP, MQTT, Kafka, WebSockets maar ook via REST. Voor HTTPS REST is hier gekozen om een loosely coupled koppelvlak te creëren, een relatief eenvoudig koppelvlak aan te bieden wat bekend is voor alle >1000 organisaties in het domein en gelet het type oplossing (ketenindex)._

Voorbeelden
-------------

Hieronder worden enkele voorbeelden genoemd die het verband tussen Samenwerkpatroon en Technisch patroon laten zien.

Opdracht

a) via REST API
Organisatie A geeft een opdrachten of verzoekt om een opdracht uit te voeren richting Organisatie B (Opdracht samenwerkpatroon). Organisatie A stuurt REST API POST naar API van Organisatie B (**Command patroon**). Organisatie B geeft een 200/201 terug (ontvangen en wordt opgepakt) of een 202 (geaccepteerd maar nog niet afgerond, bevat informatie om status te kunnen nagaan en/of voortgang te volgen). Hierop zijn allerlei variaties mogelijk afhankelijk hoe de Samenwerkfunctie is gedefinieerd en de composite/ capability API.

b) via events
Organisatie A geeft een opdrachten of verzoekt om een opdracht uit te voeren richting Organisatie B (Opdracht samenwerkpatroon) dan wel een partij die de opdracht wil/kan uitvoeren als er daar meerdere van zijn (Opdracht samenwerkpatroon). Organisatie A stuurt een event (**Event patroon**). Organisatie B (of een andere organisatie) stuurt een event dat de opdracht wordt opgepakt. Organisatie A bevestigt naar Organisatie B (of een andere organisatie) dat de opdracht aan die partij wordt toegekend. In de events kunnen URL’s zijn opgenomen waar informatie over de opdracht is te vinden (**Query patroon**) of de status van uitvoering (Query patroon). Hierop zijn allerlei variaties mogelijk afhankelijk hoe de Samenwerkfunctie is gedefinieerd en de event gebaseerde invulling wordt ontworpen.

c) via ebMS
Dit is de huidige benadering (CORV1).

Inzage  
Organisatie A wil informatie inzien waarvan Organisatie B bronhouder is (Inzage samenwerkpatroon). Organisatie A stuurt een REST API GET naar de API van Organisatie B (**Query patroon**). Organisatie B geeft een 200 terug en de informatie. Hierop zijn allerlei variaties mogelijk afhankelijk hoe de Samenwerkfunctie is gedefinieerd en de composite/ capability API.

Organisatie A kan genotificeerd zijn of acteren op een event welke Organisatie A heeft gezien of ontvangen. In het event kan een URL zijn opgenomen voor de Inzage.

Gebeurtenis  
Organisatie A geeft aan dat een bepaalde gebeurtenis, actie of toestandswijziging heeft plaatsgevonden (Gebeurtenis samenwerkpatroon). Een aantal andere organisaties is hierin geïnteresseerd. Organisatie A stuur het event via een REST API POST naar de Event Provenance Store en Event Hub (CORV2) (Command patroon). De geïnteresseerde organisaties sturen via REST API POST een query naar de Event Provenance Store en Event Hub (Command patroon). Daarna sturen ze een REST API GET om na te gaan over de query resultaten heeft (‘pollen’) (Query patroon).  Bij elkaar geven deze invulling aan het **Event** **patroon** via een asynchone API benadering (waarbij AsyncAPI wordt toegepast voor de API beschrijvingen.

Request-response varianten
-------------

Zoals in de voorbeelden genoemd kan een opdracht (samenwerkpatroon) uitgezet worden via een directe REST-API call of middels events. In beide gevallen is er sprake van een request (ik heb een opdracht voor je) en gewenste response (ik heb de opdracht ontvangen en ga daarmee wel/niet aan de slag).

In het REST-API geval is de response direct in de vorm van een 200/201/202 met informatie als wordt wel/niet opgepakt. Het is niet altijd mogelijk dit al direct aan te geven en kan slecht de ontvangst van het verzoek worden bevestigd. Er zal dan een status aanvraag (query) gedaan moeten worden naar de status of naar events worden gekeken die de status aangeven. Hoe het ook zij, er is sprake van een organisatorische afspraak, zoals “als ik een opdracht ontvang dan ga ik dit-of-dat doen en hou ik je zo-en-zo op de hoogte”. 

In de situatie waarbij met events wordt gewerkt is dit feitelijke niet anders. Hier geldt dezelfde afspraak, alleen wordt een andere techniek gebruikt om de opdracht te versturen en te bevestigen. De opdracht wordt via een event uitgezet, degene die de opdracht uitvoert leest het event en stuurt een event dat de opdracht is opgepakt, de opdracht is gepland, de opdracht is uitgevoerd, etc.

De vraag is wanneer pas je nu welke variant toe? 

De directe REST-API wordt toegepast wanneer:
- er één geadresseerde is;
- en het REST-API end-point (de url) bekend is, er toegang tot het end-point is en het bekend is hoe het end-point gebruikt kan worden;
- en er sprake is van een laag volume aan verzoeken;
- en er sprake is van een laag volume aan end-points voor de betreffende samenwerkfunctie (enkele tot enkele tientallen).

Verder geldt voor de directe REST-API variant een randvoorwaarde, namelijk dat de end-point adressen (url) ergens worden gepubliceerd en deze informatie actueel en juist is.

De event variant wordt toegepast wanneer:
- er meerdere geadresseerden zijn en/of het end-point (url) niet bekend is;
- en er sprake is van een hoog volume aan verzoeken;
- en er sprake is van een hoog volume aan end-points voor de betreffende samenwerkfunctie (enkele tot enkele tientallen). 

In de specificaties van de Samenwerkfuncties is te zien welke variant voor die Samenwerkfunctie en stap daarbinnen is toegepast.

Patronen informatieniveau-differentiatie
-------------

Functioneel bezien bestaat de wens onderscheid te maken in niveau van toegang tot informatie in events en/of aangeboden via API’s. Zo is denkbaar dat een bepaalde organisatie/rol minder detailinformatie hoeft en mag krijgen, en een andere meer. Ook is denkbaar dat dit van omstandigheden en situatie af kan hangen. Denk aan een normale situatie versus een acute situatie en risicovolle situatie. Hieronder worden de verschillend opties beschreven en de keuze voor invulling van deze wens.

Er is in dat geval sprake van verschillende niveaus van informatie beschikbaarheid. Denk aan een 'wat' niveau (er is een gebeurtenis type x) en een 'dat' niveau (welke ging over y). Er zou gewerkt kunnen worden zoals een niveau 0 (wat), niveau 1 (wat met een 'dat' deel, maar niet in detail) en een niveau 2 ('dat' met meer details).

### Events
Grofweg zijn er twee opties:
- Event met alle informatie, maar onderscheid in niveaus 
- Event per niveau, dus meerdere events met elk meer of minder informatie

**Event met alle informatie**  
In dit geval zijn er de volgende benaderingen:
- Ontvangers filteren zelf
- Filtering bij de Event Provenance Store en Event Hub (Ketenindex)
- Eén event met versleutelde delen

De eerste optie valt af omdat dit niet sterk genoeg is vanuit een gegevensbescherming- en beveiligingsoptiek. De tweede optie vraat dat de Ketenindex onderscheid kan maken naar wie de bevraging doet of welke claims (OIDC claims) de partij meestuurt die het event ophaalt. Dit geeft complexiteit (filtering) aan de Ketenindex kant. De laatste variant geeft complexiteit bij alle partijen (sleutelbeheer, cryptografische bewerkingen). Dit is verre van aantrekkelijk, maar kan als PET invulling ook vanuit een andere optiek gewenst of nodig zijn.

Keuze/voorkeur bij deze optie: volgt

**Event per niveau**  
Hier wordt gewerkt met meerdere events (over dezelfde gebeurtenis) per doelgroep of autorisatieniveau. 

Er is sprake van eenzelfde gebeurtenis in de werkelijkheid, maar vertaald naar:
- niveau 0 event naar brede groep
- niveau 1 event naar betrokken ketenpartners
- niveau 2 event naar bevoegde partij/audit/provenance store

Met toepassing van correlationid (gedeelde correlatie), eventfamilie bijvoorbeeld uuo (uitwisselen-uitkomst-overleg) en informatieniveau, bijvoorbeeld “notification, restricted, full”.

Een niveau 0 event kan bijvoorbeeld aangeven dat er een uitkomst beschikbaar is.
Een niveau 1 event zegt meer, bijvoorbeeld: welke activiteit heeft de uitkomst gegenereerd, en door welke organisatie/rol is dat gedaan. Maar het bevat nog geen details over personen, brondocumenten, inhoudelijke besluiten of gebruikte gegevens.
Een niveau 2 event is volledig en kan bijvoorbeeld additioneel aangeven details over personen, brondocumenten, inhoudelijke besluiten of gebruikte gegevens.

Een mogelijke benadering hierbij zou kunnen zijn:
1. Publiceer een minimaal notificatie-event naar brede doelgroep.
2. Publiceer rijkere events alleen naar organisaties/geautoriseerde die dat nodig hebben.  
En (optie)  
3. Zet volledige PROV in een aparte provenance store.
4. Laat events verwijzen naar die PROV-store met een beveiligde link/reference.
5. Autoriseer toegang tot de PROV-store per organisatie, rol, doelbinding en casus.

Hierbij zou gewerkt kunnen worden met twee autorisatielagen, namelijk een event- en data autorisatielaag.

Event autorisatielaag voorbeeld:  
Uitkomst-overleg-beschikbaar-gesteld.notification, naar alle ketenpartners  
uitkomst-overleg -beschikbaar-gesteld.restricted , naar betrokken ketenpartners  
uitkomst-overleg -beschikbaar-gesteld.full, naar voorzitter, bevoegde deelnemer  

Data autorisatielaag voorbeeld:  
PROV niveau 0, er is een activiteit geweest  
PROV niveau 1, welke organisatie/rol en welke vorige processtap  
PROV niveau 2, welke bronnen, versies, personen, regels en afleidingen  

Technisch zou gewerkt kunnen worden met aparte topics/kanalen per niveau, bijvoorbeeld:  
uoo.notification  
uoo.restricted  
uoo.full  

Een alternatief is om met één topic te werken en filtering per subscription, bijvoorbeeld:
uoo.events met attributen zoals "provenancelevel": "restricted" en "audience": "ketenpartner" bijvoorbeeld. Waarbij de filtering wordt gedaan door de Event Provenance Store en Event Hub (Ketenindex).

Keuze/voorkeur bij deze optie: volgt

Keuze  
De keuze uit de twee varianten (één versus meerdere events) is: volgt

### API’s
Voor REST-API’s is het werken met niveaus beter beheersbaar dan bij events, omdat informatie pas wordt opgehaald op het moment dat een client erom vraagt. Daardoor kun je per organisatie, rol, doelbinding, scope en endpoint bepalen welk informatieniveau wordt teruggegeven.
Er is dus eenzelfde werkelijkheid met meerdere representaties. Eén resource of procesobject, maar verschillende views afhankelijk van autorisatie en doelbinding.
Kortom er is:
- één logisch object
- met meerdere API-representaties
- autorisatie per client/organisatie/scope
- optioneel aparte endpoints voor detailniveaus

Er zou bijvoorbeeld gewerkt kunnen worden met een model als in onderstaande tabel:

| Niveau | Doelgroep | Inhoud |
| --- | --- | --- |
| Niveau 0 - minimaal | Organisaties die alleen mogen weten dát iets bestaat | id, status, datum, globale referentie |
| Niveau 1 - beperkt | Betrokken ketenpartners | beperkte metadata, processtatus, abstracte data |
| Niveau 2 - volledig | Bevoegde deelnemers | inhoud, bronnen, beslissingen, volledige data |

Er zijn verschillende benaderingen om dit in te vullen:
- Eén endpoint, representatie afhankelijk van autorisatie
- Aparte endpoints per informatieniveau
- Eén endpoint met view of projection
- Content negotiation
- Links naar detailinformatie: HATEOAS / affordances

**Eén endpoint, representatie afhankelijk van autorisatie**  
Op basis van de autorisatie zou een response kunnen volgen met (voorbeeld):
- info (niveau 0): er is een uitkomst beschikbaar voor dit casusoverleg (en meer niet)
- info (niveau 1): procesmatige context, maar nog geen persoonsgegevens, volledige bronnen of inhoudelijke details
- info (niveau 1): ook persoonsgegevens, volledige bronnen en/of inhoudelijke details

**Aparte endpoints per informatieniveau**  
Bijvoorbeeld:
GET /uitkomst-overleg/uoo-001 (mogelijk voor technische check / monitoring)  
GET /uitkomst-overleg/uoo-001/niveau0  
GET /uitkomst-overleg/uoo-001/niveau1  
GET /uitkomst-overleg/uoo-001/niveau2  

Met een zelfde inhoudelijke response voor de niveaus als bij de eerdere optie.

**Eén endpoint met view of projection**  
Bij deze benadering wordt gebruik gemaakt van een queryparameter.

GET /uitkomst-overleg/uoo-001?view=niveau0  
GET /uitkomst-overleg/uoo-001?view=niveau1  
GET /uitkomst-overleg/uoo-001?view=niveau2  

Ook hier wordt eenzelfde inhoudelijke response per niveau terug gegeven als beschreven bij de eerste optie (als voorbeeld).

**Content negotiation**  
Het niveau zou ook meegeven kunnen worden via headers, bijvoorbeeld:
GET /uitkomst-overleg/uuo-001
Accept: application/vnd.org.uuo.niveau0+json 
“Accept” is een standaard HTTP-header waarmee een client aangeeft welke response-formaten de client begrijpt of wil ontvangen. In het voorbeeld dus: Geef de niveau 0 uuo-representatie als JSON. 

Ook hier wordt eenzelfde inhoudelijke response per niveau terug gegeven als beschreven bij de eerste optie (als voorbeeld), waar “application” aangeeft dat het gaat om applicatiedata en “vnd.org” dat het een eigen organisatie- of ketenformaat betreft (en “org” de organisatienaam is).

**Links naar detailinformatie: HATEOAS / affordances**  
Hierbij worden alleen links (doorverwijzingen) naar informatie die de client mag ophalen teruggegeven.
 
Ook hier wordt eenzelfde inhoudelijke response per niveau terug gegeven, via de doorverwijzing, als beschreven bij de eerste optie (als voorbeeld).

Keuze/voorkeur:
Gebruik van één canoniek resource-id, met meerdere representaties/views en autorisatie op basis van organisatie, rol, scope, doelbinding, casusbetrokkenheid, etc. 

Dat zou er als volgt uit kunnen zien:  
GET /uitkomst-overleg/{uuoId}/uitkomst  
GET / uitkomst-overleg/{uuoId }/uitkomst/niveau0  
GET / uitkomst-overleg/{uuoId }/uitkomst/niveau1  
GET / uitkomst-overleg/{uuoId }/uitkomst/niveau2  

Met scopes als:  
uoo:read:minimaal  
uoo:read:beperkt  
uoo:read:volledig  

En met de claims (OIDC) in het token, zoals de scope. De server beslist dan:
- heeft deze organisatie toegang tot deze uitkomst overleg?
- past het doel bij de opvraag?
- heeft de client de juiste scope?
- mag deze rol deze de informatie op dit niveau zien?
- moeten persoonsgegevens worden gemaskeerd?
- moeten bronverwijzingen worden geabstraheerd?
- etc.


