# Horizon Restaurants

## Setup

To run, ensure you have docker installed with the `docker compose` command available. 
Then run `bin/prod.bat` on windows or `make prod` on linux. 
The database will be automatically generated.
The user `admin` will be generated with password `admin` which has the maximum 
amount of permissions.

To run the native GUI. Run `py gui/main.py` 
To access the webapp go to `localhost:5000`

Access to PgAdmin is provided under `localhost:5050` for convienience but would
be disabled in an actual production enviroment.
Email: `admin@admin.com`
Password: `root`
DB Host: `db`
DB Username: `postgres`
DB Password: `postgres`
