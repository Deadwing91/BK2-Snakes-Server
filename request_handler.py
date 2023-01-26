import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_species, get_single_species
from views import get_all_snakes, get_single_snake, create_snake, get_snakes_by_species
from views import get_single_owner, get_all_owners


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.
class HandleRequests(BaseHTTPRequestHandler):
    """_summary_ controls GET POST PUT DELETE reqeusts

    Args:
        BaseHTTPRequestHandler (_type_): _description_
    """
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        
        response = ""

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            ( resource, id ) = parsed

            if resource == "species":
                if id is not None:
                    response = get_single_species(id)

                    if response is not None:
                        self._set_headers(200)

                    else:
                        response = ""
                        self._set_headers(404)

                else:
                    self._set_headers(200)
                    response = get_all_species()

            elif resource == "snakes":
                if id is not None:
                    response = get_single_snake(id)

                    if response == "":
                        self._set_headers(405)

                    else:
                        self._set_headers(200)

                else:
                    self._set_headers(200)
                    response = get_all_snakes()

            elif resource == "owners":
                if id is not None:
                    response = get_single_owner(id)

                    if response is not None:
                        self._set_headers(200)

                    else:
                        response = ""
                        self._set_headers(404)

                else:
                    self._set_headers(200)
                    response = get_all_owners()

            else:
                self._set_headers(404)


        else: # There is a ? in the path, run the query param functions
            
            (resource, query) = parsed

            # see if the query dictionary has an email key

            if query.get('species') and resource == 'snakes':
                self._set_headers(200)
                response = get_snakes_by_species(query['species'][0])
        
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        """_summary_
        """
        
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new animal


        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "snakes":
            new_response = None

            if ("name" in post_body and "owner_id" in post_body and "species_id" in post_body
            and "gender" in post_body and "color" in post_body):
                self._set_headers(201)
                new_response = create_snake(post_body)

            else:
                self._set_headers(400)
                new_response = {
                      "message": f'{" name is required" if "name" not in post_body else ""} {" owner_id is required" if "owner_id" not in post_body else ""}{" species_id is required" if "species_id" not in post_body else ""}{" gender is required" if "gender" not in post_body else ""}{" color is required" if "color" not in post_body else ""}'
                }
                

        else:
            self._set_headers(404)
            new_response =""
            
        

        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_response).encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        """Handles PUT requests to the server"""
        self._set_headers(404)
        response = ''

        self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        response = ""
    # Set a 204 response code
        self._set_headers(404)

        self.wfile.write(json.dumps(response).encode())

    # Parse the URL

    # Delete a single animal from the list


    # Encode the new animal and send in response


    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
