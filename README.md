# GameLauncher

to start the server do the following:

```bash
$ source .venv/bin/activate # on Windows only .venv/bin/activate
$ python3 manage.py runserver
$ # If there are any errors, that some modules are missing run the
$ # following:
$ python3 -m pip install -r requirements.txt # and then python3 manage.py runserver
```
## Database updates (models.py)

If there are any changes made to the database, the follwing must be run
to update it:

```bash
$ python3 manage.py makemigrations myapp
$ python3 manage.py sqlmigrate myapp [number (0001)]
$ python3 manage.py migrate
```
