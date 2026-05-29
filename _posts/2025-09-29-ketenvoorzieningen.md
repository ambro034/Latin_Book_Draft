---
title: Stelselvoorzieningen
author: lg
date: 2025-09-29
category: Jekyll
layout: post
---

> ##### Definitief
{: .block-tip }

Binnen de keten leveren de verschillende partijen diensten en is sprake van een federatief landschap. Idealiter zijn er geen centrale voorzieningen, of wel ketenvoorzieningen, nodig. In die zin volgen we eenzelfde uitgangspunt als het Federatief Datastelsel (FDS): “afspraken boven standaarden boven voorzieningen”. Echter zullen ketenvoorzieningen niet te voorkomen zijn. Zie ook CORV. Voor de werking van het stelsel zullen de volgende ketenvoorzieningen nodig zijn:
1. Event Provenance Store en Event Hub
2. Diensten Catalogus (optioneel)
3. API Catalogus (optioneel)
4. Transformatie dienst (optioneel, mogelijk onvermijdbaar)
5. Demo- en testomgeving 

Daar waar “optioneel” is aangegeven, is geen sprake van een noodzaak, maar van een potentieel nut. Dit type voorzieningen zal niet in het eerste plateau worden gerealiseerd, maar mogelijk in opvolgende plateau’s. 


Event Provenance Store en Event Hub
-------------

Om relevante gebeurtenissen te kunnen vinden en customer journey of tijdlijnen mogelijk te maken is een ketenindex nodig en de gestructureerde (graph based) opslag van events in een onveranderlijke chronologische volgorde. Dus een voorziening die dit levert voor binnen keten uitgewisselde gebeurtenissen of wel een Event Provenance Store. Er moeten in grote hoeveel heden gebeurtenisgegevens (events) kunnen worden ontvangen, gedistribueerd, opgeslagen in logs/topics, etc. Er is hiervoor een streamingplatform nodig, we noemen dat de Event Hub. Merk op dat de ketenpartners vaak ook zullen beschikken over streamingplatformen, we noemen deze Event Brokers. Het verschil tussen Event Hub en Event Broker is dat de Event Hub meer geschikt is voor het efficiënt verwerken van grote hoeveelheden event data en daarvoor geoptimaliseerd ids. Ook geeft de term Event Hub in deze context aan dat het een centrale voorziening betreft in een hub-spoke architectuur.


Diensten Catalogus (optioneel)
-------------

De Diensten Catalogus is een centrale voorziening in de keten, waarin de diensten die aangeboden worden door de keten- of samenwerkingspartners binnen de Jeugd-, Zorg- en Veiligheidsketen worden beschreven en gepubliceerd. De dienstencatalogus bevat gegevens over een dienst, de aanbiedende ketenpartner, de toegestane afnemende ketenpartners, de contactgegevens bij de aanbieder, de URL voor het aanvragen van de dienst, en de minimale vereiste gegevens voor het ‘bestellen’ van de dienst en een verwijzing naar de bij de dienst behorende SLA. Er moet, niet vrijblijvend, altijd een contract, convenant of andersoortige afspraak tussen afnemer en aanbieder aan het leveren van een dienst ten grondslag liggen. Deze en eventuele bijbehorende DPIA of andersoortige afspraken kunnen eventueel ook via de Dienstencatalogus ontsloten worden.


API Catalogus (optioneel)
-------------

Idealiter zijn API's goed vindbaar. De API-Catalogus voorziening vormt een centrale plek om keten-API’s te kunnen vinden. De API-Catalogus voorziening verwijst door naar de decentrale API-Catalogi / DevPortals. REST API is immers een decentraal patroon en afhankelijkheden van centrale voorzieningen zijn ongewenst. De API-Catalogus voorziening maakt het zoeken slechts eenvoudiger en levert een totaal overzicht van de keten API’s op één plek. Dat is handig, maar geen vereiste.


Transformatie dienst (optioneel, mogelijk onvermijdbaar)
-------------

De communicatie tussen verschillende domeinen die hun eigen protocollen, eigen datamodellering en eigen semantiek, voeren vraagt om een vertaalservice. Naast deze verschillen moet het verschil tussen verschillende versies en release kalenders van services en clients worden opgevangen. Een verschil tussen service (bron) en client (gebruiker) zal altijd opgelost moeten worden. In een zuivere API-gedachte zijn de clients en de services 'loosely coupled', wat het translatie en transformatie probleem bij de ontvanger van de gegevens legt. 

In het meest ideale geval worden services, overal hetzelfde toegepast én volgen ze allemaal dezelfde releasekalender voor nieuwe versies. Dat is echter een utopie en zal nooit voorkomen. Vandaar dat berichttransformatie en protocol translatie functies zijn die ook CORV2 zal moeten ondersteunen. Het vertalen van berichten is een standaard functie van het huidige CORV. Doorgaans is standaard vertaling niet mogelijk en in plaats daarvan moet vrijwel altijd maatwerk worden ingezet. 

Het centraal transformeren van gegevens verlangt veel kennis van de bron en de ontvangende partij. Vooral als deze vertalingen complexe “IF THEN ELSE” constructies bevatten. Ze zijn kostbaar om te onderhouden en relatief foutgevoelig. Omdat we verwachten dat het aantal services zal stijgen is het zaak om deze transformaties (als wel de translaties) tot een minimum te beperken. Een landschap dat via transformaties is gekoppeld is sterk monolithisch. Dergelijke transformaties centraal uitvoeren is ongewenst en dient dus alleen te worden gedaan als dit realistisch niet anders kan en dienen in principe altijd tijdelijk te zijn (ter overbrugging).

Bericht transformatie kan (en zal dat in de praktijk waarschijnlijk zijn) tijdelijk ook nodig zijn ter overbrugging van de transitie van CORV1 naar CORV2 als migratie dienst. Deze dienst is ook wel bekend onder de benaming Silvester diensten. 


Demo- en testomgeving
-------------
Er is een demo- en (acceptatatie)testomgeving beschikbaar om componenten, interfaces en de werking van het stelsel te demonsteren en te testen, ook de vernieuwingen daarvan. Deze omgeving bestaat uit de ketenvoorzieningen en de demo- en (acceptatatie)testomgeving variant daarvan, waarop kan worden aangesloten en de decentrale onderdelen bij de verschillende organisaties (welke zijn aangesloten al dan niet tijdelijk).   
