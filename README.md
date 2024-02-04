## Bank

This is a simple bank application that allows a user to create an account, deposit money, withdraw money, and view 
their balance.

The architecture of the application is mix of layered architecture and Clean Architecture. The application is 
divided into layers:

- domain - contains the business logic
- application - contains the use cases
- infrastructure - contains database implementation, migrations and web framework implementation.
- presentation - contains the API endpoints

The app is covered with tests using pytest, and the coverage is 100% (with some exceptions, such as migrations, 
configurations).

### Technologies used:
- FastAPI (and Pydantic, SQLAlchemy, and Alembic, Asyncpg)
- PostgreSQL
- Docker
- Docker-compose


### Available endpoints:

- `GET /accounts/` - get all accounts
- `POST /accounts/` - create an account
- `PATCH /accounts/{account_id}/` - update an account
- `DELETE /accounts/{account_id}/` - delete an account
- `GET /accounts/{account_id}/balance/` - get the balance
- `GET /accounts/{account_id}/transactions/` - get account transactions
- `POST /accounts/{account_id}/deposit/` - deposit money to account
- `POST /accounts/{account_id}/withdraw/` - withdraw money from account
- `POST /accounts/{account_id}/transfer/` - transfer money to another account

- `GET /transactions/` - get all transactions (history of all transactions)

### How to run the application (docker-compose)

To run the application, you need to have docker and docker-compose installed on your machine. If you don't have it installed, 
you can download it from [here](https://www.docker.com/products/docker-desktop).

After you have docker and docker-compose installed, you can clone the repository with:


```bash
  git clone https://github.com/iza-w/fastapi-bank.git
```

Then you can run the application with:

```bash
  docker compose up -d 
  make migrate-docker  # run migrations
```

And that's it! The application is running on [http://localhost:8000](http://localhost:8000).


To **stop** the application, you can run:

```bash
  docker compose down
```


### How to see the application in action

Open your browser and go to [http://localhost:8000/docs](http://localhost:8000/docs). You will see the FastAPI 
Swagger UI where you can test the application. 

You can also use the redoc UI by going to [http://localhost:8000/redoc](http://localhost:8000/redoc).
