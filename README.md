# Django project to fetch video data from youtube

### Project setup

Uses the default Django development server.

1. Rename `app/.env.example` to `app/.env`
2. Update the environment(`google api keys`) variables in the `app/.env` file.
3. Build the images and run the containers:

    ```
    docker-compose up -d --build
    ```

    Test it out at [http://localhost:8000](http://localhost:8000).
4. `/videos` API for getting paginated videos, can use different filters there
5. `/videos?search=title` for searching using title and description.
6. For creating a superuser, so that you can access the dashboard. Use below command
    ```
    docker-compose exec web python manage.py createsuperuser
    ```

*`secret keys` used in `.env.sample` file should not use in production's environment.

> Add multiple Google API keys in .env file with suffix _1, _2, etc. for multiple keys support

> This is development setup, so no nginx used in docker as well debugging is on

### Tech stack used
- Docker
- Django/Python
- DRF
- Celery
- RabbitMQ
- PostgreSQL
