# GameLauncher Entwickler Dokumentation

## Hintergrund

Das GameLauncher Projekt ist mit dem Python 3 Programmiersprache und Django
Framework entwickelt. Das Projekt handelt sich, um die Spiele hinzufügen,
bearbeiten, und löschen zu können. Es ist ähnlich wie Steam und Epic Games,
aber hat keine Features wie Spiele zum öffnen oder sie kaufen.

In diesem Projekt sind einige Modulen genutzt, um einige Funktionalitäts
Entwicklung zu vereinfachen. Wie zum Beispiel PDF erstellung. Die Modulen,
die in diesem Projekt verwendet werden, sind im requirements.txt Datei
definiert. Die aktuelle Liste ist:

* setuptools -> Helfer zum Installieren anderer Python-Module aus dem Quellcode.
* django -> Framework zum Erstellen von Websites in Python.
* django-import-export -> Modul zum einfacheren Export von Datenbanken in vielen
Formaten wie Excel, JSON, CSV und vielen mehr...
* django-bootstrap-modal-forms -> Modul zum Erstellen von Popups in Django einfacher.
* pillow -> Python-Imaging-Bibliothek.
* requests -> Einfache, aber elegante HTTP-Bibliothek.
* PyPDF2 -> Eine reine Python-Bibliothek, die als PDF-Toolkit erstellt wurde.

## Wie ist es aufgebaut?

Jetzt stellt man sich die Frage: wie eigentlich ist es aufgebaut und wie könnte
es man weiterentwickeln? Bevor ich die Frage beantworte und ekläre wie es aufgebaut
ist, empfehle ich Ihnen Django, django-bootstrap-modal-forms und django-import-export
Dokumentationen anlesen:

Django -> https://docs.djangoproject.com/en/4.0/

django-bootstrap-modal-forms -> https://pypi.org/project/django-bootstrap-modal-forms/#description

django-import-export -> https://django-import-export.readthedocs.io/en/latest/

Damit Sie besser verstehen können, was hier geschrieben ist. Machen Sie keine
Sorge, wenn Sie die Dokumentationen lesen nicht können, ich verusche so eklären,
damit es für jeden klar ist.

### Grundlagende Struktur

GameLauncher Projekt hat die grundlagende Struktur des Djangos Projekt bzw. Es
gibt ein Projekt, das enthält ein oder mehreren Anwendung/en.

Was ist der Unterschied zwischen ein Projekt und eine Anwendung in Django?

Projekt ist einfach der Name Ihrer Website. Django erstellt ein Python-Paket und
gibt ihm einen Namen, den Sie angegeben haben. In unsere Fall wird es dann
game_launcher sein.

Anwendungen sind kleinen Komponenten, die zusammen Ihr Projekt ausmachen. Sie
sind die Merkmale Ihres Projekts. Wie unseren Fall:

* Spiel - Logik für Spieler
* Kategorien - Logik für Kategorien
* Anmelden - Login für Anmeldung und Registrierung

Jede Anwendung konzentriert sich auf einen einzelnen logischen Teil Ihres
Projekts.

Derzeitig im Projekt gibt es eine Anwendung, die myapp heißt. Es is ein
schlechtes Design, aber da ich am Anfang nicht über das Design fokusiert habe
und nur um das Projekt zu Ende zu bringen, habe ich so aufgebaut.

Es ist geplant das zu ändern, wenn alles andere fertig ist und es noch Zeit
gibt.

### myapp Anwendung Struktur

Die wichtigsten Dateien in myapp Anwendung/Verzeichnis sind:

* views.py -> Django-Ansichten sind Teil der Benutzeroberfläche — sie rendern
normalerweise das HTML/CSS/Javascript in Ihren Vorlagendateien in das, was Sie
in Ihrem Browser sehen, wenn Sie eine Webseite rendern.
* modules.py -> Datenbank Tabellen bzw. Datenbank.
* urls.py -> Pfaden den Projekts.
* resources.py -> Resource definiert, wie Objekte ihren Import- und
Exportdarstellungen zugeordnet werden und den Import und Export von Daten
handhaben.
* templates/* -> HTML Dateien, die UI definieren.
* static/* -> CSS/JS Dateien, die UI verschönert.

### Weiterentwicklung

Wenn Sie eine Seite für diesen Projekt erstellen wollen, müssen Sie ein Template
erstellen. Ein Template ist ein HTML-Datei, die kann Django-Template-Syntax nutzen
kann. Um Django-Template-Syntax zu verstehen, empfehle ich folgende Dokumentaion
anlesen:

https://docs.djangoproject.com/en/4.0/ref/templates/language/

Jede Template sollte ein oder mehrer urls haben, die zu dem Temmplate zeigt. Das
heißt, dass Sie müssen für Ihre erstelltes Template ein url definieren, mit dem
man Ihre Template erreichen kann. Das können Sie im urls.py Datei machen.

Ein url braucht ein Ansicht, damit das URL weißt, was er machen sollte. Sie können
Ansichten in views.py Datei definieren. Ein Ansicht ist meisten einfach eine Methode,
die macht ein HTTP GET oder POST request und rendert Ihre definierte Template. Ein
Ding zum beoabachten ist, dass das Ansicht sollte immer ein Anfrage als Paramaeter
haben und immer irgendwelche Template zurückgeben.

Wenn Sie das alles gemacht haben, sollte alles funktionieren.

## Datenbankänderungen

Falls Sie brauchen Datenbank zu ändern, müssen Sie folgende Befehle ausführen,
damit Ihre Änderungen wahrgenommen würden:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```
