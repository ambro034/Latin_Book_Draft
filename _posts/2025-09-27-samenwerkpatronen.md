---
title: Samenwerkpatronen
author: lg
date: 2025-09-27 09:00:00
category: Jekyll
layout: post
---

> ##### Definitief
{: .block-tip }

De samenwerkingsfuncties zoals genoemd in onderdeel Werking zijn navolgend uitgewerkt.

Opdracht patroon
-------------

Het gaat hier om het patroon van het aan elkaar geven van opdrachten of verzoeken om een opdracht uit te voeren (of dienst te verlenen).

_Opmerking: Dit patroon wordt toegepast in estafettemodel, maar ook in het netwerkmodel. Binnen het netwerkmodel worden ook andere patronen toegepast, binnen het estafettemodel niet tot nauwelijks._

Bij het opdracht patroon geeft de ene ketenpartner de andere ketenpartner een opdracht of verzoekt om een opdracht uit te voeren. De ketenpartner wacht op een antwoord, bijvoorbeeld dat de opdracht is uitgevoerd of krijgt bijvoorbeeld het resultaat van de opdracht. Hier kan sprake zijn van diensten en dienstverlening. De modaliteiten hiervan (eisen aan de geleverde dienst, vorm van het antwoord, reactietermijn, ..) zullen vooraf zijn afgesproken en bijvoorbeeld zijn vastgelegd in een SLA (of soortgelijke afspraken). 

Kenmerkend voor dit patroon is de vaak asynchrone verwerking van het verzoek; met andere woorden: na het verzoek gaat er enige tijd overheen voordat de terugkoppeling volgt.

_Voorbeeld: De opdracht kan zijn: “lever mij informatie over …”. Bij een informatiedienst moet deze informatie bijvoorbeeld eerst worden opgezocht en of verzameld. Wanneer de informatie direct kan worden opgevraagd is er sprake van een synchrone verwerking en is het patroon Inzage van toepassing. Met dit patroon kan ook een asynchroon verzoek tot het wijzigen van informatie worden georganiseerd._

Kenmerk: asynchroon.

Om deze patronen te implementeren moeten taak/procesapplicaties van ketenpartners worden uitgerust met applicatiefuncties voor iedere Samenwerkfunctie:

- **Opdracht Aanvragen** \[Samenwerkfunctie\]: De applicatiefunctie "Aanvragen \[Samenwerkfunctie\]" ondersteunt de dienstaanvrager bij de afhandeling van een dienstaanvraag bij een ketenpartner. Dit omvat zowel het plaatsen van een dienstaanvraag bij een ketenpartner, als het in ontvangst nemen van het aangevraagde (informatie)product.  
- **Opdracht Leveren** \[Samenwerkfunctie\]: De applicatiefunctie "Levering \[Samenwerkfunctie\]" ondersteunt de dienstleverancier bij de afhandeling van dienstaanvragen van de \[Dienst\]. Dit omvat zowel het in ontvangst nemen van een dienstaanvraag van een ketenpartner, als het leveren van het aangevraagde (informatie)product en de afhandeling van de statusovergangen van de Samenwerkfunctie.  

Inzage patroon
-------------

Dit patroon wordt gebruikt om informatie in te zien (bij de bron). Op een inzageverzoek volgt direct (synchroon) het antwoord.

Kenmerken: synchroon, niet toestand veranderend.

De te implementeren applicatiefuncties:

- **Inzage Verzoek** \[Samenwerkfunctie\]: De ketenapplicatiefunctie "Inzage Verzoek \[Samenwerkfunctie\]" is de functie met behulp waarvan de daartoe geautoriseerde functionarissen van de eigen organisatie informatie via Samenwerkfunctie kan opvragen bij ketenpartners.
- **Inzage Leveren** \[Samenwerkfunctie\]: De ketenapplicatiefunctie "Inzage Leveren \[Samenwerkfunctie\]" is de informatie verstrekkende functie via de Samenwerkfunctie van de Ketenpartner die door de leverende Ketenpartner wordt ingericht.

Gebeurtenis patroon
-------------

Dit patroon betreft het melden van en zich informeren over gebeurtenissen die in de processen bij een specifieke ketenpartner hebben plaatsgevonden. Gebeurtenissen bevatten slechts enkele identificerende gegevens over de gebeurtenis. Het is aan de afnemer om zich regelmatig te informeren over nieuwe gebeurtenissen en te bepalen wat hij hiermee doet. Geeft de gebeurtenis aanleiding tot een informatiebehoefte, dan kan deze verkregen worden via het patroon Inzage.

In de IV is de term 'event driven' bekend geworden, gebeurtenis gedrevenheid. Het idee achter gebeurtenis gedrevenheid is dat gegevens worden vastgelegd als een gebeurtenis en dat een proces wordt getriggerd door deze toestandsveranderingen. Een gebeurtenis beschrijft die toestandsverandering die gelogd (of geregistreerd) wordt. Dat betreffen doorgaans ruwe data of observaties. In deze zienswijze is een event een gestandaardiseerde manier waarop gegevens worden opgeslagen. Dat heet ook wel toestand gedrevenheid. Het is juist een relevante toestand die een proces activeert. Wanneer één afzonderlijke gebeurtenis die toestand beschrijft dan zijn toestand en gebeurtenis “in sync”. Vaak is het zo dat eerdere gebeurtenissen tezamen een relevante toestand beschrijven. Een verzameling aan gebeurtenissen leiden tot een bepaalde toestand waarop geacteerd moet worden. Zo leidt één specifieke gebeurtenis niet tot handelen (bijvoorbeeld 1 VT melding), maar een verzameling wel (bijvoorbeeld verschillende zorgmeldingen). De toestand die voldoende grondslag of reden biedt om over te gaan tot handelen is de toestand (en niet de afzonderlijke gebeurtenis). Dit impliceert overigens dat gebeurtenissen gepersisteerd moeten worden, als deze op deze manier ingezet worden.

Een gebeurtenis is een specifieke, waarneembare actie of voorval dat plaatsvindt op een bepaald moment en dat invloed kan hebben op de toestand van een systeem, proces of entiteit. Een gebeurtenis kent de volgende eigenschappen:
- Tijdgebonden: Een gebeurtenis vindt plaats op een specifiek tijdstip of binnen een bepaalde tijdsperiode.
- Waarneembaar: Gebeurtenissen kunnen geregistreerd worden. Ze is derhalve meetbaar of observeerbaar.
- Contextafhankelijk: Een gebeurtenis, net als alle gegevens, heeft in een bepaalde context betekenis.
- Afzonderlijk en onderscheidbaar: Gebeurtenissen staan los van andere gebeurtenissen en kunnen duidelijk worden geïdentificeerd.
- Niet doelgericht: Een gebeurtenis kent geen intentie. Een gebeurtenis beschrijft, zoveel mogelijk, de feitelijkheden.
- Toestandbeschrijvend: Een gebeurtenis beschrijft een event.
- Onwijzigbaar en niet verwijderbaar: Gebeurtenissen beschrijven feiten. Ze zijn daarom onwijzigbaar of verwijderbaar. Tenslotte is iets daadwerkelijk voorgevallen.
- Asynchroon: Events worden asynchroon gecommuniceerd. De afzender wacht niet op reactie.

De volgende applicatiefuncties zijn relevant:

- **Gebeurtenis Melden** \[Samenwerkfunctie\]: Voor iedere dienst die een ketenpartner levert, voorziet deze ketenpartner in een applicatiefunctie "Gebeurtenis melden \[Dienst\]". Deze applicatiefunctie meldt aan de centrale voorziening de voortgang van de afhandeling van een Dienstaanvraag.
- **Gebeurtenis Ontvangen** \[Samenwerkfunctie\]: Ketenpartners dienen geregeld te verifiëren of er interessante gebeurtenissen zijn. De ketenpartners kunnen deze gebeurtenissen gebruiken om gegevensverwerkende processen te activeren; bijvoorbeeld om de eigen informatiepositie bij te werken en hier vervolgens adequaat op te reageren.
