from waitress import serve
from dataexcelwebsite.wsgi import application  # Ganti 'myproject' dengan nama folder project kamu

if __name__ == '__main__':
    serve(application, host='172.16.150.98', port=5050)