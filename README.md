# Sample Blog — Django

Sample project built as a companion to the article series **Djangonaut Diaries**.

> **Week 1: Creating and Debugging a Django Project**
> https://dev.to/rodbv/djangonaut-diaries-week-1-creating-and-debugging-a-django-project-3bf6-temp-slug-8033734

## What's in here

A minimal Django blog application with three models:

- **Blog** — a named blog with a slug and description
- **Post** — articles belonging to a blog
- **Comment** — user comments on posts

All models share a common `TimestampedModel` base with a UUID primary key and `created_at` / `modified_at` timestamps.

## Running locally

This project uses [uv](https://docs.astral.sh/uv/) for dependency management.

```bash
uv sync                        # creates .venv and installs all dependencies
uv run python manage.py migrate
uv run python manage.py createsuperuser
uv run python manage.py runserver
```

Then open http://127.0.0.1:8000/admin.

To add a new dependency:

```bash
uv add <package>               # adds to pyproject.toml and updates uv.lock
uv add --dev <package>         # dev-only dependency
```

## Code quality

This project uses [ruff](https://docs.astral.sh/ruff/) for linting and formatting, enforced via [pre-commit](https://pre-commit.com/).

Install the hooks after cloning:

```bash
pre-commit install
```

Hooks run automatically on `git commit`. To run manually:

```bash
pre-commit run --all-files
```

Rules enabled: pycodestyle, pyflakes, isort, pyupgrade, bugbear. Most issues are autofixed on commit.

## License

MIT License

Copyright (c) 2026 Rodrigo

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
