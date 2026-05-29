---
title: Aansluiten
author: lg
date: 2025-10-02
category: Jekyll
layout: post
---

> ##### Definitief
{: .block-tip }

Aansluitvoorwaarden
-------------
Om aan te sluiten op het Jeugd, Zorg en Veiligheid Afsprakenstelsel en de voordelen daarvan te kunnen benutten is het nodig:  
1. Te voldoen aan het geheel van afspraken en standaarden dat veilige en betrouwbare uitwisseling van gegevens borgt binnen het domein.
2. De relevante eigen koppelvlakken en systemen in te richten volgens deze afspraken en standaarden.​
3. De samenwerkfuncties en samenwerkpatronen te implementeren.

Aansluitstappen
-------------
Een aansluitende organisatie kan de volgende stappen volgen:  
1. Kennisnemen van doel, achtergronden, principes, randvoorwaarden en techniek (zie leeswijzer).
2. De afspraken na te gaan en een impact bepaling uitvoeren op organisatie, processen en techniek.
3. Stappen nemen om aan het geheel van afspraken en standaarden te kunnen voldoen.
4. Eventuele procesmatige aanpassingen voorbereiden of maken.
5. Relevante eigen koppelvlakken en systemen aanpassen, zodat deze voldoen aan de afspraken.
6. De koppelvlakken en systemen zodanig aan te passen dat deze het realiseren van samenwerkfuncties en samenwerkpatronen in basis ondersteunen (het mogelijk maken deze te realiseren).
7. Een aantal essentiële samenwerkfuncties en samenwerkpatronen implementeren.
8. De overige samenwerkfuncties en samenwerkpatronen geleidelijk verder implementeren.

Impact-bepaling
-------------
Binnen voorgenoemde stappen is een essentiële stap het uitvoeren van een impact bepaling. Die kan voor elke organisatie anders zijn. Hieronder is een vragenlijst opgenomen die kan helpen bij de impact bepaling en tevens een concreter beeld geeft van wat hiervoor eenvoudigweg genoemd is het implementeren van proces, koppelvlak en systeem aanpassingen.

De impact bepaling kan gedaan worden in drie delen. Waarbij in het eerste deel alleen gekeken wordt naar de theoretische en strategische aspecten, in het tweede deel langs de lijnen van samenwerkpatronen en in het derde deel langs de lijnen van samenwerkfuncties.

Als hieronder over kosten wordt gesproken moet gedacht worden aan zowel eenmalige kosten als terugkomende kosten zoals die gerelateerd aan beheer (beheerkosten).

### Deel I
Voer een analyse uit t.a.v. doelen, principes, afspraken en het stelsel in de breedte. Ga na wat de impact zou zijn van de beweging naar het Afsprakenstelsel voor de organisatie en de processen. Kijk minimaal naar de volgende aspecten met hun mogelijke impact:  
1. De beweging van estafette model naar netwerkmodel en het ontstaan van een ketenindex (tijdlijnen), welke beide impact kunnen hebben op processen, weliswaar positief, maar vragen ook aandacht voor datakwaliteit, schrijfwijze, etc.
2. Het bewegen naar en toepassen van gebeurtenis gedrevenheid en event driven architectures. Past deze ontwikkeling bij beweging die organisatie wil maken en hoever is de organisatie daar al in.
3. Het bewegen naar en toepassen van halen bij de bron en REST-API architectures. Past deze ontwikkeling bij beweging die organisatie wil maken en hoever is de organisatie daar al in.
4. De geleidelijke uitfasering van ebMS.
5. Het uitgangspunt van één bounded context en daarmee één semantisch model en begrippenkader binnen het Jeugd, Zorg en Veiligheidsdomein, voor ten minste de onderlinge koppelvlakken.
6. De potentiële vertaling van semantisch model en begrippenkader naar de binnenwereld van de organisatie welke mogelijk een ander semantisch model en begrippenkader hanteert of geen van beide.
7. Het ontstaan van mogelijkheden waarbij een organisatie soms zelf geen directe baten ervaart, maar het collectief wel, wat kan leiden tot financieringsvragen en vraagstukken over rol en taak.    

### Deel II
In dit deel wordt de impact van het implementeren van de samenwerkpatronen Gebeurtenis Ontvangen/ Gebeurtenis Melden, Inzake Verzoek/ Inzake Leveren, en Opdracht Aanvragen / Opdracht Leveren geanalyseerd inclusief generieke daarvoor benodigde onderdelen. Met implementatie bedoelen we hier de inrichting en of aanpassing van koppelvlakken en systemen om deze patronen te kunnen toepassen. De analyse van hoe deze worden toegepast volgt in het derde deel.

Gebeurtenis Ontvangen / Gebeurtenis Melden  
Voor de impactbepaling wordt onderstaande schets gebruikt en vanuit twee perspectieven, die van gebeurtenissen ontvangen en gebeurtenissen melden.

![Alt text]({{ site.baseurl }}/assets/events.png)

Gebeurtenis Ontvangen:  
Om gebeurtenissen te ontvangen zijn er geen voorzieningen bij de ontvangende organisatie nodig als API-Management, Event Platform, etc. Daarom zijn deze wit en grijs weergegeven. Dat wil niet zeggen dat deze niet ingezet kunnen worden. Zo is het denkbaar de events te ontvangen via een event platform, maar vereist is dat niet.

Om de impact als ontvanger van gebeurtenissen te bepalen kunnen de volgende vragen worden gesteld:  
- Kan mijn systeem aangepast worden om events te ontvangen? Kan mijn systeem de ontvangen events verwerken en beschikbaar maken voor de gebruikers van het systeem? Moet het daarvoor aangepast worden, hoeveel tijd vergt dat en welke kosten zijn ermee gemoeid?
- Als mijn systeem niet aangepast kan worden, kunnen er services worden toegepast (ontwikkeld worden) die deze functionaliteit kunnen invullen in samenhang met het systeem. Wat zijn daar de kosten van en hoeveel tijd en inspanning vergt dat?
- Als integratie met het systeem niet mogelijk is, kan een separate functionaliteit worden gerealiseerd. Wat zijn daar de kosten van en hoeveel tijd en inspanning vergt dat?
- Als het gewenst is een event platform in te zetten, is dat al aanwezig? Zo ja; wat zijn de configuratie kosten/inspanning? Zo nee; wat zijn de kosten en wat is inspanning om zo’n platform te realiseren?

Gebeurtenis Melden:  
Om gebeurtenissen te melden zijn geen voorzieningen bij de verzendende organisatie nodig zoals API Management. Denkbaar is dat de verzendende organisatie een event platform gebruikt, maar vereist is dat niet.

Om de impact als verzender van gebeurtenissen te bepalen kunnen de volgende vragen worden gesteld:  
- Is mijn (common ground gebaseerde) ICT-infrastructuur geschikt om events te verzenden? Moet deze daarvoor aangepast worden, hoeveel tijd vergt dat en welke kosten zijn ermee gemoeid?
- Kan mijn systeem aangepast worden om events te verzenden of de verzending daarvan te triggeren? Moet het daarvoor aangepast worden, hoeveel tijd vergt dat en welke kosten zijn ermee gemoeid?
- Als mijn systeem niet aangepast kan worden, kunnen er services worden toegepast (ontwikkeld worden) die deze functionaliteit kunnen invullen in samenhang met het systeem. Wat zijn daar de kosten van en hoeveel tijd en inspanning vergt dat?
- Als het gewenst is een event platform in te zetten, is dat al aanwezig? Zo ja; wat zijn de configuratie kosten/inspanning? Zo nee; wat zijn de kosten en wat is inspanning om zo’n platform te realiseren?

Inzage Verzoek / Inzage Leveren  
Voor de impactbepaling wordt onderstaande schets gebruikt en vanuit twee perspectieven, die van inzake verzoeken en van inzage leveren.

![Alt text]({{ site.baseurl }}/assets/inzage.png)

Inzage Verzoek  
Om inzage te doen zijn er geen voorzieningen bij de vragende organisatie nodig als API-Management, event platforme, etc. Daarom zijn deze wit en grijs weergegeven. Er zijn eveneens geen centrale voorzieningen nodig, zoals een Event provenance store en event hub. Ook een centrale API-catalog is niet noodzakelijk hoewel deze wel handig kan zijn om de API’s voor inzage te vinden waarbij de centrale catalog zal doorverwijzen naar de API-devportals/catalogs bij de aanbiedende organisatie.

Om de impact te bepalen om verzoeken om inzage te kunnen doen, kunnen de volgende vragen worden gesteld:  
- Kan mijn systeem aangepast worden om inzage verzoeken te doen en de response te ontvangen en verwerken? Moet het daarvoor aangepast worden, hoeveel tijd vergt dat en welke kosten zijn ermee gemoeid?
- Als mijn systeem niet aangepast kan worden, kunnen er services worden toegepast (ontwikkeld worden) die deze functionaliteit kunnen invullen in samenhang met het systeem. Wat zijn daar de kosten van en hoeveel tijd en inspanning vergt dat?
- Als integratie met het systeem niet mogelijk is, kan een separate functionaliteit worden gerealiseerd. Wat zijn daar de kosten van en hoeveel tijd en inspanning vergt dat?

Inzage Leveren:  
Om inzage te leveren dient een inzage (REST API) service te worden aangeboden. Doorgaans zal deze worden aangeboden via een API-Managementoplossing. Er moet toegang aangevraagd en verleend kunnen worden. De API-Managementoplossing en de bijbehorende Devportal kunnen daar een rol in spelen inclusief toegangsservices binnen de API Management oplossing of daaraan gekoppeld.

Om de impact te bepalen van het inzage leveren beschikbaar te stellen, kunnen de volgende vragen worden gesteld:  
- Beschik ik al over een API-Management oplossing? Zo ja; wat zijn de configuratie kosten/inspanning? Zo nee; wat zijn de kosten en wat is inspanning om zo’n voorziening te realiseren?
- Is mijn (common ground gebaseerde) ICT-infrastructuur geschikt om inzage te leveren? Moet deze daarvoor aangepast worden, hoeveel tijd vergt dat en welke kosten zijn ermee gemoeid?

Opdracht Aanvragen / Opdracht Leveren (REST API)  
Voor de impactbepaling wordt onderstaande schets gebruikt en vanuit twee perspectieven, die van opdrachten aanvragen en opdrachten leveren. Dit met behulp van REST-API’s (en dus niet via ebMS).

![Alt text]({{ site.baseurl }}/assets/opdrachtrestapi.png)

Opdracht Aanvragen:  
De benadering lijkt sterk op een Inzage Verzoek. Zie de vragen daar aangeven. In dit geval wordt er met de REST API call echter geen informatie opgevraagd, maar een opdracht ingestuurd (REST API POST).

Opdracht Leveren:  
Hoe de ontvangende partij de opdracht uitvoert kan zeer divers zijn en afhankelijk van de opdracht. Er kan een event worden gestuurd waarin wordt gemeld dat de opdracht is ontvangen, geweigerd, wat de status van uitvoering is of dat het event is uitgevoerd. In die gevallen kunnen min of meer dezelfde vragen gesteld worden als bij Gebeurtenis Melden. Wel zal extra aandacht besteed moeten worden aan de impact op systemen en processen om van opdracht tot melding te kunnen komen. Dit is een complexer patroon dan eerder behandelde patronen. Een opdracht kan ook zijn het klaarzetten van specifieke informatie voor Inzage, zie daarvoor de vragen bij Inzage Leveren waarbij opgemerkt dat hier sprake is van een complexer patroon dan Inzage Leveren op zichzelf.

Opdracht Aanvragen / Opdracht Leveren (ebMS)  
Opdracht Aanvragen en Opdracht Leveren via ebMS is een bestaande praktijk, zie navolgende figuur. De impactvraag is hier welke kosten gemoeid zijn bij het in de lucht houden van beide benaderingen tijdens de overgangsfase.

![Alt text]({{ site.baseurl }}/assets/opdrachtebms.png)

Generieke elementen  
Alle voorgaande aspecten maken gebruik van generieke bouwstenen rond toegang en logging. Bij deze bouwstenen zouden de volgende vragen gesteld kunnen worden.

OIN/Certificaat toegang (>plateau 1):  
Dit is de meest eenvoudige methode van toegangssverlening en de meeste organisaties zullen deze reeds toepassen.

- Beschikt mijn organisatie over processen om PKIoverheid certificaten te kunnen aanvragen en toepassen? Zo nee; welke inspanning en kosten zouden ermee gemoeid zijn deze processen in te richten.
- Kan ik toegang verlenen op basis van OIN/PKIoverheid certificaat?
- Zijn er afspraken gemaakt met de organisaties waarmee ik een koppeling wil of moet maken?

FSC (>plateau 1)  
- Kan ik de Federatieve Service Connectiviteit (FSC) standaard ondersteunen of doe ik wellicht dat al?
- Beschik ik over virtual servers of een container platform om FSC-componenten op te kunnen laten landen? Ondersteunt mijn leverancier FSC? Zo nee; welke inspanning en kosten zouden ermee gemoeid zijn FSC te gaan ondersteunen?

FTV (>plateau 1)  
- Ondersteunt mijn infrastructuur Federatieve Toegangsverlening, OIDC, OaAuth, AuthZen, ABAC, PBAC? Zo nee; welke inspanning en kosten zouden ermee gemoeid zijn FTV te gaan ondersteunen?

Logging  
- Beschikt mijn organisatie over logging en monitoring voorzieningen waarnaar alle verschillende services en componenten naar kunnen loggen? Zo nee; welke inspanning en kosten zouden ermee gemoeid zijn een logging voorziening te realiseren?

Common Ground  
- Ondersteunt mijn informatievoorziening het Common Ground gedachtengoed en is mijn data losgekoppeld van applicaties en werkprocessen? Zo nee; welke inspanning en kosten zouden ermee gemoeid zijn deze beweging te maken?
- Hoe voorkom ik dat ik door aanpassingen aan mijn systeem, om aan te sluiten op het afsprakenstelsel, geen monolithische maatwerkapplicatie krijg die afwijkt van het Common Ground gedachtengoed en op termijn tot hoge (transitie) kosten gaat leiden?   

### Deel III
Uitgaande dat we de samenwerkpatronen Gebeurtenis Ontvangen/ Gebeurtenis Melden, Inzake Verzoek/ Inzake Leveren, en Opdracht Aanvragen / Opdracht Leveren kunnen ondersteunen (technisch), en wellicht al enkele eerste samenwerkfuncties in productie hebben gebracht, is een vervolgvraag welke impact het heeft om de resterende functies te implementeren. Denkbaar is dat de eerste samenwerkfuncties meer moeite en inspanning vergen dan opvolgende, maar ook dat er aanzienlijke verschillen kunnen zitten in implementatieinspanning en kosten tussen de verschillende functies. Deze kunnen weer afhangen van het achterliggende systeem en de ICT-infrastructuur en dus ook per organisatie verschillen. Per samenwerkfunctie zal de vraag gesteld moeten worden wat de realisatie behelst, wat de inspanning is en welke kosten ermee gemoeid zijn. Dus ten aanzien van de samenwerkfuncties:
- Uitwisselen Melding
- Vaststellen Identiteit & Relaties
- Bepalen Bekendheid & Verrijking
- Werken aan Preventie
- Uitvoeren Triage & Taxatie
- Opstellen Analyse & Advies
- Inzien en Deelnemen door de Burger
- Overleggen over de Casus
- Uitwisselen Uitkomst Overleg
- Opstellen & Regisseren Plan
- Uitvoeren Actie
- Nazorg en Afsluiten Casus
- Inzien beschikbare diensten
- Inrichten en Bijsturen Samenwerking
- Monitoren samenwerking

Dit zal vooraf en zonder ervaringscijfers moeilijk zijn in te schatten. Het advies is daarom om hier een eerste schatting te maken en die bij te stellen op basis van ervaringscijfers zodra die beschikbaar komen.
