# -*- coding: utf-8 -*-
# Author: Nianze A. TAO
"""
call pdfeditorma_core.main and others
"""
import sys
from argparse import ArgumentParser
from pdfeditorma_core import main, reset, remove


if __name__ == "__main__":
    DEBUG = False
    parser = ArgumentParser(description="pdfeditorMA-GUI")
    parser.add_argument(
        "--reset",
        action="store_true",
        help="remove all settings and caches; "
        "default settings will be created at next launch",
    )
    parser.add_argument(
        "--remove", action="store_true", help="remove the whole application"
    )
    parser.add_argument("--debug", action="store_true", help="enable debug mode")
    args = parser.parse_args()
    if args.reset and args.remove:
        print("reset or remove?")
        sys.exit(0)
    if args.reset:
        reset()
        sys.exit(0)
    if args.remove:
        remove()
        sys.exit(0)
    if args.debug:
        DEBUG = True
    main(debug=DEBUG)
