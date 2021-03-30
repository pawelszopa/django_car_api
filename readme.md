# Django Car_Api 
Django Rest Framework application allows to keep cars in database and rating them

## Prerequisites
You have to have installed docker and docker-compose on your computer.

## Starting
1. Rename .env-default file to .env.
2. Type command `docker-compose up --build` in terminal in project root directory.
3. Open browser with url `http://0.0.0.0:8000/cars` or `http://127.0.0.1:8000/cars` on Windows.
4. Enjoy!

### Swagger:
`https://immense-refuge-23099.herokuapp.com/swagger/`
if localhost:
`http://localhost:8000/swagger/`

### Endpoints:
1. `/cars`  POST & GET - allows to get list of cars and send a new car to database
2. `/rate` POST - allows to rate a car
3. `/cars/{id}` GET & DELETE - allows to get information about a car by id and delete car by id
4. `/popular` GET  - allows to list cars based on rates amount.


### Tests
1.Model tests - type command `docker-compose exec web python manage.py test api/tests` in terminal in project root directory.
1.API tests - type command `docker-compose exec web python manage.py test cars/tests` in terminal in project root directory.


## Licence
```text
* ----------------------------------------------------------------------------
 * "THE BEER-WARE LICENSE" (Revision 42):
 * <phk@FreeBSD.ORG> wrote this file.  As long as you retain this notice you
 * can do whatever you want with this stuff. If we meet some day, and you think
 * this stuff is worth it, you can buy me a beer in return.  Poul-Henning Kamp
 * ----------------------------------------------------------------------------
```