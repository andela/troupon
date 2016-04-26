#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "troupon.settings")

    from django.core.management import execute_from_command_line
    args = [argument.decode('UTF-8') for argument in sys.argv]
    execute_from_command_line(args)
