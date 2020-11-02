import logging

from traceback_with_variables import printing_tb, LoggerAsFile


logging.basicConfig(format='%(asctime)-15s %(name)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


def f(n):
    print(1 / n)


def main():
    with printing_tb(file_=LoggerAsFile(logger)):
        x = 1
        f(x - 1)


main()
