from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import logging
import mimetypes
import pathlib
import json
import socket
import urllib.parse


BASE_DIR = pathlib.Path()
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5000


def send_data_to_socket(msg):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(msg, (SERVER_IP, SERVER_PORT))
    client_socket.close()


class HttpHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        msg = self.rfile.read(int(self.headers['Content-Length']))
        send_data_to_socket(msg)
        #self.send_html_file('index.html')
        self.send_response(302)
        self.send_header('Location', 'index.html')
        self.end_headers

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('message.html')
        else:
            if pathlib.Path().joinpath(pr_url.path[1:]).exists():
                self.send_static()
            else:
                self.send_html_file('error.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def save_data(data):
    msg = urllib.parse.unquote_plus(data.decode())
    filename = BASE_DIR.joinpath('storage/data.json')
    try:
        payload = {key: value for key, value in [el.split('=') for el in msg.split('&')]}
        with open(filename, "r") as fd:
            unpacked = json.load(fd)
        unpacked[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = payload
        with open(filename, 'w', encoding='utf-8') as fd:
            json.dump(unpacked, fd, indent='\t', ensure_ascii=False)
    except ValueError as err:
        logging.error(f'Field parse data {msg} with error {err}')
    except OSError as err:
        logging.error(f'Field write data {msg} with error {err}')


def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(1024)
            save_data(data)
    except:
        logging.info('Socket server stopped')
    finally:
        server_socket.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(threadName)s %(message)s")
    thread_server = Thread(target=run)
    thread_server.start()

    thread_socket = Thread(target=run_socket_server(SERVER_IP, SERVER_PORT))
    thread_socket.start()
