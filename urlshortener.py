import http.server
import json
import random
import string
from urllib.parse import urlparse
import time
from collections import defaultdict

url_storage = {}
# Набор для защиты от перебора
used_shortened_urls = set()

request_count = defaultdict(list)  # Хранит список временных меток запросов для каждого IP

# Максимальное количество запросов за указанный период
MAX_REQUESTS_PER_MINUTE = 5


def is_request_allowed(ip_address):
    current_time = time.time()
    request_count[ip_address] = [timestamp for timestamp in request_count[ip_address] if current_time - timestamp < 60]

    if len(request_count[ip_address]) >= MAX_REQUESTS_PER_MINUTE:
        return False

    request_count[ip_address].append(current_time)
    return True


def generate_short_url():
    while True:
        short_url = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if short_url not in used_shortened_urls:
            used_shortened_urls.add(short_url)
            return short_url


# Валидация ссылки
def is_valid_url(url):
    parsed = urlparse(url)
    return all([parsed.scheme, parsed.netloc])


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        ip_address = self.client_address[0]
        if not is_request_allowed(ip_address):
            self.send_response(429)  # Too Many Requests
            self.end_headers()
            self.wfile.write(b'{"error": "Too many requests"}')
            return

        if self.path == '/shorten':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            original_url = data.get("original_url")

            if not is_valid_url(original_url):
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b'{"error": "Invalid URL"}')
                return

            for short_url, original in url_storage.items():
                if original == original_url:
                    short_url_full = f'http://127.0.0.1:8000/{short_url}'
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(json.dumps({"short_url": short_url_full}).encode())
                    return

            short_url = generate_short_url()
            url_storage[short_url] = original_url

            short_url_full = f'http://127.0.0.1:8000/{short_url}'

            self.send_response(201)
            self.end_headers()
            self.wfile.write(json.dumps({"short_url": short_url_full}).encode())

    def do_GET(self):
        short_url = self.path[1:]  # Убираем начальный '/'
        original_url = url_storage.get(short_url)

        if original_url:
            self.send_response(302)  # Redirection
            self.send_header('Location', original_url)
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error": "URL not found"}')


def run(server_class=http.server.HTTPServer, handler_class=Handler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Сервер работает на адресе 127.0.0.1:{port}')
    httpd.serve_forever()


if __name__ == "__main__":
    run()
