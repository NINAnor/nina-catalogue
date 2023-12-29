# Catalogue Architecture
NINA catalogue uses Django and PostgreSQL.

The software is made of different parts:
- Django, is the application server, it handles all the logic of answering to browser requests
- Queue, provides long running tasks, scheduled tasks and asyncronous executions
- PostgreSQL, is the database server, it stores the data
- NGINX, is the webserver, it shares user-uploaded files and static assets
- Varnish, provides a caching layer

Features inside the catalogue are organized as modules, each module aims to be as much independent as possible:
- [Datasets](./datasets/index.md)
- [Maps](./maps.md)
