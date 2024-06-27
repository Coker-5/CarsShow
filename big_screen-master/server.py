import logging
from waitress import serve
from app import app


if __name__ == '__main__':
    logging.basicConfig(filename="logs/los.log", level=logging.INFO)
    logging.basicConfig(filename="logs/errors.log", level=logging.ERROR)

    serve(app, host='0.0.0.0', port=5000, threads=5)
