from http.server import BaseHTTPRequestHandler, HTTPServer
import json

import vectorize

host = "localhost"
post = 8080

class RecommendHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status):
        self.send_response(status)
        self.send_header("Content-type", 'application/json') # request and response only in json
        self.end_headers()

    def _json(self, data):
        self._set_headers(200)
        self.wfile.write(bytes(json.dumps(data), 'utf-8'))

    def _error(self, err_msg):
        self._set_headers(400)
        response = {
            "message" : err_msg
        }
        self.wfile.write(bytes(json.dumps(response), 'utf-8'))

    def do_GET(self):
        data = "server test"
        json = {'message': data}
        self._json(json)

    def do_POST(self):
        if self.headers['content-type'] != 'application/json':
            self._error("Content type error: use json to send data")

        content_length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(content_length), encoding="utf-8")
        if "userIngredients" in body:
            print(body)
            response = self.handleRequest(body["userIngredients"])
            self._json(response)
        else:
            self._error("'userIngredients' is missing")        

    def handleRequest(self, userIngredients):
        vec = vectorize.Vectorizer()
        vec.connect_database()

        vec.recipe_embedding()
        result = vec.recommend_recipes([userIngredients])

        vec.disconnect_database()
        return result


if __name__ == "__main__":        
    httpd = HTTPServer((host, post), RecommendHandler)
    print("Server started on http://%s:%s" % (host, post))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    print("Server stopped.")