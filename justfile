default: run

run:
    uv run manage.py runserver

migrate:
    uv run manage.py migrate

shell:
    uv run manage.py shell_plus --ipython

mmm *args:
    uv run manage.py makemigrations {{args}}
    uv run manage.py migrate

manage *args:
    uv run manage.py {{args}}

alias m := manage
