# Luukannel

Julkaisuvalmis, täysin staattinen HTML-sivusto Janne K. Jääskeläisen fantasiaromaanille **Luukannel**. Etusivu ja kaikki 37 lukua ovat omilla osoitteillaan. Lukija voi käyttää sisällysluetteloa, siirtyä luvusta toiseen ja vaihtaa vaalean ja tumman teeman välillä. Viimeksi avattu luku tallentuu vain lukijan selaimeen.

## Sisältö ja lähteet

- index.html: kirjan etusivu ja sisällysluettelo
- chapters/: 37 valmista HTML-lukusivua
- assets/: tyylit, paikallinen JavaScript, kansikuva ja kuvake
- source/chapters/: [alkuperäisen kirjasivuston](https://books.yellowmineralindustries.com/4/luukannel) 37 erillistä Markdown-lukuvientiä
- source/book.md: saman kirjan koko Markdown-vienti
- build.py: luo HTML-sivut uudelleen lähteistä

Sisältö ja kansikuva ladattu 5.11.2026 julkisesta Writebook-julkaisusta. Alkuperäisen sisällysluettelon 37 lukua ovat mukana samassa järjestyksessä. Lukujen tekstiä ei ole toimitettu tai lyhennetty. Kirjan tekijänoikeudet kuuluvat Janne K. Jääskeläiselle; alkuperäinen sivu ei ilmoita avointa lisenssiä.

## Esikatsele

Avaa index.html suoraan selaimessa tai käynnistä paikallinen palvelin komennolla python3 -m http.server 8000. Avaa sitten http://localhost:8000/.

## Julkaise GitHub Pagesissa

Repo on tarkoitettu nimelle pub-luukannel. index.html on repon juuressa. Valitse GitHubissa **Settings → Pages → Deploy from a branch → main → /(root)** ja tallenna. CNAME määrittää verkkotunnukseksi luukannel.net; DNS pitää osoittaa [GitHub Pagesin ohjeen](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) mukaisesti. .nojekyll varmistaa, että valmiit HTML-tiedostot julkaistaan sellaisinaan.

## Luo HTML-sivut uudelleen

Asenna riippuvuus komennolla python3 -m pip install -r requirements.txt ja aja python3 build.py. Skripti tarkistaa, että lähteissä on täsmälleen 37 lukua. Julkaisu ei tarvitse Pythonia eikä ulkoisia JavaScript-kirjastoja.
