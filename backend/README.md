# Backend

## Installation

```
$ virtualenv env
$ source env/bin/activate
(env) $ pip install -r requirements.txt
(env) $ python migrate.py
```

## Test data

If you want to test your setup with data from bastogne.be website just follow those easy steps ;-)

```
(env) $ $ python scrape.py 
[$] parsing http://bastogne.be/plan-de-bastogne/plan-de-bastogne 
[$] 16 categories
[$] 187 pois
(env) $ $ python populate.py 
[+] Populating data to the database ...
[+] Cleaning up previous dataset ...
[+] Done !
```

## Run

```
(env) $ python app.py 
[+] Starting server on 0.0.0.0:8000
[I 150321 00:18:05 web:1825] 200 GET /poi/ (172.16.115.130) 22.57ms
```
