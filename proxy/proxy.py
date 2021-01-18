import socket


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 28016))
    s.listen()
    conn, addr = s.accept()
    print('Connected by', addr)
    # Connected by('127.0.0.1', 54854)
    # b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=xylvqR28RzZY70ErNe7OPc6P"}\x00'

    db_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db_s.connect(('127.0.0.1', 28015))
    # Database>_b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00'

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print(f'Client>_{data}')
        db_s.sendall(data)

        data = db_s.recv(1024)
        if not data:
            break
        print(f'Database>_{data}')
        conn.sendall(data)