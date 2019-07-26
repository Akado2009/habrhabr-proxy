from http.server import BaseHTTPRequestHandler,HTTPServer
import urllib.request
from bs4 import BeautifulSoup

IP_ADDRESS = "127.0.0.1"
PORT_NUMBER = 8080
BASE_URL = "https://habr.com"

def check_path(path):
    fake_gets = ['/fonts', '/images', '/site', '/favicon']
    for fake in fake_gets: 
        if path.startswith(fake): return False
    return True

def add_trademark(word):
    punctuation = ['.', ',', '?', '!', ':', ';']
    tm_char = '™'
    if word.endswith(tuple(punctuation)):
        if len(word) == 7: 
            return word[:-1] + tm_char + word[-1]
        return word
    if len(word) == 6:
        return word + tm_char
    return word


class CustomHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if check_path(self.path): 
            habr_html = urllib.request.urlopen(BASE_URL + self.path)
            habr_content = habr_html.read()
            soup = BeautifulSoup(habr_content, "html.parser")
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            for a in soup.findAll('a', href=True):
                if BASE_URL in a['href']:
                    a['href'] = a['href'].replace(BASE_URL, 'http://{}:{}'.format(IP_ADDRESS, PORT_NUMBER))
            for element in soup.body.findAll(text=True):
                text = element.string.strip()
                if text:
                    words = text.split()
                    words = list(map(add_trademark, words))
                    element.replace_with(' '.join(words) + ' ')
            self.wfile.write(str(soup).encode())
        
        return

try:
    server = HTTPServer((IP_ADDRESS, PORT_NUMBER), CustomHandler)
    server.serve_forever()

except KeyboardInterrupt:
    server.socket.close()

    # check pep8
    # check urls for redirect
    