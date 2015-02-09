import socket
import sys
import mimetypes
import os.path


def response_ok():
    """returns a basic HTTP response"""
    resp = []
    resp.append("HTTP/1.1 200 OK")
    resp.append("Content-Type: text/plain")
    resp.append("")
    resp.append("this is a pretty minimal response")
    return "\r\n".join(resp)


def response_method_not_allowed():
    """returns a 405 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 405 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)


def parse_request(request):
    first_line = request.split("\r\n", 1)[0]
    method, uri, protocol = first_line.split()
    if method != "GET":
        raise NotImplementedError("We only accept GET")
    print >>sys.stderr, 'request is okay'
    return uri


def resolve_uri(uri):

    # this should check if the path exists, if it doesn't, call response not found to return 404 error
    if not os.path.exists(uri):
        response_not_found()

    file_name, extension = os.path.splitext(uri)

    if os.path.isdir(uri):
        return "" #this is where I'll return list if is a directory
    if os.path.isfile(uri):
        return "" #this can be where I return if uri points to a file (need else to raise error if none of these catch?)
    content = ""
    type = mimetypes.types_map[extension]
    return (content, type)
    

def response_not_found():
    """returns a 404 Method Not Allowed response"""
    resp = []
    resp.append("HTTP/1.1 404 Method Not Allowed")
    resp.append("")
    return "\r\n".join(resp)


def server():
    address = ('127.0.0.1', 10000)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print >>sys.stderr, "making a server on %s:%s" % address
    sock.bind(address)
    sock.listen(1)

    try:
        while True:
            print >>sys.stderr, 'waiting for a connection'
            conn, addr = sock.accept() # blocking
            try:
                print >>sys.stderr, 'connection - %s:%s' % addr
                request = ""
                while True:
                    data = conn.recv(1024)
                    request += data
                    if len(data) < 1024 or not data:
                        break

                try:
                    uri = parse_request(request)
                except NotImplementedError:
                    response = response_method_not_allowed()
                else:
                    # replace this line with the following once you have
                    # written resolve_uri
                    response = response_ok()
                    # content, type = resolve_uri(uri) # change this line

                    ## uncomment this try/except block once you have fixed
                    ## response_ok and added response_not_found
                    # try:
                    #     response = response_ok(content, type)
                    # except NameError:
                    #     response = response_not_found()

                print >>sys.stderr, 'sending response'
                conn.sendall(response)
            finally:
                conn.close()

    except KeyboardInterrupt:
        sock.close()
        return


if __name__ == '__main__':
    server()
    sys.exit(0)
