# AWS Cost Guardian

Monitor de costos d'AWS amb alertes, basat en FastAPI, PostgreSQL i Docker Compose.

## Arquitectura

- **FastAPI** per a l'API backend.
- **PostgreSQL** per a dades persistents i registres.
- **Docker Compose** per a entorn local reproduïble.
- **Vanilla HTML/JS** per a dashboard lleuger (planificat).
- **Boto3** per a consulta de cost AWS a Cost Explorer.

## Estructura de carpetes

- `app/`
  - `api/v1/` : rutes i versionat de l'API
  - `core/` : configuració i constants de l'aplicació
  - `db/` : definició de base de dades i base models
  - `models/` : ORM models de SQLAlchemy
  - `services/` : integracions amb AWS i lògica d'informes
- `tests/` : proves unitàries i d'integració
- `Dockerfile` : imatge de producció per a l'API
- `docker-compose.yml` : entorn local de desenvolupament
- `.env` : variables sensibles locals (no es commiten)

## Començar

1. Copia `.env.example` a `.env`.
2. Ajusta `DATABASE_URL` i `AWS_*` si cal.
3. Executa `docker compose up --build`.
4. Navega a `http://localhost:8000`.

## Notes

- Aquesta arquitectura està pensada per ser escalable i apta per GitHub des del primer dia.
- Els secrets no es commiten; s'usen variables d'entorn i `.env` local.
