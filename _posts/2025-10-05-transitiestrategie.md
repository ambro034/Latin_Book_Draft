---
title: Transitiestrategie en pad
author: lg
date: 2025-10-05
category: Jekyll
layout: post
---

> ##### Concept
{: .block-danger }

Strategie
-------------
**Inleiding**  
De benodigde transitie is niet alleen technisch, maar raakt het hele paradigma van gegevensuitwisseling en samenwerking.

De kern van de transitie is de beweging **van een estafettemodel naar een netwerkmodel**.

In het huidige estafettemodel wordt informatie stap voor stap doorgegeven in een keten. Elke partij ontvangt berichten, voegt eigen informatie toe, slaat deze lokaal op en stuurt het geheel door naar de volgende partij. Dit is sterk procesgedreven en lineair ingericht, met berichtenverkeer volgens vaste protocollen en volgordes. De gewenste situatie – het netwerkmodel – doorbreekt dit principe fundamenteel. In plaats van informatie door te geven, blijft informatie bij de bron en wordt deze gedeeld via het netwerk. Partijen raadplegen elkaars gegevens rechtstreeks, op basis van autorisatie, in plaats van kopieën te ontvangen en door te sturen. Daarmee verandert de aard van informatievoorziening van “doorgeven” naar “beschikbaar stellen en raadplegen”.

Als dit nader geanalyseerd wordt, kan de transitie verder geconcretiseerd worden in een aantal samenhangende verschuivingen:
- Ten eerste is er een verschuiving van ketengerichte processen naar netwerkgerichte samenwerking. In het estafettemodel is de keten leidend en bepaalt de volgorde van berichten het proces. In het netwerkmodel bestaat geen vaste volgorde meer; partijen kunnen informatie ophalen wanneer nodig, wat leidt tot meer flexibiliteit en gelijktijdigheid in samenwerking.
- Ten tweede verschuift de informatiepositie van kopieën naar bronregistraties. In het netwerkmodel houdt elke deelnemer een eigen register bij, en andere partijen raadplegen die direct. Dit voorkomt duplicatie en inconsistentie en maakt het mogelijk om altijd met actuele gegevens te werken.
- Ten derde verandert de manier van integratie. De site benoemt expliciet dat organisaties moeten bewegen richting halen bij de bron, REST-API-architecturen en event-driven werken. Tegelijk wordt het gebruik van traditionele berichtprotocollen zoals ebMS geleidelijk uitgefaseerd.  
Dit betekent concreet een transitie van batch- en berichtgebaseerde koppelingen naar API’s, services en gebeurtenissen.
- Ten vierde ontstaat een verschuiving van bilaterale koppelingen naar een gedeeld stelsel met generieke afspraken. In plaats van dat elke koppeling apart wordt afgesproken, biedt het afsprakenstelsel uniforme regels, rollen en standaarden die voor alle deelnemers gelden. Dit maakt one-to-many interactie mogelijk in plaats van one-to-one integraties.
- Ten vijfde verandert de interactievorm tussen organisaties. Naast het klassieke “opdracht”-patroon uit het estafettemodel, introduceert het netwerkmodel aanvullende patronen zoals inzage (direct raadplegen) en notificaties (gebeurtenissen).  
Hiermee verschuift de samenwerking van asynchroon berichtenverkeer naar een mix van synchroon (raadplegen) en event-driven communicatie.
- Ten zesde wordt de rol van de burger en ketenregie versterkt. Doordat informatie centraal inzichtelijk wordt (bijvoorbeeld via registers en inzage), ontstaat meer transparantie en kan de burger of professional beter regie voeren over het proces en de gegevens.

Deze transitie vindt incrementeel plaats. Het netwerkmodel wordt niet in één keer gerealiseerd, maar stap voor stap opgebouwd via registers en stelselvoorzieningen, waarbij het afsprakenstelsel steeds wordt uitgebreid.

Samengevat vraagt het Afsprakenstelsel dus om een meervoudige transitie: van lineaire ketens naar een dynamisch netwerk, van berichten naar API’s en events, van kopieën naar brondata, van bilaterale afspraken naar een gedeeld stelsel, en van procesgedreven uitwisseling naar informatiegedreven samenwerking. Dit is een fundamentele herinrichting van zowel de technische architectuur als de manier waarop organisaties samenwerken.

**Aanleiding en richting**  
De transitie van het estafettemodel naar het netwerkmodel is geen klassieke moderniseringsopgave, maar een fundamentele heroriëntatie op hoe organisaties informatie delen en samenwerken. Waar het huidige model uitgaat van lineaire overdracht van informatie via bilaterale koppelingen, verschuift de gewenste situatie naar een dynamisch netwerk waarin informatie bij de bron blijft en opvraagbaar is voor bevoegde partijen. Deze beweging raakt niet alleen de technische inrichting, maar ook governance, samenwerking en de manier waarop organisaties hun rol in het geheel begrijpen.

Het transitieplan vertrekt daarom vanuit een gedeelde visie: een toekomst waarin informatie duurzaam, betrouwbaar en gecontroleerd beschikbaar is, en waarin organisaties gezamenlijk verantwoordelijkheid dragen voor het functioneren van het netwerk. Die visie moet niet abstract blijven, maar vertaald worden naar concrete perspectieven voor bestuurders, professionals en technici. Alleen wanneer zichtbaar wordt hoe het netwerkmodel bijdraagt aan betere dienstverlening, lagere complexiteit en grotere wendbaarheid, ontstaat de basis voor daadwerkelijke beweging.

**Bestuurlijk draagvlak en gezamenlijke ambitie**  
De eerste stap in de transitie ligt in het organiseren van bestuurlijk commitment dat verder gaat dan formele instemming. Bestuurders moeten zich expliciet verbinden aan de richting van het netwerkmodel en de implicaties daarvan accepteren. Dat betekent dat zij bereid moeten zijn om te investeren in generieke voorzieningen, om bestaande werkwijzen ter discussie te stellen en om ketenbelangen zwaarder te laten wegen dan het optimaliseren van de eigen organisatie.

Dit vraagt om een zorgvuldig opgebouwd verhaal waarin urgentie en perspectief samenkomen. De beperkingen van het estafettemodel moeten herkenbaar zijn, bijvoorbeeld in de vorm van inefficiënte koppelingen, vertraagde processen en inconsistentie van gegevens. Tegelijkertijd moet duidelijk worden wat het netwerkmodel oplevert: snellere samenwerking, betere datakwaliteit en een fundament voor toekomstige ontwikkelingen. Het helpt om deze baten niet alleen rationeel te onderbouwen, maar ook zichtbaar te maken in concrete casussen en praktijkvoorbeelden.

Bestuurlijk draagvlak krijgt pas echt betekenis wanneer het wordt vertaald naar sturing. Dat betekent dat de transitie wordt verankerd in strategie, dat middelen beschikbaar worden gesteld en dat er actief wordt gestuurd op voortgang en samenhang. Zonder deze verankering bestaat het risico dat de transitie blijft hangen in losse initiatieven.

**Fundament: modernisering van de informatievoorziening**  
Parallel aan het creëren van draagvlak moeten organisaties hun technologische basis op orde brengen. De beweging naar het netwerkmodel sluit aan bij ontwikkelingen die al langer gaande zijn, zoals het werken met REST-API’s, het toepassen van event-driven architectuur en het hanteren van principes als data bij de bron en Common Ground. Deze ontwikkelingen vormen de bouwstenen van het netwerkmodel en zijn daarmee geen optionele verbeteringen, maar noodzakelijke voorwaarden.

In deze fase ligt de nadruk op het ontsluiten van bestaande systemen via gestandaardiseerde API’s en het inrichten van API-managementvoorzieningen. Dit gaat verder dan techniek alleen; het raakt ook governance, omdat afspraken nodig zijn over gebruik, beveiliging en lifecycle management. Tegelijkertijd ontstaat de behoefte aan functionele bouwstenen die het delen van informatie daadwerkelijk mogelijk maken, zoals voorzieningen voor inzage en autorisatie. Belangrijk in deze fase is dat organisaties niet proberen om hun volledige landschap in één keer te transformeren. Door te werken met ontkoppeling en het toevoegen van een API-laag kan stapsgewijs worden gemoderniseerd, zonder dat de continuïteit van bestaande processen in gevaar komt. Deze incrementele aanpak maakt het mogelijk om snel waarde te realiseren en tegelijkertijd ervaring op te bouwen.

**Implementatie van het Afsprakenstelsel**  
Met een gemoderniseerd fundament kunnen organisaties het Afsprakenstelsel gaan implementeren. Dit stelsel biedt de gemeenschappelijke taal en spelregels die nodig zijn om als netwerk te functioneren. Het invoeren daarvan betekent dat organisaties hun processen, gegevensmodellen en interacties toetsen aan de afgesproken kaders en waar nodig aanpassen. De implementatie vraagt om een iteratieve benadering waarin leren centraal staat. Standaarden en afspraken krijgen pas betekenis in de praktijk en zullen zich verder ontwikkelen op basis van ervaringen. Het is daarom belangrijk dat organisaties actief bijdragen aan deze ontwikkeling en niet wachten tot alles volledig is uitgekristalliseerd.

Stelselvoorzieningen spelen hierbij een cruciale rol. Door generieke functies centraal te organiseren, wordt voorkomen dat elke organisatie zelf oplossingen ontwikkelt voor dezelfde vraagstukken. Het gebruik van deze voorzieningen vraagt vertrouwen, maar ook actieve betrokkenheid, zodat zij blijven aansluiten bij de behoeften van de deelnemers.
 
**Aansluiten en deelnemen aan het netwerk**  
Het moment waarop een organisatie aansluit op het Afsprakenstelsel markeert een belangrijke overgang. De organisatie committeert zich aan de gezamenlijke afspraken en maakt haar informatie beschikbaar binnen het netwerk. Dit vraagt niet alleen technische aansluiting, maar ook organisatorische inbedding. Rollen en verantwoordelijkheden veranderen. Er ontstaat een expliciete verantwoordelijkheid voor het beheren en beschikbaar stellen van brondata, voor het borgen van kwaliteit en voor het naleven van afspraken. Tegelijkertijd moeten nieuwe competenties worden ontwikkeld, zoals API-design, datagovernance en ketensamenwerking. Aansluiting betekent ook dat een organisatie deel wordt van een ecosysteem waarin samenwerking centraal staat. Dit vraagt om een andere houding, waarin niet alleen wordt gekeken naar de eigen belangen, maar ook naar de impact op het geheel.

**Gefaseerde invoering van samenwerkfuncties**  
Na aansluiting verschuift de focus naar het daadwerkelijk benutten van het netwerkmodel door het implementeren van samenwerkfuncties. Deze functies maken het mogelijk om informatie te delen, processen op elkaar af te stemmen en gebeurtenissen uit te wisselen. De invoering hiervan gebeurt gefaseerd, omdat zij direct ingrijpt op bestaande systemen en werkwijzen. Zaak- en dossiersystemen moeten worden aangepast om informatie beschikbaar te stellen via API’s en om te kunnen reageren op gebeurtenissen. Dit vraagt om een architectuur die gericht is op modulariteit en flexibiliteit, zodat veranderingen beheerst kunnen worden doorgevoerd.

In deze fase wordt de meerwaarde van het netwerkmodel zichtbaar. Door samenwerkfuncties toe te passen in concrete processen ontstaat ervaring en vertrouwen, wat de basis vormt voor verdere opschaling.

**Verandering van cultuur en werkwijze**  
Naast technische en organisatorische veranderingen is er sprake van een diepgaande cultuurverandering. Het netwerkmodel vraagt om een andere manier van denken over informatie, waarin delen de norm wordt en eigenaarschap een andere invulling krijgt. Informatie wordt niet langer gezien als bezit, maar als een gemeenschappelijke bron die onder voorwaarden toegankelijk is. 
Dit vraagt om aandacht voor de menselijke factor. Medewerkers moeten nieuwe vaardigheden ontwikkelen en wennen aan andere manieren van werken. Verandermanagement speelt hierin een cruciale rol. Het gaat om het creëren van begrip, het bieden van ondersteuning en het stimuleren van experimenteren en leren. Leiderschap is hierin bepalend. Wanneer leidinggevenden het gewenste gedrag niet actief uitdragen, zal de transitie stagneren. Het is daarom belangrijk dat zij zichtbaar betrokken zijn en ruimte creëren voor verandering.

**Risico’s en beheersing**  
De transitie naar het netwerkmodel kent verschillende risico’s. Een belangrijk risico is dat de beweging blijft steken in technische initiatieven zonder dat de organisatie daadwerkelijk verandert. Ook bestaat het gevaar van fragmentatie, waarbij verschillende partijen het model op hun eigen manier invullen, waardoor nieuwe vormen van incompatibiliteit ontstaan. Daarnaast kan weerstand ontstaan vanuit bestaande belangen en structuren. De transitie kan leiden tot verschuivingen in verantwoordelijkheden en budgetten, wat spanning kan veroorzaken. Technisch gezien liggen er risico’s in beveiliging, performance en afhankelijkheid van centrale voorzieningen. Deze risico’s vragen om actieve sturing, duidelijke governance en continue monitoring. Door transparant te zijn over voortgang en knelpunten en door tijdig bij te sturen, kunnen problemen worden voorkomen of beperkt.
 
**Kansen en baten**  
Tegenover de risico’s staan aanzienlijke kansen. Het netwerkmodel maakt het mogelijk om sneller en flexibeler samen te werken, doordat informatie direct beschikbaar is. Het vermindert de complexiteit van koppelingen en verhoogt de kwaliteit van gegevens, doordat er gewerkt wordt met broninformatie.

Voor burgers en bedrijven leidt dit tot een betere dienstverlening, waarin gegevens niet steeds opnieuw hoeven te worden aangeleverd en processen beter op elkaar aansluiten. Voor organisaties betekent het een grotere wendbaarheid en een fundament voor verdere digitalisering en innovatie.

**Naar volledige participatie en doorontwikkeling**  
De transitie eindigt niet bij aansluiting of implementatie van samenwerkfuncties. Het netwerkmodel is een continu evoluerend geheel waarin deelnemers gezamenlijk verantwoordelijkheid dragen voor doorontwikkeling. Naarmate meer organisaties deelnemen en meer functies worden toegevoegd, groeit de waarde van het netwerk. Volledige participatie betekent dat organisaties niet alleen gebruik maken van het netwerk, maar er ook actief aan bijdragen. Dit vraagt om blijvende investering in samenwerking, innovatie en governance.

De transitie van estafettemodel naar netwerkmodel is daarmee geen project met een einddatum, maar een beweging die zich over jaren ontwikkelt. Het succes ervan hangt af van het vermogen om techniek, organisatie en cultuur in samenhang te veranderen en om gezamenlijk te blijven leren en verbeteren.

Transitiepad
-------------

### Transitiefasen
De transitie laat zich schetsen aan de hand van enkele fasen zoals in onderstaande figuur afgebeeld.

![Alt text]({{ site.baseurl }}/assets/tpad.png)

### A Initiatiefase
**Bestuurlijk commitment**  
Organisatie hebben de afgelopen periode meegedacht en meegewerkt aan het Jeugd, Zorg en Veiligheid - Samen onder Handbereik Afsprakenstelsel. Hiervoor was reeds bestuurlijk commitment vanuit de verschillende organisaties. Voor de transitie is bestuurlijk commitment nog van een veel groter belang. Transitie vraagt immers inspanning. Die inspanning moet leiden tot de beoogde baten.
Om de transitie en de implementatie van het Afsprakenstelsel in gang te zetten en de baten daarvan te gaan oogsten is de wil van organisatie nodig hier een succes van te maken, het belang te onderkennen, er voldoende prioriteit aan toe te kennen naast alle andere prioriteiten en funding beschikbaar te maken. De realisatieteams zullen dit hard nodig hebben om efficiënt te kunnen leveren. Dit zal als eerste binnen het transitie-pad geregeld moeten zijn, uitgesproken moeten worden en bekend moeten zijn. Zodat de transitie met wind in de rug en vaste grond onder de voeten kan starten.

Valkuil: vaag, mager, zwak en/of laat invullen van het bestuurlijk commitment

Succesfactoren: duidelijke prioriteit toekennen, funding beschikbaar stellen en communiceren van belang en commitment vanuit de organisatieleiding 

Direct hierop volgend start de transitie met de initiatie van een aantal sporen tegelijkertijd:
-	Modernisering van de informatievoorziening en ICT-infrastructuur
-	Implementatie van het Afsprakenstelsel
-	Verandering van cultuur en werkwijze

**Modernisering van de informatievoorziening en ICT-infrastructuur**  
De meeste organisaties zijn al bezig hun ICT-infrastructuur geschikt te maken om de nieuwe era van gedistribueerde ICT landschappen waar informatie gedeeld wordt en wordt samengewerkt en daarbij gebruik gemaakt wordt van REST-API en event driven architectuur benaderingen. Hierop kan worden aangesloten als dergelijke vernieuwingen al lopen. Als dat nog niet het geval is kan deze transitie deze vernieuwing triggeren.
In de meeste gevallen zijn infrastructurele voorzieningen en vernieuwingen nodig zoals het implementeren van API Management oplossingen inclusief DevPortals/API-Catalogs, het veilig toegankelijk maken van API’s vanuit het internet (naast API Management oplossingen vraagt dit ook aanpassingen in de internet koppelingen), het kunnen bevragen en benutten van informatie vanuit het stelsel in de eigen systemen, het kunnen leveren van informatie uit de eigen systemen en/of data aan ketenpartners, etc.
Het verdient aanbeveling dergelijke vernieuwingen geleidelijk in een ‘just-in-time’ en ‘just-enough’ te doen en niet eerst een veel omvattende technische implementatie te doen en daarna pas groen licht te geven voor verdere ontwikkelingen. Zo kunnen de eerste Samen onder Handbereik functies al met beperkte infrastructurele aanpassingen worden gerealiseerd.

Valkuil: allesomvattende langdurige en kostbaar infrastructurele aanpassingen te doen en daarna pas vervolgstappen (waaruit dan pas, en te laat, feedback en inzichten ontstaan)

Succesfactoren: inrichten van de vereisten die nodig zijn om te starten en die geleidelijk uit te bouwen naar wat vanuit  brede ontwikkelingen en Samen onder Handbereik nodig zijn in de volledigheid

**Implementatie van het Afsprakenstelsel**  
De implementatie van het Afsprakenstelsel richt zich op de inrichting van de rollen die nodig zijn om het stelsel te laten functioneren, maar ook het deelnemen als organisatie en het implementeren van de afspraken die daarin meekomen. 

Valkuil: alleen focussen op centrale of decentrale rollen

Succesfactoren: inrichten en invullen van de rollen, ook de deelnemersrol

**Verandering van cultuur en werkwijze**  
Het Samen onder Handbereik Afsprakenstelsel vereist een en ander in de techniek, maar veel belangrijker nog ook veel op het vlak van werkprocessen, werkwijzen en organisatiecultuur. Er ontstaan in potentie enorme voordelen en mogelijkheden voor zowel professionals als burgers. Die zijn alleen te realiseren als er draagvlak is, de wil om de transitie een kans te geven, maar ook goede communicatie, begeleiding, bijsturen waar dat nodig is, luisteren naar feedback vanuit de werkvloer en daar wat mee doen. De transitie is vooral ook een verandertraject.

Valkuil: belang van het meenemen van organisatie en werkvloer onderschatten en/of het niet acteren op feedback vanuit de uitvoeringskant

Succesfactoren: nadrukkelijk aandacht besteden aan transitie en transitie effecten op werkprocessen, werkwijzen en organisatiecultuur, maar ook op communicatie en het benutten van de aanwezig kennis in de uitvoering

 
### B Fase van testen, leren en bijsturen
Deze fase is van niet te onderschatten belang. Merk op dat deze fase nadrukkelijk kort op de start van de initiatie fase is geschetst. Veel transitie- en ICT trajecten falen omdat er te lang vanuit een onderwerpfase wordt gedacht en het idee dat alles is te voorzien en vooraf doordacht kan worden. Ook speelt dat vaak pas groen licht geven wordt voor bouw en test trajecten als allerlei onderwerpen en zorgen uitvoerig zijn besproken, er consensus over is bereikt en oplossingen zijn beschreven, zonder dat dit nodig en verstandig is. De nadelen daarvan zijn aanzienlijk, sterker een dergelijke aanpak komt met aanzienlijke risico’s omdat deze te theoretisch is, belangrijke leermomenten ontbreken, feedback loops te laat ontstaan of geen kans krijgen, begrip en besef binnen de organisatie ontstaan op een moment dat er weinig meer mee gedaan kan worden om bij te sturen of te verbeteren. Kortom essentieel binnen de transitie is dat organisaties snel en vrijwel direct beginnen te bouwen, beproeven en testen zodat ze tijdig kunnen leren en bijsturen.

Valkuil: pas gaan aansluiten en testen als ‘alles’ is uitgekristalliseerd en is ‘uit-vergaderd’

Succesfactoren: snel en direct aansluiten, testem, feedback leveren en bijsturen

### C Aansluiten en invoeren
Na de test periode kan er met vertrouwen worden aangesloten op het Afsprakenstelsel en de productionele invoering van Samenwerkingsfuncties starten. Ook hier geldt dat snel starten, geleidelijk invoeren en bijsturen te prefereren is boven veel omvattende complete big-bang invoeringen.

Valkuil: wachten en half dan wel onduidelijk aansluiten en deelnemen 

Succesfactoren: formeel en volwaardig aansluiten en kleinschalig productioneel starten en uitbouwen van de Samenwerkingsfuncties

#### D. Bijsturen
In deze fase is aangesloten en zijn Samenwerkingsfuncties geimplementeerd en worden deze in de praktijk gebruikt. Dit is ook het moment om kritisch te kijken naar of de doelstellingen worden bereikt en kunnen worden bereikt, in project termen of de business case nog valide is. Tevens om na te gaan of het nodig is bij te sturen. Dit is iets dat continue over het gehele traject moet worden gedaan, toch is het ook verstandig hier ook een expliciet moment voor te plannen binnen de transitie en wellicht meer dan één. Daarin zou meer nog dan in het continue proces kritisch gekeken moet worden en extra aandacht besteed moeten worden aan kritische feedback of gemelde risico’s. Als er hier onvoldoende van beschikbaar is verdient het aanbeveling een red team review te doen waar er expliciet gezocht wordt naar zwakten, missers en risico’s in de aanpak. Het moment zoals geschetst in de illustratie is in ieder geval een goed moment om dat te doen. 

Valkuil: ‘doorhobbelen’ zonder expliciete validatie op koers, effectiviteit en behalen van delen

Succesfactoren: expliciete en herhaalde validaties inclusief red team reviews en het daarop bijsturen en dat laatste vooral niet nalaten

### E. Doorontwikkelen en operationaliseren stelsel
Nu Samenwerkingsfuncties succes zijn geïmplementeerd en baten worden gerealiseerd gaat de aandacht schuiven naar het verder professionaliseren van het stelsel en de invulling van de rollen daarin, maar ook naar het gezamenlijk doorontwikkelen van het geheel.

Valkuil: vanuit de projectmatige benadering activiteiten afronden zonder te zorgen voor een verder evoluerend geheel 

Succesfactoren: inzetten op professionalisering en gezamenlijke doorontwikkeling vanuit een PDCA benadering

### F. Invoering resterende Samenwerkingsfuncties
Doordat sprake is van een geleidelijke invoering zullen ook nog resterende Samenwerkingsfuncties ingevoerd moeten worden. Mogelijk ook nog Samenwerkingsfuncties of delen daarvan waard de leverende organisatie mogelijk zelf weinig baten bij heeft, maar andere organisaties wel.

Valkuil: focus op eigen baten en Samenwerkingsfuncties of delen daarvan die vooral voor anderen van belang zijn laten zitten / cherry picking

Succesfactoren: integrale benadering met focus op zowel individuele baten als baten voor het geheel en vooral ook doelgroepen

### G. Oogstfase
Na alle investeringen is de tijd aangebroken om de redendement binnen te laten vloeien. In deze context dus de waarde voor de proffesionals en de doelgroepen. De fase van het maximaal realiseren van baten en het vast houden en waar nodig verbeteren en optimaliseren is  aangebroken. Er kan in deze fase ook worden gekeken naar bredere samenwerking, aansluiting maken op andere stelsel (federatie van federaties) en verder standaardiseren.

Valkuil: effect van de remmende voorsprong laten ontstaan of aanjagen

Succesfactoren: bewaken van waardecreatie en optimaliseren van de werking van het stesel


> ##### Concept
{: .block-danger }

Gedeelde (domein/sector)voorzieningen 
-------------
**Inleiding**  
Binnen het Jeugd, Zorg en Veiligheidsdomein zijn er verschillende entiteiten die één rechts‑ en organisatie‑entiteit vormen, bijvoorbeeld een branchevereniging, maar waarbij sprake kan zijn van vestigingen en aangesloten organisaties die elk de eigen ICT regelen. Daarnaast komen ook landelijke sectoren van regionale organisaties voor, die ook elk de eigen ICT regelen. In sommige gevallen wordt er op bepaalde gebieden samengewerkt, denk aan het doen van gezamenlijke inkoop, hanteren van een dezelfde processen en het gebruiken van dezelfde zaaksystemen etc.

In deze gevallen zou gesproken kunnen worden van een domein waar gelijksoortige organisaties, soms vallend onder één rechts‑ en organisatie‑entiteit of één landelijke sectore, in de context van Samen onder Handbereik allemaal dezelfde technische koppelingen en bijbehorende beveiligingsmaatregelen moeten realiseren. Voor elke afzonderlijke organisatie kan dat ingewikkeld, kostbaar en moeilijk onderhoudbaar zijn. Het zou ook mogelijk te zijn de krachten te bundelen en gebruik te maken van gedeelde voorzieningen. Dit zou sterk vereenvoudigend kunnen werken, kosten kunnen verlagen, drempelwerking voorkomen en implementatie van het Samen onder Handbereik netwerkmodel binnen een korte tijd mogelijk maken.

Binnen dit type domeinen zouden twee scenario’s gevolgd kunnen:

- Scenario 1: elke organisatie regelt zelf de technische koppelingen en bijbehorende beveiligingsmaatregelen
- Scenario 2: een domein of sector gebruikt een gedeelde voorziening voor het realiseren van technische koppelingen en bijbehorende beveiligingsmaatregelen

De elementen die via een gedeelde voorziening zouden kunnen worden geregeld zijn vooral de generieke elementen, het gaat dan om:
- technische koppelingen naar de API’s van de partijen binnen het domein of de sector
- de beveiligingsmaatregelen voor de afscherming van de achterliggende systemen van die partijen
- generieke elementen in de toegangsverlening tot de systemen en API’s  van de partijen binnen het domein of de sector

Om een beeld te hebben van de potentiële voordelen en baten worden beide scenario’s hieronder geschetst.

**Scenario 1: elke organisatie/organisatieonderdeel/vestiging/etc. voor zich**  
De algemene beweging binnen de overheid naar REST-API betekent dat elke organisatie elke andere organisatie moet kunnen bereiken en adresseren. Dat is impactvol, maar ook niet onlogisch. In de fysieke wereld kan elke organisatie elke andere organisatie ook bereiken (telefonisch, schriftelijk of door fysiek langs te gaan). Digitaal zou dat niet anders moeten zijn.

Hoewel logisch is de impact in de digitale wereld aanzienlijk, een organisatie moet zorgen dat:

- de adressen van de services van de organisatie bekend zijn (FQDN’s, DNS)
- de services benaderbaar zijn voor geautoriseerde organisaties en alle achterliggende systemen goed beschermd zijn tegen kwaadwillende actoren (d.m.v. Firewalls, IDS/IPS, Monitoring, API Gateways/API Management)
- de services voorzien van de juiste en geldige PKI certificaten
- andere organisaties zich succesvol kunnen authentiseren en geautoriseerd zijn zodat toegang verleend kan worden tot de services
- en andersom dat de organisatie ook services van andere organisaties kan benaderen

De schaal van het aantal onderlinge relaties is groot. Zie onderstaande figuur waar alleen de relaties vanuit twee organisatie(domeinen) zijn geschetst.

![Alt text]({{ site.baseurl }}/assets/domeinr.png)

Hier zijn voor eenvoud entiteiten gebundeld zoals Veilig Thuis (~25 entiteiten), Zorg- en Veiligheidshuizen (~31 entiteiten), etc. Zonder deze vereenvoudiging zou de schets nauwelijks te maken zijn. Neem de illustratie hieronder waarin één domein met slechts 10 entiteiten zou worden uitgevouwen en zou communiceren met een domein met slechts 20 entiteiten. Waarbij om tot een overzichtelijke figuur ook nog eens een groot deel van de mogelijke relaties is weggelaten.

![Alt text]({{ site.baseurl }}/assets/relaties.png)

Ten opzichte van de getallen in het Jeugd, Zorg en Veiligheidsdomein is bovenstaande figuur op zichzelf een sterke vereenvoudiging van de werkelijkheid.
Het aantal een-op-een relaties zou sterk te reduceren zijn via een knooppunt of ‘gateway’. Zie hiervoor scenario 2.

**Scenario 2: gedeelde voorziening**  
Wanneer een domein zichzelf toegankelijk zou maken via een knooppunt of ‘gateway’, zou het aantal relaties sterk reduceren. Zie onderstaande figuur.

![Alt text]({{ site.baseurl }}/assets/relatiesgw.png)

Zo’n knooppunt of ‘gateway’ noemen we hier een Gedeelde Domein Voorziening (GDV). Elk domein of sector zou zo’n gedeelde domein voorziening kunnen realiseren. Een dergelijke benadering is gelet de vereenvoudiging welke dit oplevert, dan ook sterk aangeraden.

Zeker als bedacht wordt dat in elke ‘bol’ doorgaans de volgende componenten zitten, zie navolgende figuur, en daar wijzigingen op nodig zijn, beheer en life cycle management etc.

![Alt text]({{ site.baseurl }}/assets/apimgmt.png)

Voor scenario 2 zou dit het volgende beeld geven (voorbeeld):

![Alt text]({{ site.baseurl }}/assets/metgw.png)

In scenario 1 zou dit zijn (voorbeeld):

![Alt text]({{ site.baseurl }}/assets/zondergw.png)

**Conclusie**  
Beide scenario’s zijn in principe haalbaar. Zo is er in scenario 1 weliswaar een enorme hoeveelheid koppelingen/relaties, maar is dat voor computersystemen en bij het gebruik van standaarden ook niet onoverkomelijk (zie de werking van het internet en services daarop). Scenario 2 kan sterk vereenvoudigend werken en in potentie aanzienlijke kostenbesparend werken. De term ‘in principe’ is gebruikt omdat de haalbaarheid van beide scenario’s sterk afhangt van de ICT-volwassenheid van de entiteiten, maar ook van wat er op centraal niveau voor het betreffende domein en sector mogelijk is en of er überhaupt een centrale of regie organisatie is etc. Soms zal een domein en sector scenario 1 prima in kunnen vullen, in andere gevallen kan dat nauwelijks het geval zijn. Andersom geldt dit ook. Soms zal een domein en sector eenvoudig een Gedeelde Domein Voorziening (GDV) kunnen financieren, realiseren en leveren. In andere gevallen kan het vanwege allerlei aspecten volstrekt onmogelijk zijn zo’n voorziening op te tuigen in gezamenlijkheid. Bijvoorbeeld door de inrichting van governance, inrichting van de financiering, autonomie aspecten, gebrek aan draagvlak voor gedeelde voorzieningen enz. Kortom per domein en sector zal moeten worden nagegaan wat de beste aanpak is en daarop worden ingezet.

**Ondersteuning**  
Wanneer een domein en sector tot de conclusie komt dat een Gedeelde Domein Voorziening (GDV) wenselijk of noodzakelijk is, dan kan vanuit het stelsel ondersteuning worden geboden bij de realisatie. Zo zijn er mogelijkheden om mee te denken bij het ontwerp, kunnen er referentie-ontwerpen worden gemaakt, kunnen eerdere ontwerpen vanuit andere domeinen/sectoren (indien aanwezig) worden gedeeld, etc. Mocht er concrete interesse zijn, dan kunnen vanuit het stelsel en via de stelselbeheer initiatieven op dit vlak worden geïnitieerd. Neem daarvoor in dat geval contact op met de stelselbeheer met verwijzing naar de hier beschreven informatie.




