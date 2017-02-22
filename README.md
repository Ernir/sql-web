# SQLweb

**(Ísl)** Kennsluvefur í notkun gagnasafna. Hluti af meistaraverkefni Eiríks Ernis Þorsteinssonar við IVT-deild Háskóla Íslands. Uppsetningarleiðbeiningar má finna að neðan.

**(En)** A teaching website for introductory database usage. Written as a part of Eiríkur Ernir Þorsteinsson's master's project, Faculty of Industrial Engineering, Mechanical Engineering, and Computer Science at the University of Iceland. Installation instructions are currently in Icelandic only, but can be found below.

## Uppsetning þróunarútgáfu

Vefurinn er skrifaður í [Django](https://www.djangoproject.com/) og ætti að keyranlegur á flestum nútíma stýrikerfum. Þessar uppsetningarleiðbeiningar gera ráð fyrir [Ubuntu](https://www.ubuntu.com/) Linux 16.04 eða sambærilegu kerfi. Gert er ráð fyrir að lesandinn sé kunnugur skipanalínunotkun.

### 0. Undanfarar

Áður en hafist er handa er nauðsynlegt að eftirfarandi sé uppsett:

  *  [python 3](https://www.python.org/downloads/) með þróunartólum, sýndarumhverfakerfi og pakkakerfi (nauðsynlegt)
  *  þýðingartól sem tengjast C-viðbótum
  *  gagnagrunnskerfi, hér gert ráð fyrir [SQLite](https://sqlite.org/)
  
að auki er sterklega mælt með:
  *  [git](https://git-scm.com/) til að sækja og viðhalda forritskóða
  *  cURL og tar til að sækja myndir

Á Ubuntu má setja þetta allt saman upp með eftirfarandi skipunum:

```
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install git python3-dev python3-pip python3-venv sqlite3 build-essential curl
```

### 1. Forritskóði sóttur

Til að ná í nýjustu útgáfu af forritskóða vefsins má nota git. Færum okkur í yfirmöppu þeirrar möppu sem vefurinn skal dvelja í og sækjum þvínæst forritskóðann með:

```
$ git clone https://github.com/Ernir/sql-web.git
```

en skipunin mun búa til möppu að nafni `sql-web`. Færum okkur til hennar og höldum okkur þar þangað til uppsetningu er lokið.

```
$ cd sql-web/
```

*Annar valmöguleiki*: Hægt er að sækja forritskóðann án þess að nota git með því að fara inn á [github-síðu verkefnisins](https://github.com/Ernir/sql-web) og sækja hana sem .zip skrá.

### 2. Uppsetning og virkjun sýndarumhverfis

Ráðlagt er að keyra Python-forrit önnur en hin fánýtustu í sýndarumhverfi (e. *virtual environment*) sem heldur utan um forritssöfn. Stofnum til nýs sýndarumhverfis að nafni `sqlvenv`.
```
$ python3 -m venv sqlvenv
```
Áður en umhverfið má nota þarf að virkja það. Að óbreyttu mun nafn sýndarumhverfisins birtast fremst á skipanalínunni meðan það er virkt.
```
$ source sqlvenv/bin/activate
(sqlvenv) $ 
```

*Athugasemd*: Ekki er þörf á því núna, en til að slökkva á sýndarumhverfinu má gefa skipunina `deactivate`.
```
(sqlvenv) $ deactivate 
$
```

### 3. Uppsetning pakka sem vefurinn krefst

Í möppunni `sql-web` má finna skrá sem heitir `requirements.txt`, sem inniheldur upplýsingar um forritssöfn sem vefnum eru nauðsynleg. Setjum söfnin upp með `pip` pakkastjórnunarkerfinu, sem sett var upp í skrefi 0.

Í þessu skrefi er mikilvægt að sýndarumhverfið sé virkt!

```
(sqlvenv) $ pip install -r requirements.txt
```

Líklegt er að þessi skipun gefi leiðbeiningar um að uppfæra `pip` með skipuninni `pip install --upgrade pip`. Óhætt er að gera það.

### 4. Uppsetning gagnagrunns

Sjálfgefin gögn eru til fyrir kennsluvefinn, sem innihalda mögulega upphafsuppsetningu á greinum og sýnidæmi um verkefni. Þau má finna í SQLite-gagnagrunnsskránni `sqlweb.db` sem sækja má með

```
(sqlvenv) curl -O https://notendur.hi.is/~ernir/sql-web/sqlweb.db
```

Sjálfgefnu gögnin innihalda vísanir í myndir. Myndirnar eiga heima í skrá sem heitir `mediafiles` og er undirmappa `sql-web` möppunnar. Eftirfarandi skipun (sem krefst cURL og tar) sækir myndirnar og setur þær í viðeigandi möppu:

```
(sqlvenv) $ curl https://notendur.hi.is/~ernir/sql-web/mediafiles.tar.gz | tar -xz
```

Eigi ekki að nota sjálfgefnu gögnin má upphafsstilla tóman gagnagrunn fyrir vefinn með skipuninni

```
(sqlvenv) $ python manage.py migrate
```

*Annar valmöguleiki*: Hægt er að komast hjá því að nota cURL og/eða tar, þó ferlið sé þá . Þá þarf að vista [.db skrána](https://notendur.hi.is/~ernir/sql-web/sqlweb.db) í grunnmöppunni. Til að fá myndirnar þyrfti að búa til `mediafiles` möppuna handvirkt og sækja þær sem [.zip skrá](https://notendur.hi.is/~ernir/sql-web/mediafiles.zip). Þetta gæti verið viðeigandi fyrir Microsoft Windows notendur.

### 5. Uppsetning ofurnotandareiknings (valkvæmt)

Setja þarf upp ofurnotanda fyrir vefinn ef gera á efnisbreytingar. Það má gera með skipuninni

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
Af öryggisástæðum þarf þó að gera breytingar á umhverfisbreytum (e. *environment variables*). Breyturnar hafa sjálfgefin gildi sem ekki eru viðeigandi við raunverulega keyrslu.

Umhverfisbreyturnar eru `DEBUG_MODE`, `SECRET_KEY` og `ALLOWED_HOSTS`. Í keyrsluútgáfu ætti `DEBUG_MODE` að vera `0` og `SECRET_KEY` að vera mjög langur strengur sem erfitt er að giska á. Einnig er líklegt að uppsetningin noti annan þjón en hinn sjálfgefna `127.0.0.1`, svo gefa þarf breytunni `ALLOWED_HOSTS` viðeigandi gildi.

Á staðaluppsettu Ubuntu er að afgreiða breyturnar með því að setja línur á borð við eftirfarandi í `.bashrc` skrána og endurhlaða svo breytunum (t.d. með því að endurræsa skelina).
```
export SECRET_KEY="miklulengristrengurenþetta"
export DEBUG_MODE="0"
```

Auk þess þarf að setja upp afkastameiri og öruggari vefþjón en þróunarvefþjóninn sem er innbyggður í Django. Þekkt er að [Gunicorn](http://gunicorn.org/) með [NGINX](https://www.nginx.com/) hentar vel.
