# NAVIS

## Opis projekta ##


Aplikacija pruža osnovne funkcionalnosti [CIMIS](https://cimis.pomorstvo.hr/ords/f?p=100:1:11980871426075:GOST_APLIKACIJE::::) sustava koji koristi Ministarstvo mora, prometa i infrastrukture za vođenje evidencije o plovilima
koja se nalaze u Hrvatskom registru brodova i koji plove sjevernim djelom Jadrana. 

[Video demonstracija aplikacije](https://youtu.be/QDbW3rUIouY)

### Osnovne funkcionalnosti uključuju: ###
- upisivanje novih plovila i svih podataka o njima u registar
- brisanje zapisa i editiranje postojećih podataka
- prijava odlaska i dolaska broda u luku u nacionalnoj plovidbi 
- pregled svih putovanja i statusa za svaki brod

### Dodatne funkcionalnosti ###
- prikaz statistika o putovanjima
- pretraživanje podataka o brodovima (slično kao e-plovilo)
- zaključivanje putovanja po završetku ili otkazivanju
- notifikacija adminu u slučaju prekrcaja broda

---
### Struktura aplikacije ###
Aplikacija je podjeljenja na:
- API za korisnika
- API za Admina

   API za korisnika uključuje funkcije koje omogućavaju pregled podataka o brodovima, putovanjima, prijavu i zaključivanje putovanja te statistiku
   
   API za Admina uključuje upis/editiranje/brisanje plovila u/iz registra i pregled upozorenja o prekrcaju/opasnom teretu
---
## Pokretanje aplikacije lokalno ##

1. Preuzimanje i raspakiravanje svih podataka sa git repozitorija u direktorij
2. Navigacija u terminalu u navedeni direktorij
3. Izrada docker image-a upisivanjem naredbe 

   ```bash 
   docker build --tag navis:1.0 .
4. Pokretanje kontejnera na temelju stvorene slike na portu 5000 

    ```bash
    docker run  -p 5000:8080 -d navis:1.0

5. Otvaranje preglednika na adresi 

    ```bash
    localhost:5000



