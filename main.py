import logging as lg
import traceback

from py_files import logging_setup as ls


def main():
    pass


if __name__ == '__main__':
    ls.logging_setup_main()
    try:
        main()
    except:
        lg.error(traceback.format_exc())
