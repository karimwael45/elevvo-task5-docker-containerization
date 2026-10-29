# Task 5: Containerized Flask and PostgreSQL Application

This project runs a small Flask web application and PostgreSQL database on a
private Docker bridge network named `internal`. The app exposes only port 5000;
PostgreSQL has no host port mapping. Docker bridge networks are private to the
Docker host by default, and only the app's explicit port mapping is published.

## Requirements

- Docker Desktop with Docker Compose
- PowerShell, Bash, or an equivalent shell

## Configuration

Copy the safe template and choose a local password:

```bash
cp .env.example .env
```

The `.env` file is ignored by Git and is never copied into the Docker image.

## Build and run

```bash
docker compose build
docker compose up -d
docker compose ps
```

The app is available at <http://localhost:5000>. PostgreSQL is reachable by
the app at the Docker DNS name `db:5432`, but its port is not published to the
host.

## Test

```bash
curl http://localhost:5000/
curl http://localhost:5000/db-time
docker compose exec app whoami
docker compose port db 5432
```

Expected results include a successful JSON response from `/db-time`, `app` from
`whoami`, and no output from `docker compose port db 5432`.

To confirm the private network and published ports:

```bash
docker network inspect internal
docker compose ps
```

The app should show `0.0.0.0:5000->5000/tcp`; the database should show no
published host port.

## Stop

```bash
docker compose down
```

Add `-v` only when you intentionally want to delete the PostgreSQL data volume.
