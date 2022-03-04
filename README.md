# GameLauncher

## Probieren Sie mal aus!

Um dieses Projekt auszuprobieren, müssen Sie Python 3 auf Ihrem Rechner
installiert haben. Python 3 können Sie auf folgenden Link herunterladen
und installieren:

https://www.python.org/downloads/

Wenn Sie den GNU/Linux Betriebssystem nutzen, können Sie Python 3 mit
Paketmanager Ihre Linux-Distribution installlieren.

Wenn Sie Python 3 auf Ihren System haben, führen Sie folgende Befehlen,
um den Server zu starten:

Die erste Schritt unterscheidet sich im Windows und Linux.

* Linux/MacOS

```bash
source .venv/bin/activate
```

* Windows

```bash
.venv/bin/activate
```

Falls Sie PowerShell im Windows nutzen, müssen Sie den folgenden Befehl
ausführen:

```bash
.venv/bin/activate.ps1
```

Wenn Sie sich im virtualen Umgebung finden, müssen Sie benötigte Modulen,
die in requirements.txt Datei definiert sind, installieren. Das zu machen
können Sie einfach den folgenden Befehl ausführen:

```bash
python3 -m pip install -r requirements.txt
```

Zum Schluss starten Sie den Server:

```bash
python3 manage.py runserver
```

Viel Glück beim Ausprobieren!
