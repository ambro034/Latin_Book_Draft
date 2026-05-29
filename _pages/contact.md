---
title: Contact
author: lg
date: 2025-09-30
category: Jekyll
layout: post
---

Contactgegevens: volgen

Test1

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

<details><summary>▶ Click to show answer</summary>Correct Answer: A</details>  

Test1a

   ```python
   from google.colab import drive
   drive.mount('/content/drive')
   ```

<details><summary>▶ PlantUML</summary>
@startuml  
skinparam monochrome true  
skinparam defaultTextAlignment center  

actor "Client" as Client  
rectangle "Autorisatieserver" as AuthServer  
rectangle "Policy Administration Point\n(PAP)" as PAP  
rectangle "Policy Retrieval Point\n(PRP)" as PRP  
rectangle "Policy Decision Point\n(PDP)" as PDP  
rectangle "Policy Information Point\n(PIP)" as PIP  

rectangle "Policy Enforcement Point\n(PEP)" as PEP  
database "Data Toegangspunt\n(Resource-Server)" as DataAccess  

Client -up-> AuthServer : "Tokenaanvraag"  
AuthServer -down-> Client : "JWT Access-token"  

Client -right-> PEP : "Toegangsverzoek\n(REST/GraphQL + JWT)"  
PEP -left-> Client : "Gevraagde data"  

PEP -right-> DataAccess: "Geautoriseerde data-aanvraag"  
DataAccess -left-> PEP : "Gevraagde data"  

PEP -down-> PDP : "Toegangsverzoek"  
PDP -up-> PEP : "Toegangsbesluit"  

PDP -right-> PIP : "Contextinformatie opvragen" 
PIP -left-> PDP : "Contextinformatie retourneren"  

PDP -down-> PRP : "Beleidsregels ophalen"  
PRP -up-> PDP : "Beleidsregels retourneren"  

PAP -up-> PRP: "Beleidsregels beheren"  
@enduml
</details>  


