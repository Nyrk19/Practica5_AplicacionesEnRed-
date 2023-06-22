import socket
import threading

def parse_request(request):
    lines = request.split('\r\n')
    method, path, _ = lines[0].split(' ')
    headers = {}
    for line in lines[1:]:
        if line:
            if ': ' in line:
                key, value = line.split(': ')
                headers[key] = value
    return method, path, headers

def build_response(status_code, status_text, headers, body):
    response = 'HTTP/1.1 {} {}\r\n'.format(status_code, status_text)
    for key, value in headers.items():
        response += '{}: {}\r\n'.format(key, value)
    response += '\r\n'
    if body:
        response += body
    return response

def handle_request(request):
    method, path, headers = parse_request(request)

    if method == 'GET' and path == '/':
        status_code = 200
        status_text = 'OK'
        body = '<h1>Bienvenido al servidor HTTP!</h1>'
        headers = {
            'Content-Type': 'text/html',
            'Content-Length': str(len(body))
        }
    elif method == 'GET' and path == '/data':
        status_code = 200
        status_text = 'OK'
        body = 'Algunos datos del servidor'
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': str(len(body))
        }
    elif method == 'GET' and path == '/test':
        status_code = 200
        status_text = 'OK'
        body = 'Esta es una respuesta de test'
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': str(len(body))
        }
    elif method == 'PUT' and path == '/upload':
        status_code = 200
        status_text = 'OK'
        body = 'Archivo subido correctamente'
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': str(len(body))
        }
    elif method == 'PUT' and path == '/update':
        status_code = 200
        status_text = 'OK'
        body = 'Recurso actualizado correctamente'
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': str(len(body))
        }
    else:
        status_code = 404
        status_text = 'Not Found'
        body = '404 Pagina no encontrada'
        headers = {
            'Content-Type': 'text/plain',
            'Content-Length': str(len(body))
        }

    response = build_response(status_code, status_text, headers, body)
    return response

def handle_client(client_socket, address):
    print('Conecatado a: ', address)

    while True:
        # Establecimiento de la conexión
        request = client_socket.recv(1024).decode('utf-8')
        if request !='':
            print("request recibido: ", request)
            if request is not None:
                print('Recibiendo solicitud de {}:'.format(address))

                # Recepción de la solicitud
                response = handle_request(request)

                print('Enviando respuesta:')
                print(response)

                # Envío de respuesta
                client_socket.sendall(response.encode('utf-8'))

def run_server():
    host = '127.0.0.1'
    port = 8000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print('Escuchando en {}:{}'.format(host, port))

    while True:
        client_socket, address = server_socket.accept()

        # Handle each client connection in a separate thread
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.start()

if __name__ == '__main__':
    run_server()
