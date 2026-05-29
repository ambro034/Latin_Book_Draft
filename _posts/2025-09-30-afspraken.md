---
title: Afspraken
author: lg
date: 2025-09-30
category: Jekyll
layout: post
---


> ##### Consultatie
{: .block-warning }

Realisatie afspraken
-------------

1. Niet alle beschreven functionaliteiten en technische voorzieningen kunnen tegelijk gerealiseerd worden. De realisatie zal in fasen worden uitgevoerd waarbij steeds naar een vastgesteld en afgesproken plateau wordt gewerkt. 

### Plateau 1 afspraken
Plateau 1 speelt zich af in 2026.

_Algemeen_
1. Binnen plateau 1 wordt de aandacht eerst gericht op uitwisseling van informatie tussen organisaties, in opvolgende plateaus volgt het informatie verstrekken aan de burger en aan individuele professionals, wel wordt hier in plateau 1 al rekening mee gehouden (in voorbereiding op).
2. Deelnemers zorgen binnen plateau 1 dat de drie samenwerkpatronen technisch zijn geïmplementeerd en de deelnemer daarmee over de capability beschikt om: a) opdrachten aan te vragen en te leveren via REST API, b) inzage te verzoeken en inzage te leveren via REST API, c) gebeurtenissen te kunnen melden en ontvangen via aansluiting op CORV2.
3. Deelnemers zorgen dat minimaal de samenwerkfunctie "Bepalen Bekendheid en Verrijking" (Opdracht uitvoeren deel) en de samenwerkfunctie "Uitwisselen Uitkomst Overleg" (Inzage deel) is geïmplementeerd.
4. De samenwerkingsfuncties en gerelateerde services (API's), maar ook Stelselvoorzieningen worden geimplementeerd en gebruikt zoals in de [specificaties][3] daarvan aangegeven. 

_Toegang_
1. We passen voor dit plateau minimaal de huidige authenticatie op organisatieniveau (Organisatie identifier en certficaat) toe. 
2. Bij toegangsverlening op basis van Organisatie identifier en certficaat wordt OIN gebruikt als identifier en uitsluitend PKIoverheid certificaten.
3. We onderzoeken de beweging naar nieuwere en meer granulaire vormen van toegangsverlening zoals 'identifier, certficaat en contract' authenticatie (FSC), authenticatie op niveau persoon/professional en daarmee o.a. OIDC/Oauth, FTV, DigiD en Wallet, en combinatie daarvan (FSC + FTV), maar realiseren deze nog niet binnen dit plateau.
4. Deze toegangsafspraken gelden voor zowel toegang tot de "Event Provenance Store en Event Hub" (ketenindex) als voor toegang tot de API's van deelnemers onderling gerelateerd aan de Samenwerkfuncties.
5. Alle hier bedoelde API's zijn toegankelijk (gemaakt) en standaard bereikbaar (gemaakt) via het internet. Standaard wil zeggen dat er geen (firewall/proxy) wijzigingen nodig zijn als een bestaande deelnemer connectie wil maken, maar dat deze waar nodig reeds vooraf gerealiseerd zijn.  

_Gebeurtenissen_
1. Binnen dit plateau werken we met gebeurtenissen die voor alle ketenpartijen toegankelijk zijn en mogen zijn. Voor latere plateau’s onderzoeken we autorisatie/abonneren op bepaalde gebeurtenissen/topics.
2. De gebeurtenissen bevatten genoeg informatie om een inzage te kunnen doen via het (REST API) inzage patroon. Zodoende wordt dus de toegangsverlening daarvan hergebruikt en is de informatie alleen zichtbaar voor partijen met toegang tot die informatie.
3. Voor dit plateau vertrekken we met in de gebeurtenissen opgenomen de persoon/BSN waar de gebeurtenis betrekking op heeft. Voor latere plateau’s onderzoeken we of pseudonimisering, etc. een meerwaarde heeft en noodzakelijk is.
4. We gaan in plateau 1 uit van één centrale Event Provenance Store en Event Hub (ketenindex). Voor latere scopes onderzoeken we of er nut en noodzaak is om in het stelsel meerdere event stores op te nemen.
5. Binnen dit plateau realiseren we via filtering, dat waar dat wenselijk is, gebeurtenissen niet meer bevraagd kunnen worden.


Burgerportaal afspraken
-------------

_Toegang burgerportaal_
1. Bij toegangsverlening voor burgers, denk aan het burgerportaal, gebruiken we DigiD waarbij de authentiserende persoon over een BSN moet beschikken.
2. Voor de te realiseren samenwerkfuncties binnen dit plateau gerelateerd aan het burgerportaal is betrouwbaarheidsniveau voor toegang “Substantieel” voldoende (minimaal Digid met App benodigd). Samenwerkfuncties die een hoger niveau vereisen vallen buiten dit plateau.
3. In de context van DigiD/eHerkenning passen we SAML toe en stappen (in hogerliggende plateaus) naar OIDC/Oauth over zodra dat wordt ondersteund door DigiD/eherkenning
4. Binnen dit plateau kan er niet van worden uitgegaan dat de identiteit van de persoon die het portaal gebruikt doorgegeven kan worden bij inzage bij ketenpartners. Er wordt onderzocht hoe dit gerealiseerd kan worden in situatie waar dit nodig is en is toegestaan binnen opvolgende plateau’s.
5. We gebruiken voor dit plateau (voor het burgerportaal) de gezagsinformatie van de BRP en dienen Gezagsdiensten te zijn om dat te kunnen en mogen. Gezagsdiensten zijn bestuursorganen en enkele daartoe aangewezen instanties, die rechtmatig toegang hebben tot de BRP volgens de Wet BRP en het Besluit BRP. 


Architectuur afspraken
-------------

1. Het jeugd-, zorg- en veiligheidsdomein vormt één domein met één bounded context. Een domein is een afgebakend, autonoom gebied waarin één coherent domeinmodel geldt en alle partijen dat model hanteren.
2. De informatievoorziening in het jeugd, zorg en veiligheidsdomein is gefedereerd en centrale ketenvoorzieningen worden alleen toegepast als dat nodig of wenselijk is.
3. Het jeugd-, zorg- en veiligheidsdomein kent een uniforme dienstverlening. Deze uniforme benadering waarborgt consistentie, interoperabiliteit en gelijkwaardigheid binnen het netwerk. Elke deelnemer, ongeacht grootte of specifieke context, neemt deel vanuit zijn eigen rol in dit samenwerkverband en verbindt zich aan het leveren van deze vastgestelde diensten volgens gezamenlijk overeengekomen standaarden en kwaliteitsnormen. Zie het samenwerkproces, de samenwerkfuncties en de samenwerkpatronen.
4. Binnen het jeugd-, zorg- en veiligheidsdomein wordt dezelfde taal gesproken. Uit het uitgangspunt “domein oriëntatie” volgt logisch dat uitgegaan wordt van één gemeenschappelijk semantisch, schematisch en syntactisch model. Populair gezegd spreken we, binnen het samenwerkverband, dezelfde taal.
5. Informatie wordt waar mogelijk en zinvol eenmalig opgeslagen en meervoudig gebruikt. Het kernidee is dat er voor elke soort informatie één leidende bron bestaat, één verantwoordelijke. In plaats van gegevens te kopiëren of over te nemen, wordt informatie steeds opnieuw opgehaald uit deze originele bron met één daarvoor verantwoordelijke partij. Let wel, een verantwoordelijke partij kan een andere partij de bevoegdheid geven om deze gegevens beschikbaar te maken. Eenmalig opslaan en meervoudig gebruik zorgt ervoor dat: de gegevens altijd up-to-date zijn, meer zekerheid over de juistheid van gegevens bestaat, er geen inconsistenties ontstaan door verouderde kopieën; we uitgaan van één actuele en historische waarheid, de integriteit van de data beter gewaarborgd blijft.
6. Gegevens zijn voorzien van context. Gegevens (in welke vorm dan ook) zijn altijd voorzien van contextuele gegevens. Door consequent context te koppelen aan gegevens wordt een robuuste basis voor geïnformeerde besluitvorming en effectieve data-gedreven processen gelegd. Dit zorgt voor een beter begrip, verhoogt de betrouwbaarheid en bevordert het juiste gebruik van de data.
7. Het jeugd, zorg en veiligheidsdomein is een gedistribueerd systeem, of kan minimaal als zodanig worden gezien, met een eventual consistency kenmerk naast availability en partition tolerance (zie het CAP theorem).
8. De bronhouder geeft toegang tot gegevens (op basis van afspraken). In beginsel moet elke bronhouder autonoom de voorwaarden bepalen voor toegang tot zijn gegevens via hun API’s. Deze benadering waarborgt de integriteit, veiligheid en het juiste gebruik van data. Gebruikers die toegang wensen tot deze gegevens, committeren zich aan het naleven van de gestelde voorwaarden. Dit creëert een transparant en verantwoord ecosysteem voor gegevensuitwisseling, waarbij de rechten en plichten van zowel bronhouders als gebruikers duidelijk zijn gedefinieerd en gerespecteerd.
9. Partijen zorgen voor flexibiliteit en aanpasbaarheid (waar dat kan) waardoor  ingespeeld kan worden op veranderingen en nieuwe wensen of vereisten. Door: een modulaire opbouw, een business agnostische ICT-benadering, een event gedreven benadering, real-time reactievermogen, afstemming op bedrijfsprocessen, API-first benadering, configureerbare workflows.


Principes gerelateerde afspraken
-------------

1. De principes zoals beschreven in Prinpes en standaarden worden gehanteerd en toegepast door alle partijen.


Standaarden gerelateerde afspraken
-------------

1. De standaarden zoals benoemd in Standaarden worden toegepast
2. Er wordt niet meer dan één versie van de standaarden achtergelopen.
3. De tijd tussen toepassing van vorige versies en nieuwe versies van de betreffende standaard wordt zo kort mogelijk gehouden.


Samenwerkproces gerelateerde afspraken
-------------

1. Het proces zoals beschreven in Samenwerkingsproces wordt gehanteerd in de samenwerking tussen de verschillende partijen.


Samenwerkfuncties gerelateerde afspraken
-------------

1. Functies voor samenwerking in het netwerkmodel worden door alle partijen toegepast zoals beschreven in Samenwerkfuncties.
2. Een organisatie past de Samenwerkfuncties toe die binnen de taak van de organisaties relevant zijn (niet elke organisatie zal alle samenwerkfuncties behoeven te implementeren).

Samenwerkpatronen gerelateerde afspraken
-------------

1. Elke organisatie ondersteunt de patronen zoals beschreven in Samenwerkpatronen dat wil zeggen de patronen Opdracht, Inzage en Gebeurtenissen.
2. Elke organisatie zorgt dat deze patronen technisch en operationeel worden geboden in het eigen technische landschap in een operationele vorm en compliant met het Afsprakenstelsel.
3. Elke organisatie zorgt dat de eigen achterliggende systemen interoperabel zijn met de patronen (waarbij sprake kan zijn van een implementatie en transitietijd). 



Technische afspraken
-------------

Deze afspraken zijn van toepassing voor de deelnemers aan het afsprakenstelsel. Ze zijn gericht op het realiseren van een gedistribueerd stelsel met zo min mogelijk afhankelijkheden en koppelingen. De technische afspraken zijn onderverdeeld in drie categorieën: Algemeen, Gebeurtenissen gerelateerd en REST API gerelateerd.

### Algemeen
1. Er is sprake van gefedereerde gedistribueerde systemen, waarbij monolithische centralistische concepten worden vervangen door oplossingen die gekenmerkt worden door het terugdringen van afhankelijkheden.
2. Er worden alleen centrale gedeelde (keten)voorzieningen gerealiseerd wanneer dat nodig is.
3. Alle extern aangeboden services (API's) zijn bereikbaar op FQDN via DNSSEC.
4. Voor alle voorzieningen in het stelsel gelden de [niet-functionele-eisen][4] zoals verderop weergeven.

### Gebeurtenissen gerelateerd
4. Voor het verzamelen, opslaan en distribueren van grote hoeveelheden gebeurtenisgegevens (events) is een centrale Event Provenance Store en Event Hub (ketenindex) nodig binnen het Stelsel. Een Event Provenance Store en Event Hub (ketenindex) is een gedistribueerd streamingplatform dat wordt gebruikt voor het verwerken en beheren van realtime datastreams (van gebeurtenissen/notificaties).
5. Er wordt een Ketenindex gerealiseerd, die customer journeys of ‘tijdlijnen’ mogelijk maakt. Omdat relevante gebeurtenissen gevonden kunnen worden, kunnen deze op een tijdlijn worden geplaatst. Het kunnen volgen (track en trace) van personen, objecten en concepten (en procesgangen) maakt integrale beelden mogelijk. Omdat het een verwijzing betreft kan eventueel een verdiepingsvraag worden gesteld.
6. Events (gebeurtenissen) ten behoeve van onder andere de ketenindex (en daarmee tijdslijnen) slaan we op in een centrale Event Store. Een Event Store is een gespecialiseerde database die gebeurtenissen (events) opslaat in een onveranderlijke, chronologische volgorde. Deze biedt daarmee een volledige historische weergave van alle veranderingen.
7. De Event Store maakt net als de Event Provenance Store en Event Hub (ketenindex) deel uit van CORV2.
8. De Event Store levert naast customer journeys of ‘tijdlijnen’ ook ondersteuning ten behoeve van data lineage / data provenance.
9. Binnen CORV2 hanteren we CQRS (Command Query Responsibility Segregation), oftewel het scheiden van het schrijf- en lees-datamodel.
10. Voor gebeurtenissen-uitwisseling in CORV2 context hanteren we een ontkoppelde variant via een REST API layer (API Proxy) om een toestand of gebeurtenis op te vragen, dus een pull model (en niet het native publish-subscribe model, waarbij producenten events publiceren en consumenten deze events kunnen consumeren via native interfaces).
11. Binnen de keten hanteren we een gestandaardiseerd Event Datamodel.

### REST API gerelateerd
12. REST API-calls binnen de keten verlopen decentraal, dus direct tussen partijen zonder tussenkomst van een centrale component. Als centrale component is slechts een API-Catalog beschikbaar, deze is om API’s vindbaar te maken en daarmee ondersteunend van aard.
13. REST API’s verbonden aan Samenwerkfuncties en Samenwerkpatronen volgen de specificaties daarvan.
14. REST API's gerelateerd aan Samenwerkfuncties of Ketenvoorzieningen zijn opgenomen in de decentrale API-Catalog's/DevPortal's en de centrale API-Catalog (verwijzend naar de decentrale Catalog/DevPortal).

Begrippenkader en semantiek gerelateerde afspraken
-------------

1. Binnen het Jeugd-, Zorg- en Veiligheiddomein wordt het Metamodel voor Informatiemodellering (MIM) gehanteerd en beheerd als kader voor het opstellen van informatiemodellen.
2. Binnen de bounded context (zie onderdeel Architectuur) spreken we met elkaar één taal en hanteren we het Begrippenkader bestaande uit het Semantisch model en Begrippen.
3. Waar nodig vertalen we het Semantisch model en de Begrippen naar onze eigen bounded context of breder domein en vice versa.
4. Alle Samenwerkfuncties en hun Samenwerkpatronen zijn beschreven in informatie- en data interactiemodellen en gepubliceerd via Afsprakenstelselsite (zowel ‘latest’ als alle vorige versies).
5. Samenwerkfuncties zijn geïmplementeerd conform deze modellen


Deelname gerelateerde afspraken
-------------

1. Elke partij binnen het domein, zie Architectuur, kan deelnemen aan het Afsprakenstelsel door de afspraken te implementeren en zich aan te melden.
2. Partijen melden zich aan door bij de Ledenadministrator en Vertrouwensleverancier zodat zij toegang tot het stelsel kunnen krijgen en vervolgens door hun beheer- en support mailadres via een Gebeurtenis aan te melden. Hun deelname zal dan gepubliceerd worden via een Gebeurtenis en de gegevens van de deelnemer zijn via een Inzage API op te vragen (en ook worden weergegeven via een website). 

Beheer en support afspraken
-------------

1. De stelselbeheerder zorgt voor het beheer van ketenvoorzieningen en support rond ketenvoorzieningen denk aan documentatie en ondersteuning bij het aansluiten of gebruik maken van deze voorzieningen.
2. Deelnemers beheren hun Opdracht, Inzage en Gebeurtenissen voorzieningen waaronder ook het leveren van documentatie, het publiceren van wijzigingen ten aanzien van die voorzieningen en vooral API’s geldt.
3. Deelnemers leveren een algemeen beheer- en support e-mail adres aan bij de Ledenadministrator, dat actief gelezen wordt door het Samen onder Handbereik (SoH) gelieerde beheer-, support- of devops-team. 
4. Deelnemers reageren actief op vragen, aankondigingen en verzoeken via dit mail-adres, denk aan verzoeken om te migreren naar een nieuwe major release van een SoH-API van een andere organisatie.
5. De Stelsel-distributeur	onderhoud en publiceert (via een Inzage API) een overzicht van SoH deelnemers en hun beheer- en support mailadres. Wijzigingen in de lijst worden aangegeven via een notificatie (via Gebeurtenis). 


Niet functionele eisen
-------------

Kern van het Samen onder Handbereik zijn de [Afspraken][1], deze verwijzen naar de [Samenwerkfuncties][2] en de [specificaties][3] daarvan. Deze kunnen gezien worden als functionele eisen. De Afspraken verwijzen ook naar niet-functionele-eisen (NFE’s). Deze zijn hieronder te vinden.

### NFE algemeen
Niet functionele eisen voor alle voorzieningen binnen het stelsel, zowel bij deelnemers als ten aanzien van stelselvoorzieningen

| NFE-id | Non-functional | Toelichting | Self assessment |
| --- | --- | --- | --- |
| B-01 | De omgeving en services voldoen aan de BIO dan wel aan NEN 7510 of ISO 27001 (voor organisaties waarvoor de BIO niet verplicht is). | Zie Baseline Informatiebeveiliging Overheid en NEN 7510/ISO27001. |  |
| B-02 | Software ontwikkeling volgt CIP Secure Software Development (SSD) normen en mmethodiek of een vergelijkbare aanpak |  |
| B-03 | Webportals/Webapps voldoen minimaal aan OWASP normen |  |
| B-04 | Webportals/Webapps voldoen aan de ICT beveiligingsrichtlijnen voor webapplicaties van het NCSC  |  |
| C-01 | De gerelateerde verwerkingen voldoen aan de AVG | Zie AVG. |  |
| I-01 | Webportals/Webapps functioneren voldoende bij het gebruik van de bekende veel gebruikte moderne browsers tot minimaal een versie daarvan terug | In het kader van compatibiliteit. |  |
| I-02 | Webportals/Webapps functioneren zonder plugins | In het kader van compatibiliteit wordt het gebruik van plugins niet toegestaan. |  |
| I-03 | Stelsel API’s kunnen worden getest op beschikbaarheid en functioneren | Andere deelnemers moeten het functioneren van een API kunnen valideren en monitoren. |  |
| I-04 | Stelsel API’s zijn gedocumenteerd op een API Catalog/DevPortal waar ook toegang aanvragen tot de API’s kan worden aangevraagd | Informatie en toegang dient eenvoudig en laagdrempelig te kunnen verlopen. |  |
| I-07 | De stelsel API’s zijn opgenomen in de domein API Catalog waarbij wordt verwezen naar de decentrale API Catalogs | Decentrale API Catalogs dienen eenvoudig en laagdrempelig te kunnen worden gevonden. |  |
| P-01 | Maximale responstijd < 200 ms voor eenvoudige GET-verzoeken voor Stelsel API’s | Responsetijd vereiste. |  |
| P-02 | Gemiddelde responstijd < 2 seconden voor Stelsel API’s bij normale belasting | Responsetijd vereiste. |  |
| P-03 | Onder piekbelasting voor Stelsel API’s < 3 seconden | Responsetijd vereiste. |  |
| P-04 | Ondersteuning voor 100+ requests per seconde voor Stelsel API’s | Belastingsvereiste. |  |
| P-05 | Uptime van 99,9% (ongeplande downtime max. 8,8 uur/jaar), herstel binnen 4 uur op werkdagen | Streefwaarde. |  |
| P-06 | RTO 2-4 uur en RPO 1-24 voor Stelsel API’s | Recovery vereisten. |  |
| P-07 | Mean Time Between Failures (MTBF) > 99,99% en Mean Time to Recovery (MTTR) < 1 uur. | Streefwaarde. |  |

### NFE Stelselvoorzieningen
Aanvullende niet-functionele eisen  voor Stelselvoorzieningen:

| NFE-id | Non-functional | Toelichting | Self assessment |
| --- | --- | --- | --- |
| SA-01 | Er is een solution architectuur beschikbaar | De solution architectuur geeft richting aan de oplossing en bevat richtinggevende uitspraken. |  |
| SA-02 | Er is een high level design beschikbaar | Het high level design beschrijft hoe de voorziening wordt/is gerealiseerd, welke componenten en software deze bevat en hoe deze in samenhang werken. |  |
| SA-03 | De Stelselvoorzieningen service(s) zijn beschreven, hun interfaces en gebruik | Documentatie van de services gericht op afname daarvan. |  |
| SA-04 | Er is beschreven waar de voorzieningen en services zijn gerealiseerd (datacenter, cloud) | Denk aan waar de voorzieningen en services zijn gehost. |  |
| SA-05 | Er is beschreven welke omgevingen worden geboden, dat dient ten minste een productie en acceptatie omgeving te zijn | De acceptatie omgeving dient ook en sterker vooral gebruikt te kunnen worden door deelnemers in het stelsel, zij moeten aan kunnen sluiten op de acceptatieomgeving zodat een gedistribueerde acceptatieomgeving ontstaat zoals er ook een gedistribueerde productieomgeving is. |  |
| ST-01 | Er dient een self-service omgeving beschikbaar te zijn, welke onderdeel van de acceptatieomgeving mag zijn, waar deelnemers zelf zonder hulp voorzieningen en werking van het stelsel kunnen testen. | Denk aan het self service kunnen testen van insturen van events, terug ontvangen van events, inzage kunnen doen, (test)services kunnen triggeren die inzage doen bij de deelnemer. |  |
| ST-02 | Voor de voorziening/service(s) is een performance test uitgevoerd en alle response tijden vallen binnen de vereisten | Zie voor de response tijden het algemene deel (de NFR’s voor het stelsel). |  |
| SB-01 | De voorzieningen voldoen aan de BIO (intern gericht) en ABRO (extern gericht) | Zie Baseline Informatiebeveiliging Overheid en Algemene Beveiligingseisen voor Rijksoverheidsopdrachten (in het geval van externe dienstverleners). |  |
| SB-01 | De voorzieningen getest middels een pentest/security test van het type white/crystal-box, er mogen geen bevindingen open staan van 7.0 of hoger en alleen bevindingen van 4.0 of hoger als dit expliciet en formeel vastgelegd is toegestaan | Zie Common Vulnerability Scoring System. |  |
| SC-01 | Er wordt gebruik gemaakt van open standaarden conform de lijst van standaarden van het Forum van Standaardisatie. | Zie Forum Standaardisatie, Lijst open standaarden |  |
| SC-02 | Er wordt gebruik gemaakt van open source software tenzij. | Zie het “Open, tenzij” beleid, zie ook Woo en Who (t.a.v. informatie waaronder broncode). |  |
| SC-03 | In de documentatie wordt aangegeven of sprake is van de verwerking van persoonsgegevens en wie de gegevensverantwoordelijke(n) is(/zijn). | De verwerker moet kunnen aangeven wie de gegevensverantwoordelijke(n) is(/zijn) en houders van de DPIA(s). |  |
| SC-04 | Indien sprake is van verplichte registratie (cloud/algoritmen) wordt dit opgenomen in de documentatie alsmede een verwijzing naar de registratie en eigenaar van de registratie | De dienstverlener moet kunnen aangeven of sprake is van registraties en wie verantwoordelijk is voor registratie. |  |
| SR-01 | Er wordt voorzien in een backup en restore beschrijving, de restore procedure wordt minimaal jaarlijks getest. | Beschrijving van backup van data, software, documentatie e.d. om volledige restore uit te kunnen voeren van data en service. |  |
| SR-02 | Business continuïteit beschrijving. | Beschrijving van te beschermen service(s), (business)impact en disaster recovery maatregelen en procedures. |  |
| SR-03 | In de Business continuïteit dreigingsscenario’s worden ook cyber dreigingen meegenomen en waar relevant omstandigheden dit uitvoering van exit scenario’s vereisen. | Denk bij cyberdreigingen aan de vercijfering van data (ransom attacks) en aan exit plannen in gevallen waar datacenters of infrastructuur van derden wordt gebruikt. |  |
| SR-04 | Er is een beschrijving van het exit-plan beschikbaar. Vereisten vanuit beleid rond exit-plannen worden aantoonbaar ingevuld. | Denk aan vereisten als het testen van de exit-plannen. |  |
| SO-01 | Er is 1e, 2e en 3e lijns-ondersteuning, beheer en monitoring ingericht | De voorzieningen dienen adequaat beheerd en gemonitord te worden . |  |
| SO-02 | De 1e, 2e en 3e lijns-ondersteuningscontactpunten zijn bekend en gepubliceerd | De serviceorganisatie dient eenvoudig en laagdrempelig benaderbaar te zijn en te kunnen worden gevonden. |  |
| SO-03 | Er is een SLA en DAP opgesteld voor de voorzieningen/services | Service niveau afspraken en procedures worden vastgelegd. |  |
| SO-04 | Er is een gedefinieerde en verstrekte security incident procedure | Security incidenten vergen speciale aandacht en versnelde reactietijden en vooraf gedefinieerde escalatie mogelijkheden. |  |
| SO-05 | Wijzigingen beheer is beschreven en geïmplementeerd | Voorzieningen en services zullen regelmatig wijzigingen ondergaan, er dient duidelijkheid te zijn dat wijzigingen beheer is ingericht |  |
| SO-06 | Als onderdeel van wijzigingen beheer is opgenomen de coördinatie van wijzigingen die actie van deelnemers vereisen | Wijzigingen kunnen acties van deelnemers vereisen, onafhankelijk van elkaar tot wijzigingen die een gelijktijdige wijziging en test vereisen bij alle deelnemers of subgroepen daarvan. |  |
| SP-01 | Maximale responstijd < 200 ms voor alle verzoeken | Responsetijd vereiste. |  |
| SP-02 | Gemiddelde responstijd < 1 seconden bij normale belasting | Responsetijd vereiste. |  |
| SP-03 | Onder piekbelasting < 2 seconden | Responsetijd vereiste. |  |
| SP-04 | Ondersteuning voor 100.000+ requests per seconde event gebaseerde push and pull step 1 stelselvoorzieningen/services API’s | Belastingsvereiste. |  |
| SP-04 | Ondersteuning voor 10.000+ requests per seconde event gebaseerde pull step 2 stelselvoorzieningen/services API’s | Belastingsvereiste. |  |
| SP-05 | Uptime van 99,9% (ongeplande downtime max. 8,8 uur/jaar), herstel binnen 4 uur op werkdagen | Uptime vereiste. |  |
| SP-06 | RTO 2-4 uur en RPO 1-24 voor Stelsel API’s | Recovery vereisten gevalideerd haalbaar. |  |
| SP-07 | Mean Time Between Failures (MTBF) > 99,99% en Mean Time to Recovery (MTTR) < 1 uur. | MTBF vereiste. |  |

[1]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-30-afspraken.html
[2]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-26-samenwerkfuncties.html
[3]: https://samen-onder-handbereik.github.io/specificaties/
[4]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-30-afspraken.html#niet-functionele-eisen