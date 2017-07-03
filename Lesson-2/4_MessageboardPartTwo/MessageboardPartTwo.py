#!/usr/bin/env python3
#
# Step two in building the messageboard server:
# A server that handles both GET and POST requests.
#
# Instructions:
#
# 1. Add a string variable that contains the form from Messageboard.html.
# 2. Add a do_GET method that returns the form.
#
# You don't need to change the do_POST method in this exercise!
#
# To test your code, run this server and access it at http://localhost:8000/
# in your browser.  You should see the form.  Then put a message into the
# form and submit it.  You should then see the message echoed back to you.

from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

form = '''<!DOCTYPE html>
              <html><head><title>Message Board</title></head>
              <body><form method="POST" action="http://localhost:8000/">
                <textarea name="message"></textarea>
                <br>
                <button type="submit">Post it!</button>
              </form></body></html>
            '''


class MessageHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # 1. How long was the message? (Use the Content-Length header.)
        print(self.headers)
        length = int(self.headers.get('Content-Length', 0))
        # 2. Read the correct amount of data from the request.
        data = self.rfile.read(length).decode()
        # 3. Extract the "message" field from the request data.
        message = parse_qs(data)["message"][0]
        # Send the "message" field back as the response.
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        # Add a Blank Line
        self.end_headers()
        # Write to the output stream
        self.wfile.write(message.encode())

    def do_GET(self):
        # First, send a 200 OK response.
        self.send_response(200)

        # Then send headers.
        self.send_header('Content-type', 'text/html; charset=utf-8')

        # Add a blank line
        self.end_headers()

        # Now, write the response body.

        # encode() translates the string() into a bytes object
        # which is suitable for sending over the network
        # path contains the request path
        self.wfile.write(form.encode())

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MessageHandler)
    # Start the server
    httpd.serve_forever()
