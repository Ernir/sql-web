# SQLweb*

**(Ísl)** Kennsluvefur í notkun gagnasafna. Hluti af meistaraverkefni Eiríks Ernis Þorsteinssonar við IVT-deild Háskóla Íslands. Uppsetningarleiðbeiningar má finna að neðan.

**(En)** A teaching website for introductory database usage. Written as a part of Eiríkur Ernir Þorsteinsson's master's project, Faculty of Industrial Engineering, Mechanical Engineering, and Computer Science at the University of Iceland. Installation instructions are currently in Icelandic only, but can be found below.

## Uppsetning þróunarútgáfu

Vefurinn er skrifaður í [Django](https://www.djangoproject.com/) og ætti að keyranlegur á flestum nútíma stýrikerfum. Þessar uppsetningarleiðbeiningar gera ráð fyrir [Ubuntu](https://www.ubuntu.com/) Linux 16.04 eða sambærilegu kerfi. Gert er ráð fyrir að lesandinn sé kunnugur skipanalínunotkun.

### 0. Nauðsynlegir undanfarar

Áður en hafist er handa er nauðsynlegt að eftirfarandi sé uppsett:

  *  [git](https://git-scm.com/)
  *  [python 3](https://www.python.org/downloads/) með þróunartólum, sýndarumhverfakerfi og pakkakerfi
  *  gagnagrunnskerfi, hér gert ráð fyrir [SQLite](https://sqlite.org/).
  *  þýðingartól sem tengjast C- og Postgresviðbótum

Á Ubuntu má setja þau upp með:

```
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install git python3-dev python3-pip python3-venv sqlite3 build-essential libpq-dev
```

### 1. Stilling á umhverfisbreytum

Keyrsla vefsins krefst þess að tvær umhverfisbreytur (e. *environment variables*) séu stilltar. Þær eru `DEBUG_MODE`, sem við þróun ætti að vera `1` og `SECRET_KEY` sem er ekki-tómur strengur.

Hægt er að afgreiða þær með því að setja línur á borð við eftirfarandi í `.bashrc` skrána og endurhlaða henni (t.d. með því að endurræsa skelina).
```
export SECRET_KEY="lykill"
export DEBUG_MODE="1"
```
Í raunverulegu keyrsluumhverfi ætti `SECRET_KEY` að vera langur strengur sem erfitt er að giska á og `DEBUG_MODE` að vera 0.

### 2. Forritskóði sóttur

Til að ná í nýjustu útgáfu af forritskóða vefsins má nota git. Yfirmappa möppunnar sem vefurinn skal dvelja í er valin og eftirfarandi skipun keyrð:

```
$ git clone https://github.com/Ernir/sql-web.git
```

en hún mun búa til möppu að nafni `sql-web`. Færum okkur til hennar og höldum okkur þar.

```
$ cd sql-web/
```

### 3. Uppsetning og virkjun sýndarumhverfis

Ráðlagt er að keyra Python-forrit önnur en hin fánýtustu í sýndarumhverfi (e. *virtual environment) sem heldur utan um forritssöfn. Stofnum til nýs sýndarumhverfis að nafni `sqlvenv`.
```
$ python3 -m venv sqlvenv
```
Áður en umhverfið má nota þarf að virkja það. Að óbreyttu mun nafn sýndarumhverfisins birtast fremst á skipanalínunni meðan það er virkt.
```
$ source sqlvenv/bin/activate
(sqlvenv) $ 
```

Ekki er þörf á því núna, en til að slökkva á sýndarumhverfinu má gefa skipunina `deactivate`.
```
(sqlvenv) $ deactivate 
$
```

### 4. Uppsetning pakka sem vefurinn krefst

Í möppunni `sql-web` má finna skrá sem heitir `requirements.txt`, sem inniheldur upplýsingar um forritssöfn sem vefnum eru nauðsynleg. Setjum söfnin upp með `pip` pakkastjórnunarkerfinu.

Í þessu skrefi er mikilvægt að sýndarumhverfið sé virkt!

```
(sqlvenv) $ pip install -r requirements.txt
```

### 5. Uppsetning gagna 

Með forritskóðanum fylgja sjálfgefin gögn - þ.e.a.s. innihald kennslubókarinnar sjálfrar ásamt sýnidæma um verkefni. Til að setja gögnin upp þarf að keyra tvær skipanir, sú fyrri til að setja upp gagnagrunn og þá seinni til að hlaða í hann gögnum.

```
(sqlvenv) $ python manage.py migrate
(sqlvenv) $ python manage.py loaddata content.json
```

að því loknu þarf að setja upp ofurnotanda fyrir vefinn. Það má gera með skipuninni

```
(sqlvenv) $ python manage.py createsuperuser
```

og fylgja leiðbeiningunum sem birtast á skjánum.

### 6. Keyrsla þróunarvefþjóns

Með Django fylgir vefþjónn sem er hentugur til keyrslu á þróunarvélum. Á honum má kveikja með skipuninni

```
(sqlvenv) $ python manage.py runserver
```

og heimsækja svo síðuna með því að fara á slóðina `http://127.0.0.1:8000/` í vafra.

Til að breyta eða bæta við námskeiðum, lesefni eða verkefnum má fara inn á slóðina `http://127.0.0.1:8000/admin` og skrá sig inn með ofurnotendaaðganginum sem búinn var til í skrefi 5.

## Uppsetning keyrsluútgáfu

Uppsetning keyrsluútgáfu (til opinberrar birtingar) er í flestum atriðum eins og uppsetning þróunarútgáfu.
Af öryggisástæðum þarf þó að gera breytingar á umhverfisbreytum, sjá skref 1 í uppsetningu þróunarútgáfu. 

Auk þess þarf að setja upp afkastameiri vefþjón en þróunarvefþjóninn sem er innbyggður í Django. Nútíma vefþjónar duga flestir, en mælt er með [NGINX](https://www.nginx.com/).
