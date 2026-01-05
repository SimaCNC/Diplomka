CONTROLLER -odkaz na funkce v MODELU - metody nebo funkce spravovane v controlleru

M - funkce spravovane v controlleru od modelu

C - command pro piezopohony (funkce ma vysokou spojitost s piezopohony)

O - "origo" -originalni hodnota ktera byla funkcni nebo puvodni a ted je zmenena z urciteho duvodu

cisla u popisku v controlleru odpovidaji cca strane kde se spojitost vyskytuje





#upravy

**KOD**

- je potreba zacit kreslit diagram dedeni apod.
-hledat mista k osetreni (Start kalibrace - verifikace podminek, )
- Detailne testovat aplikaci pro bugy, zrejme pri startu kalibrace sekvence rizeni piezopohonu problemy s vlakny race conditions, seriova linka
-popsat co jaka strategie dela: self.strategie = ["-", "Dopředná", "Zpětná","Opakovatelnost", "Hystereze", "Hystereze_2" ]
- nejaky excel pro vyhodnoceni s datasheetem - pythonu okno vyhodnoceni vypoctu + ale kopirovaci okna,
> statisticke vyhodnoceni - vyhodnoceni v pythonu a propsat do excelu - podivat se na vlastnosti senzoru a propsat.
- opravit pripojeni k aplikaci kdyz se treba odpoji piezopohony
-opravit chovani grafu pri preruseni sberu dat
-classa pro delani grafu

**PCB**
-citlivejsi obvod oscilatoru
-vymyslet snimace a pouziti
- u A/D snimani pridat zapojeni s operacnimi zesilovaci pro 3,3V, 5V, 10V vstupy - prepinani prepinacem,
LED pro indikaci jaky je zvolen OP zesilovac pro upravu signalu ze snimace -> PCB +12V napajeni a rozdeleni na 10V, 5V, 3,3V,
OP zesilovac v zapojeni..
-nejaka relatka pripojena k GPIO napriklad pro ovladani veci v budoucnu
-sirenka 5V
-ledky 5V
-debug konektory

-JAK JSEM PCB VYTVORIL -schema navrh ,deska - kiCAD,frezovani - flatCAM,zarovnani protoze nerovna deska cuprextitova - Autoleveller, pouziti frezky s - LinuxCNC,... material, proces vyroby blokove schema pochodu pouzitych SW
# udelat statickou charakteristiku A/D prevodniku pro OP zapojeni - asi neni treba - mozna pro zapojeni s OP amps
- krabicka s prvky
- LM pro rozdeleni napeti
- STOP tlačítko, softwarove reseni skrz MCU - preruseni INT, specialni vlakno v aplikaci pro cteni 

- TZN. VSTUPY : 1x oscilator, 3x A/D (10,5,3,3V), 1x protokol (Uart)
- pripojeni pro teploteni senzor


**3D MODEL**
-udelat vykresy soucastek
-do prilohy v diplomce udelat vykresy - rozjezdy max a min, misto pro ulozeni kalibracniho snimace

-JAK JSEM MODEL VYTVORIL - Inventor, LinuxCNC... material,freza,

**MCU**



**SENZOR**
-kapacitni  -- oscilator
-tenzometr  -- mustek
-IR snimac  -- delic
            -- .............amplitudove spektrum


**WORD diplomka**
-UPRVIT SCHEMATA
-upravit text? odstranit mista s dopredu znamym kapacitnim snimacem


**STATISTIKA**
-ze streamu hodnot nalezt MIN/MAX - propsat do vyhodnoceni
-z vyhodnoceni nalezt MIN/MAX - propsat do vyhodnoceni

**EXCEL**


**TODO**
-kicad navrh pcb
-python
-git
