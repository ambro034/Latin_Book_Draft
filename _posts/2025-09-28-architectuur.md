---
title: Architectuur
author: lg
date: 2025-09-28 09:00:00
category: Jekyll
layout: post
---

> ##### Definitief
{: .block-tip }

ICT-architectuur heeft als doel richting te geven aan een oplossing binnen een bepaalde scope. De oplossing in deze context is het creëren van een gezamenlijke, federatieve structuur waarin meerdere ketenpartners - uit jeugdhulp, zorg en veiligheid - op een uniforme, veilige en betrouwbare wijze informatie kunnen uitwisselen en samenwerken. De scope is het Jeugd-, Zorg- en Veiligheidsdomein. In dit domein zijn vele organisaties vertegenwoordigd, zie onderstaande figuur.

![Alt text]({{ site.baseurl }}/assets/domein.png)

Inhoudelijk bezien zijn er de organisaties welke informatie delen of ontvangen, en zijn er de stelselvoorzieningen welke door deze partijen gebruikt worden. Dit geeft twee belangrijke architectuur invalshoeken, die van de organisaties en die ten aanzien van het stelsel zelf en de stelselvoorzieningen. Zie onderstaande figuur.

![Alt text]({{ site.baseurl }}/assets/conpro.png)

De architectuur wordt belicht aan de hand van het NORA vijflaagsmodel. Bij architectuur keuzes moet vanwege wendbaarheid en aanpassingsvermogen altijd meegenomen worden welke afhankelijkheden nu en in de toekomst zullen bestaan.

**Grondslagen**

De Grondslagenlaag beschrijft met welke methoden en standaarden invulling gegeven kan worden aan wet- en regelgeving die relevant is voor het stelsel. (bron: NORA)

**Organisatie**

De Organisatielaag bevat architectuurcomponenten die relevant zijn voor het maken van de architectuur waarin de organisatorische aspecten in balans worden gebracht met de afgesproken diensten. (bron: NORA)

**Informatie**

De Informatielaag bevat architectuurcomponenten die relevant zijn voor het maken van de architectuur waarin de aspecten van informatie (zoals begrippen en informatiemodellen) in balans worden gebracht met de afgesproken diensten. (bron: NORA)

**Applicaties**

De Applicatielaag beschrijft met welke methoden en standaarden invulling gegeven wordt aan de applicatie\-architectuur. (bron: NORA)

**IT-infrastructuur**

De IT-infrastructuur laag beschrijft met welke methoden en standaarden invulling gegeven kan worden aan het fysieke transport van digitale gegevens (data) binnen het stelsel. (bron: NORA)


Grondslagen
-------------

Zie onderdeel [Grondslagen][1] en [Juridische kaders][2] waarin de relevante grondslagen zijn beschreven. De toegepaste standaarden om invulling te kunnen geven aan de grondslagen zijn te vinden in onderdeel Standaarden.

Methoden om invulling te geven aan grondslagen (WAMS, WPG, AVG, WGS, WGPGA, WDO, Wmebv, EU data wetten) binnen het stelsel zijn:

- Transitie van estafettemodel naar netwerkmodel, uitwisselen gebeurtenissen, inzage verstrekking, ketenindex/tijdslijnen;
- Het Afsprakenstelsel Jeugd, Zorg en Veiligheidsdomein (bounded context) zelf;
- Privacy-by-design benaderingen, denk aan Data minimalisatie zoals gebruik van informatiearme berichten, maar ook aan toepassing van Privacy-Enhancing-Technologies, dat in opvolgende plateau’s, maar ook aan de huidige Middenvelder dienst;
- Security-by-design.

Er zijn ook fundamentele grondslagen die zorgen dat organisaties in het Jeugd, Zorg en Veiligheidsdomein kunnen samenwerken, denk o.a. aan Europees Verdrag tot Bescherming van de Rechten van de Mens, Internationaal Verdrag voor de Rechten van het Kind, Jeugdwet 2015 en WAMS.

Organisatie
-------------

De organisatie voert een taak / wettelijke-taak uit en beschikt over primaire en secundaire processen om daar uitvoering aan te geven. In deze context zijn de [processen][3] Verbinding aangaan, Samen onderzoeken, Samen Beslissen, Doen wat werkt en Samen leren relevant. Zodat er een toekomstbestendige, transparante en effectieve samenwerking ontstaat, met de burger en ketenpartners, digitaal ondersteund binnen één netwerk (netwerkmodel). Die samenwerking helpt om de taak van de organisatie uit te voeren en huidig ervaren knelpunten op te lossen. Zie de onderdelen [Introductie][5], [Werking van het stelsel][6] en [Samenwerkfuncties][4].

Informatie
-------------

Deze laag bevat architectuurcomponenten die relevant zijn voor het maken van de architectuur, waarin de aspecten van informatie (zoals begrippen en informatiemodellen) in balans worden gebracht met de afgesproken diensten. (bron: NORA)

De NORA schrijft dat deze laag architectuurcomponenten bevat zoals begrippen en informatiemodellen en het in balans brengen daarvan met de afgesproken diensten.

De afgesproken diensten zijn nodig voor de uitvoering van [Samenwerkfuncties][4] en worden door de organisaties aangeboden. De diensten maken gebruik van [Samenwerkpatronen][7]. Met de Samenwerkpatronen kan immers invulling gegeven worden aan [Samenwerkfuncties][4] en met de Samenwerkfuncties aan het [Samenwerkproces][3]. Naast de door organisaties aangeboden diensten zijn er centrale diensten, de [Stelselvoorzieningen][8]. Deze zijn nodig binnen de federatie om de complexiteit voor afzonderlijke aangesloten organisaties te verminderen.

Om onderling federatief en effectief te kunnen samenwerken zijn informatiemodellen opgesteld per functie en een [Begrippenmodel][10]. Hoe we hier binnen het Afsprakenstelsel mee werken is vastgelegd in [Afspraken][9]. Zo eenvoudig is de architectuurinformatielaag van het Afsprakenstelsel. Dat is ook nodig omdat in een stelsel met zoveel organisaties eenvoud en complexiteitreductie essentieel is.

### Bounded context  
Binnen het Jeugd-, Zorg- en Veiligheidsdomein is er sprake van één bounded context.

Een bounded context is een duidelijk afgebakend gebied waarin begrippen, afspraken en logica eenduidig en consistent zijn gedefinieerd. Alles wat binnen die grens valt, gebruikt dezelfde begrippen en modellen, maar buiten die context kunnen termen en implementaties anders zijn. Bounded context is een concept uit “Domain Driven Design”. Daarin wordt gesteld dat het onderkennen van bounded contexten belangrijk is omwille van consistentie en duidelijkheid van begrippen, isolatie van modellen, afstemming bedrijfsdoelen, beheersing van complexiteit en autonomie van partijen.

Binnen de bounded context is het domeinmodel consistent, wordt een gemeenschappelijke taal gesproken en kan onafhankelijk van andere contexten worden ontwikkeld en onderhouden. Onder het domeinmodel verstaan we de kernconcepten en hun onderlinge relaties en bijbehorende termen, definities en (business) regels. Deze zijn binnen het domein gelijk voor iedereen en vormen de basis voor het ontwerp (en implementatie) van oplossingen.

![Alt text]({{ site.baseurl }}/assets/bc.png)

Omdat uitgegaan wordt van één gezamenlijk proces, waarbij services gelijk zijn, ongeacht de serviceprovider, kan uitgegaan worden van één begrippenkader en één data model. Dit resulteert in één conceptueel en logisch model waarin entiteiten, relaties en betekenissen gelijk zijn. Binnen de bounded context wordt gebruik gemaakt van dezelfde definities en (business) regels.

Als toestandsveranderingen zich voordoen moet het domein op de hoogte worden gebracht. Dat betekent dat er sprake is van gebeurtenisgedrevenheid. Relevante toestandsveranderingen kunnen worden gebracht (push) via meldingen en notificaties, of gehaald via (pull) services. Beide varianten moeten worden ondersteund.

Daarbij geven basisprincipes uit moderne concepten als data-mesh aan dat de verantwoordelijkheid voor gegevens klip-en-klaar dienen te zijn. Dat geldt ook voor de data-lineage en herkomst van gegevens. Van gegevens moet altijd de context bekend zijn. Gegevens ontstaan in de context van een bedrijfsproces. Om die als informatie betekenisvol te kunnen hergebruiken en begrijpen in de samenwerking moeten ze eenduidig zijn. Uniforme begrippen zijn daarvoor onontbeerlijk. Dat gaat verder dan een woordenlijst: het gaat om de relaties tussen begrippen, op het niveau van professionals.  

Gegevensbescherming is daarbij “by design” in het platform ingebed. Dit gaat verder dan onderlinge convenanten. De gegevensbescherming is ‘by design’ ingebed in de architectuur op het niveau van de professional, zijn taak, informatiebehoefte en doelbinding, en om wille van privacy leveren datadiensten voor sturing, informatie die niet herleidbaar zijn naar natuurlijke personen.

De bronhouder en oorspronkelijke dienstverlener verschuift zijn aandacht van aansluiten op de keten naar het proactief en dienstverlenend beschikbaar stellen voor samenwerken. De ketenpartners zorgen voor het duurzaam beschikbaar houden, notificeren, ter inzage bieden en archiveren van informatie in het belang van de samenwerking. Archivering heeft een sterke relatie met bewaartermijnen. Daarbij kan het zo zijn dat verschillende organisaties of afdelingen verschillende bewaarregimes hanteren of wettelijk gezien moeten hanteren. Dit omdat gegevens in een bepaalde context vernietigd of juist gearchiveerd moeten worden. Verder geldt dat verschillende sectoren onderworpen kunnen zijn aan verschillende wettelijke bewaar- en vernietigplichten.

De architectuur moet rekening houden dat gegevens domein overschrijdend gebruikt moeten kunnen worden. Een organisatie zal immers te maken kunnen hebben met meerdere domeinen. Voor een aantal organisaties zal dit eerder standaard zijn dan de uitzondering. Dat doen we door gegevens met context en betekenis te kunnen leveren, de ontkoppeling van data en processen, door het gebruik van standaarden en het gebruik van standaard koppelvlakken.

### Consistentie van gegevens  
Gedistribueerde systemen, zoals waar in het Jeugd Zorg en Veiligheidsdomein sprake van is, zullen moeten beslissen welke mate van consistentie van gegevens gehanteerd wordt of wenselijk is. In het Afsprakenstelsel gaan we er van uit dat gegevens niet strikt consistent kunnen zijn. Tenslotte kan het zo zijn dat gegevens niet tijdig zijn aangepast door alle deelnemende organisaties, bijvoorbeeld door een bepaalde verwerkingstijd of downtime van services. Zie CAP-theorema; In deze theorie wordt gesteld dat in een gedistribueerd systeem twee van de drie volgende eigenschappen tegelijkertijd gegarandeerd kan worden: Consistentie (C), Beschikbaarheid (A), Partitietolerantie (P), waarbij een gedistribueerd systeem altijd partitietolerant dient te zijn. Daarom is het uitgangspunt dat er sprake moet zijn van uiteindelijke consistentie, waarbij tijdelijke inconsistenties worden toegestaan, maar dat gegarandeerd wordt dat alle deelnemers uiteindelijke dezelfde gegevenswaarden zullen hebben. 

Om consistentie in het gedistribueerde systeem te beheersen, worden verschillende technieken toegepast:
- Gebeurtenis gestuurde communicatie: Gebruik van asynchrone berichtgeving om gegevenswijzigingen tussen services te propageren.
- Gebeurtenis stores: Door het opslaan van onwijzigbare (immutable) gebeurtenissen ontstaat een centrale, gezaghebbende bron van alle gebeurtenissen. De tijdlijn van events is altijd consistent, uitgaande dat events als atomaire transacties worden aangeboden aan de store. Het voordeel is dat deze tijdlijn direct een audittrail betreft. Het kunnen opvragen van events zorgt tevens voor een “replay” mogelijkheid, waardoor eventuele inconsistenties kunnen worden opgelost.
- CQRS (Command Query Responsibility Segregation): Scheiding van lees- en schrijfoperaties om consistentie-uitdagingen te verminderen. CQRS maakt het mogelijk om geoptimaliseerde query’s (al dan niet vooraf gedefinieerd) te draaien voor bepaalde use cases.
- Compenserende transacties: Implementatie van logica om inconsistenties te corrigeren wanneer ze worden gedetecteerd.

Bij het bevragen van verschillende services, in het JZV-domein, kan niet worden gegarandeerd dat een strikt consistent beeld wordt afgegeven. Het gevolg van een dergelijke “uncommitted read” is dat bij bevraging van verschillende bronnen een inconsistent beeld kan bestaan. De voorraad aan events (al dan niet verwerkt bij ketenpartners) echter geeft een consistent beeld.

Applicatie
-------------

NORA geeft aan dat de applicatielaag beschrijft met welke methoden en standaarden invulling gegeven wordt aan de applicatie\-architectuur.

De standaarden zijn beschreven in het onderdeel Principes en standaarden. Een van de methoden waarmee invulling gegeven wordt aan de applicatie-architectuur is het Afsprakenstelsel zelf. Daarbij zijn de Besturingsrollen en Organisatorische rollen van belang, maar in de context van de architectuur vooral ook de Technische rollen. In onderstaande figuur zijn deze schematisch weergeven.

![Alt text]({{ site.baseurl }}/assets/rollen.png)

### Aanbieden en afnemen systeemrollen  
Er zijn de rollen van aanbieden en afnemen. Het zijn de deelnemende organisatie die informatie aanbieden, maar ook kunnen afnemen van andere organisaties. Hiervoor worden de Samenwerkpatronen en Standaarden gebruikt. Organisaties dienen deze patronen en standaarden te ondersteunen alsmede het informatiemodel en begrippenkader. Wat daarvoor nodig is kan worden nagegaan via het onderdeel Aansluiten en Impactbepaling.

De zaaksystemen / dossiersystemen / primaire processystemen van de organisaties zijn van belang voor deze rol en van nog groter belang is de data (zie Informatielaag) welke deze verwerken. Vanuit architectuur bezien is ontkoppeling van werkprocessen, applicaties en data het uitgangspunt (zie Common Ground). Wanneer dit goed is ingevuld kan data eenvoudig beschikbaar gesteld worden aan de eigen systemen en die van andere organisaties waar toegestaan.

Andersom moeten de zaaksystemen / dossiersystemen / primaire processystemen van de organisatie data kunnen bevragen bij de bron. Ook moeten ze zorgen dat data op een juiste wijze wordt opgeslagen in de datalaag, denk aan de kwaliteit van de data, aan metadatering, etc.

### Vertrouwenssysteemrollen  
Er is sprake van samenwerking in een federatief verband. Bij federatie speelt vertrouwen een belangrijke rol. Er zijn daarom vertrouwenssysteemrollen en voorzieningen. Organisaties zijn zelf verantwoordelijk voor authenticatie en autorisatie, echter zijn er rollen die zorgen voor waarborgen zoals de ledenaministrator en verzekeraar betrouwbaarheid, maar zijn er ook rollen waar voorzieningen worden geleverd zoals vanuit de vertrouwensleverancier (PKIoverheid, maar denk ook aan leverancier voor IDP-lokalisatie) en bevoegde uitgever (van attesten en tokens). Zie onderdeel Toegang en Policy-based Access Control.

### Beheersysteemfuncties  
Naast de stelselbeheerder welke technische rollen toekent, zijn er ketenvoorzieningbeheerders welke de ketenvoorzieningen leveren. Er zijn verschillende typen ketenvoorzieningen:
- Voorzieningen voor lokalisatie (vindbaarheid)
- Voorzieningen voor aanleveren en ophalen van gebeurtenissen (connectiviteit en uitwisseling)
- Voorzieningen voor transformatie, o.a. van oude (estafette) naar nieuwe (netwerk) model (de zogenoemde Sylvester dienst(en))

Opmerking: "Sylvester" is een andere naam voor Oudejaarsavond, de dag voor Nieuwjaarsdag (31 december). De term is vernoemd naar Paus Silvester I, wiens feestdag op 31 december valt.

De ketenvoorzieningen vullen de intermediaire functie in zoals gedefinieerd binnen Common Ground. Zie navolgende figuur (bron: VNG).

![Alt text]({{ site.baseurl }}/assets/comg1.png)

Merk op dat REST-API verkeer volledig decentraal verloopt, dat wil zeggen zonder dat er hiervoor ketenvoorzieningen nodig zijn. Slechts een optionele ketenvoorziening, de API catalog, speelt hier een rol voor de vindbaarheid van REST-API. Beter gesteld de vindbaarheid van de decentrale API Catalogs / DevPortals want daarnaar verwijst de keten API Catalog. Deze decentrale opzet is mogelijk zonder dat complexiteit voor organisaties ontstaat, sterker nog het reduceert deze. Verder sluit deze benadering aan bij de keuze en wens: afspraken voor standaarden en standaarden voor diensten.

Bij de uitwisseling van gebeurtenissen is wel sprake van een ketenvoorziening, namelijk om gebeurtenissen aan te leveren dan wel op te halen, zie onderdeel Techniek.  Deze voorziening is nodig:
- om adressering complexiteit te reduceren, anders zou elke organisatie zich afzonderlijk moeten kunnen abonneren op channels/topics bij elke andere organisatie in het stelsel
- omdat anders elke organisatie gebeurtenissen afzonderlijk zou moeten persisteren en bevraagbaar moeten maken
- omdat anders elke organisatie complexe onweerlegbare vastlegging van gebeurtenissen persistentie en provenance zou moeten kunnen leveren
- het aan elkaar relateren van gebeurtenissen anders gedistribueerd zou moeten plaatsvinden wat een hoge complexiteit kent.

Het wil niet zeggen dat organisaties dit niet zelf kunnen. Zeker organisaties met een interne of externe ICT-dienstverlener van hoge kwaliteit en met hoog kennisniveau zouden dit kunnen invullen, echter maakt de inzet van een ketenvoorziening het voor alle partijen een stuk eenvoudiger en minder complex. Dit is essentieel gelet het aanzienlijk aantal partijen in het domein en de wisselende omvang en expertise niveau van de gerelateerde ICT-dienstverleners.

IT-infrastructuur
-------------

NORA geeft aan dat de IT-infrastructuurlaag beschrijft met welke methoden en standaarden invulling gegeven wordt aan het fysieke transport van digitale gegevens (data) binnen het stelsel.

Gelet het aantal organisaties binnen het stelsel en de diversiteit daarin wordt het fysieke transport gerealiseerd via het internet en de daaraan gelieerde standaarden, zoals TCP/IP, HTTPS, etc. Voor transport over de fysieke netwerkdrager wordt FSC gebruikt (voor vercijferd transport op basis van contracten).

Elke organisatie beschikt over een eigen IT-infrastructuur. Deze zullen op verschillende manieren zijn ingericht, wat ook geen probleem is zolang deze maar compatibel zijn met de standaarden en afspraken.

Bepaalde ketenvoorzieningen zouden als onderdeel van de IT-infrastructuurlaag gezien kunnen worden, met name in het kader van het fysiek transport van digitale gegevens (CORV2). Omdat CORV2 echter meer levert dan transport is deze gepositioneerd binnen de applicatielaag.

Decentraal kunnen organisaties beschikken over Firewalls, Web Application Firewalls, Proxies, Reverse Proxies, API Gateways, API Management oplossingen, ebMS Gateways, IDP’s, etc. Deze vallen onder de architectuur van de betreffende organisaties en beschrijving daarvan is hier niet wenselijk en nodig.

Common Ground
-------------

Common Ground draait in de kern om een structurele hervorming van de gemeentelijke informatievoorziening, door op een andere manier om te gaan met gegevens. De basisgedachte van Common Ground is:
- data worden losgekoppeld van werkprocessen en applicaties;
- data worden bevraagd bij de bron, in plaats van ze veelvuldig te kopiëren en op te slaan.

Om dit te realiseren, werken partijen samen op basis van vier uitgangspunten:
- gegevens worden uniform gemaakt;
- gegevens worden opgehaald met API’s;
- er wordt gewerkt met één gemeenschappelijke integratielaag;
- data blijven in de bron.

Centraal staat het onderscheid tussen dienstafnemers en dienstenaanbieders. Data is ontkoppeld van diensten en van procesinrichting (en dus ook van applicaties) waardoor eveneens van interactie. Communicatie tussen dienstafnemers en dienstenaanbieders vindt plaats via een intermediair. Zie onderstaande figuur (bron: VNG).

![Alt text]({{ site.baseurl }}/assets/comg2.png)

Navolgende figuur (bron: VNG) schetst dit in meer detail. Zie voor informatie de site van de VNG rond Commond Ground.

![Alt text]({{ site.baseurl }}/assets/comg3.png)


[1]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-24-werking.html#grondslagen
[2]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-24-werking.html#juridische-kaders
[3]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-24-werking.html#samenwerkingsproces
[4]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-24-werking.html#samenwerkfuncties
[5]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-23-intro.html
[6]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-24-werking.html
[7]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-27-samenwerkpatronen.html
[8]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-29-ketenvoorzieningen.html
[9]: https://samen-onder-handbereik.github.io/afsprakenstelsel/jekyll/2025-09-30-afspraken.html
[10]: https://samen-onder-handbereik.github.io/afsprakenstelsel/others/begrippenkader/
