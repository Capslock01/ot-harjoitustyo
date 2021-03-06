# Käyttöohjeet

## Asennus



Varmista ensin, että koneelta löytyy poetry komennolla
```
poetry --version
```
Mikäli poetryä ei löydy, voit asentaa sen [täältä](https://python-poetry.org/docs/#installation).

Lataa viimeisin release [GitHubista](https://github.com/Capslock01/ot-harjoitustyo/releases). Unzippaa ohjelma haluamaasi tiedostoon, ja aja siellä komento
```
poetry install
```

Nyt sovelluksen voi käyttistää komennolla
```
poetry run invoke start
```

## Käyttö
___

### Projektin luominen
___

Ensimmäistä kertaa käynnistyessään ohjelma luo tyhjän tietokannan. Uuden projektin voi luoda oikeasta reunasta kohdasta "Luo uusi projekti". Projektin nimi kirjoitetaan tekstikenttään, ja sen tulisi muodostua yhdestä lyhyestä sanasta (ei välttämätöntä). Projekti lisätään "Lisää projekti" napista, jolloin oikealle puolelle tulee näkyviin kyseisen projektin hallintapalkki. Luotujen projektien hallintapalkit haetaan tietokannasta, kun sovelluksen avaa seuraavan kerran.

### Projektien ajastaminen
___

Hallintapalkin nappi "Play" käynnistää ajastimen. "Pause" pysäyttää ajastimen väliaikaisesti. "Stop" -nappi nollaa ajastimen, ja tallentaa ajastimessa näkyvän ajan tietokantaan.

### Statistiikkojen hakeminen
___

Ikkunan oikeassa reunassa on kohta "Statistiikat". Sovellus hakee käynnistyessään oletuksena meneillään olevan kuukauden tiedot. Painamalla "Hae tiedot" ilman, että tekstikenttään on kirjoitettu mitään, voidaan hakea kaikki tallennetut tiedot. Tietyn kuukauden tiedot voidaan hakea kirjoittamalla vuosi ja kuukausi tekstikenttään ennen hakunapin painamista. Aika tulee kirjoittaa muodossa YYYY-MM, tai YYYY-MM-DD. Esimerkiksi vuoden 2022 toukokuun tilastot saa haulla `2022-05`, ja päivän 3.5.2022 haulla `2022-05-03`.

### Projektin poistaminen
___

Projektin poistaminen tapahtuu oikean reunan kohdasta "Poista projekti". Projektin nimi kirjoitetaan tekstikenttään, ja painetaan "Poista projekti". Projektin hallintapalkki katoaa, mutta kurssi jää edelleen tietokantaan deaktiivisena. Nyt projektille ei tule hallintapalkkia, mutta sen datat näkyy edelleen statistiikoissa. Projektin uudelleenaktivointi tapahtuu luomalla uusi saman niminen projekti. Mikäli haluat nollata koko tietokannan, voit käyttää komentoa:
```
poetry run invoke reset
```