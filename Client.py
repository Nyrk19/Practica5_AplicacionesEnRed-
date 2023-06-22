import socket

def send_request(client_socket, request):
        client_socket.sendall(request.encode('utf-8'))
        response = client_socket.recv(1024).decode('utf-8')
        return response

if __name__ == '__main__':
    host = '127.0.0.1'
    port = 8000

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    while True:
        choice = input("Seleccione GET, PUT o close: ")

        if choice.lower() == 'close':
            break
        elif choice.upper() == 'GET':
            path = input("Ingrese la ruta: ")
            get_request = 'GET {} HTTP/1.1\r\nHost: {}:{}\r\n\r\n'.format(path, host, port)
            get_response = send_request(client_socket, get_request)
            print('GET Response:')
            print(get_response)
        elif choice.upper() == 'PUT':
            path = input("Ingrese la ruta de subida: ")
            file_content = input("Ingrese el contenido del archivo: ")
            put_request = 'PUT {} HTTP/1.1\r\nHost: {}:{}\r\nContent-Type: text/plain\r\nContent-Length: {}\r\n\r\n{}'.format(
                path, host, port, len(file_content), file_content)
            put_response = send_request(client_socket, put_request)
            print('PUT Response:')
            print(put_response)
        else:
            print("Opción no válida. Seleccione GET, PUT o close.")