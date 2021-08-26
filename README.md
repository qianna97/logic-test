## Installation (docker-compose)

build the image

```bash
docker-compose build
```

run migrate

```bash
docker-compose run migrate
```
run server

```bash
docker-compose run web
```

## Usage
- Swagger path at index url webserver, example localhost:5000/

![Alt text](img/1.png?raw=true "Swagger index")

![Alt text](img/2.png?raw=true "Swagger Auth Header")

## API endpoint
- /register : POST -> creating user data

using body argument username, email, password, name

- /login : POST -> get token access

using body argument username, password

- /edit : POST -> edit user data

using body argument username, email, password, name and header with Authorization field containing token access from login endpoint

- /refcode : POST -> input other user ref code

using body argument refcode and header with Authorization field containing token access from login endpoint

- /find-user : POST -> find user by name

using body argument name

- /get-hero : POST -> get LoL hero by name using outside API and redis cache

using body argument name