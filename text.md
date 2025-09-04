CONTROLLER -odkaz na funkce v MODELU - metody nebo funkce spravovane v controlleru

M - funkce spravovane v controlleru od modelu

C - command pro piezopohony (funkce ma vysokou spojitost s piezopohony)



cisla u popisku v controlleru odpovidaji cca strane kde se spojitost vyskytuje





#upravy

**KOD**
-je potreba projit veskere promenne s hodnotou None.. pravdepodobne nedodelana/zapomenuta cast 
-pridat ukladani souboru (nazev),  apod. do kalibrace okno
- je potreba zacit kreslit diagram dedeni apod.
-hledat mista k osetreni (Start kalibrace - verifikace podminek, )
- Detailne testovat aplikaci pro bugy, zrejme pri startu kalibrace sekvence rizeni piezopohonu problemy s vlakny race conditions, seriova linka
-popsat co jaka strategie dela: self.strategie = ["-", "Dopředná", "Zpětná","Opakovatelnost", "Hystereze", "Hystereze_2" ]
- nejaky excel pro vyhodnoceni s datasheetem - pythonu okno vyhodnoceni vypoctu + ale kopirovaci okna,
excel start - vytvoreni excelu s zadanymi prvky v python skriptu
> statisticke vyhodnoceni - vyhodnoceni v pythonu a propsat do excelu - podivat se na vlastnosti senzoru a propsat.


**PCB**
-citlivejsi obvod oscilatoru
-vymyslet snimace a pouziti
- u A/D snimani pridat zapojeni s operacnimi zesilovaci pro 3,3V, 5V, 10V vstupy - prepinani prepinacem,
LED pro indikaci jaky je zvolen OP zesilovac pro upravu signalu ze snimace -> PCB +12V napajeni a rozdeleni na 10V, 5V, 3,3V,
OP zesilovac v zapojeni..

-JAK JSEM PCB VYTVORIL -schema navrh ,deska - kiCAD,frezovani - flatCAM,zarovnani protoze nerovna deska cuprextitova - Autoleveller, pouziti frezky s - LinuxCNC,... material, proces vyroby blokove schema pochodu pouzitych SW
# udelat statickou charakteristiku A/D prevodniku pro OP zapojeni
- krabicka s prvky
- LM pro rozdeleni napeti
- STOP tlačítko, softwarove reseni skrz MCU - preruseni INT, specialni vlakno v aplikaci pro cteni 

- TZN. VSTUPY : 1x oscilator, 3x A/D (10,5,3,3V), 1x protokol (Uart)
- pripojeni pro teploteni senzor


**3D MODEL**
-pridat znacky pohybu os
-udelat vykresy soucastek
- rotacni osa?
-do prilohy v diplomce udelat vykresy - rozjezdy max a min, misto pro ulozeni kalibracniho snimace

-JAK JSEM MODEL VYTVORIL - Inventor, LinuxCNC... material,freza,

**MCU**
-dodelat stream hodnot pro zachyceni informaci pro umisteni senzoru - pouze pro debugging skrz nejaky monitor,
napr. pro nalezeni polohy, v aplikaci napriklad udelat tlacitko start stream pro poslani prikazu a nasledny stream hodnot z mcu, pro nalezeni vhoodne polohy umisteni pieza (-tl. max pozice v Y piezo) 
- stream pulzy, stream AD --- pro stream a zisk dat udelany kruhovy buffer datova struktura..?


**SENZOR**
-kapacitni  -- oscilator
-tenzometr  -- mustek
-IR snimac  -- delic
            -- amplitudove spektrum


**WORD diplomka**
-UPRVIT SCHEMATA


**STATISTIKA**
-ze streamu hodnot nalezt MIN/MAX - propsat do vyhodnoceni
-z vyhodnoceni nalezt MIN/MAX - propsat do vyhodnoceni

**EXCEL**
-pro vyhodnoceni je nutne drzet v nejakem datovem typu vsechny informace - struktura, napr. v classe excel pro vykresleni
-

**TODO**
-kicad navrh pcb
-excel kalibracni list
-python

