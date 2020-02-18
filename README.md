# Setup the dev environment

Note, prompts beginning with `=#` indicate they should be done in psql

1. Clone the repository: `git clone git@github.com:heldridge/photos-webapp.git`
1. Install npm dependencies: `npm ci`
1. Generate css: `gulp`
1. Install postgres: `sudo apt install postgresql postgresql-contrib`
1. Create your user: `sudo -u postgres createuser --interactive`
1. Create your database: `sudo -u postgres createdb <username>`
1. Create the photos database: `=# CREATE DATABASE photos;`
1. Create the django user: `=# CREATE USER django;`
1. Add the django user pw: `=# alter user django with encrypted password '<password>';`
1. Give the django user permissions to access the database: `=# grant all privileges on database photos to django;`
1. Create a virtualenv: `python -m virtualenv venv`
1. Install the requirements: `pip install -r requirements.txt -r requirements-dev.txt`
1. Copy the `env_setup.sh` script outside of the git directory
1. Fill in the proper values for the untracked `env_setup.sh`
1. `. ./env_setup.sh`
1. Download elasticsearch `7.4.2`: https://www.elastic.co/downloads/elasticsearch
1. Run three elasticsearch nodes with:
    - `./elasticsearch`
    - `./elasticsearch -Epath.data=data2 -Epath.logs=log2`
    - `./elasticsearch -Epath.data=data3 -Epath.logs=log3`
1. Run memcached with `memcached`
1. cd into the `django` folder
1. `python manage.py migrate`
1. `python manage.py search_index --rebuild`
1. `python manage.py runserver`

# Completely reset the database

1. `=# DROP DATABASE photos;`
1. `=# CREATE DATABASE photos;`
1. `=# grant all privileges on database photos to django;`
1. `python manage.py migrate`
1. `python manage.py search_index --rebuild`

# Add photos to the database

1. `cd scripts`
1. `python json_to_postgres.py`
1. `python manage.py search_index --rebuild`
1. `python manage.py sqlsequencereset pictures | python manage.py dbshell`

# Other dependencies

-   memcached
