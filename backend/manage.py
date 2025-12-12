import os
import sys


def main():
    # Se o usuário digitar apenas:
    # poetry run python manage.py runserver
    # então adicionamos a porta automaticamente
    if "runserver" in sys.argv and len(sys.argv) == 2:
        sys.argv.append("127.0.0.1:9000")

    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()


