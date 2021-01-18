import socket

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('127.0.0.1', 28016))
        s.listen()
        conn, addr = s.accept()
        # Connected by('127.0.0.1', 54854)
        # b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=xylvqR28RzZY70ErNe7OPc6P"}\x00'

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data)