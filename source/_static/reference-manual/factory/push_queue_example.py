#!/usr/bin/env python3
from base64 import b64decode
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import logging
import os
import sys

from cryptography.x509 import load_pem_x509_certificate
import jwt
import requests

try:
    AUDIENCE = os.environ["JWT_AUDIENCE"]
except KeyError:
    sys.exit("Please run with JWT_AUDIENCE set to something like: https://<val>.ngrok.io")

keys = {}


def load_keys():
    r = requests.get("https://www.googleapis.com/oauth2/v1/certs")
    for k, v in r.json().items():
        cert = load_pem_x509_certificate(v.encode())
        keys[k] = cert.public_key()


def assert_auth(auth_header: str):
    parts = auth_header.split()
    if len(parts) != 2:
        raise ValueError("Expecting Bearer <token>")
    if parts[0].lower() != "bearer":
        raise ValueError("Invalid auth method: " + parts[0])

    headers = jwt.get_unverified_header(parts[1])
    key = keys.get(headers["kid"])
    if not key:
        raise ValueError("Invalid kid: " + headers["kid"])
    jwt.decode(parts[1], key, audience=AUDIENCE, algorithms=[headers["alg"]])


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers["Content-Length"])

        try:
            assert_auth(self.headers.get("Authorization"))
        except Exception as e:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(str(e).encode())

        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        event_type = data["message"]["attributes"]["event-type"]
        event_data = b64decode(data["message"]["data"].encode()).decode()
        event = json.loads(event_data)
        logging.info("%s - %s", event_type, event)

        self.send_response(204)
        self.end_headers()


def run(server_class=HTTPServer, handler_class=WebhookHandler, port=8080):
    logging.info("Loading pubsub JWT keys")
    load_keys()

    httpd = server_class(("", port), handler_class)
    logging.info("Starting httpd on port %d", port)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()


if __name__ == "__main__":
    from sys import argv

    logging.basicConfig(level="INFO")

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
