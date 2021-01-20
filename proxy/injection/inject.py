import socket

"""
Client side messages to inject:

b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=hwE9dR7VXM3SYzl/IncHqRGU"}\x00'
b'{"authentication":"c=biws,r=hwE9dR7VXM3SYzl/IncHqRGUrDOaBeVeWsjYKQjOha5Z,p=FzQHVoX5sC1xVSQZ+8Uyem77egCJwdDHbdtdy9FPANs="}\x00'
b'\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x00\x00\x00[1,[62,[[14,["test"]]]],{}]'
b'\x01\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611125615.1374214}]],{}]'
b'\x02\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'
b'\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'
"""

prepared_messages = [
    b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=hwE9dR7VXM3SYzl/IncHqRGU"}\x00',
    b'{"authentication":"c=biws,r=hwE9dR7VXM3SYzl/IncHqRGUrDOaBeVeWsjYKQjOha5Z,p=FzQHVoX5sC1xVSQZ+8Uyem77egCJwdDHbdtdy9FPANs="}\x00',
    b'\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x00\x00\x00[1,[62,[[14,["test"]]]],{}]',
    b'\x01\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"injector","time":1611125615.1374214}]],{}]',
    b'\x02\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]',
    b'\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'
]

if __name__ == '__main__':
    db_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db_s.connect(('127.0.0.1', 28015))

    for msg in prepared_messages:
        db_s.sendall(msg)
        data = None
        while not data:
            data = db_s.recv(4096)
        print(data)

"""
Server responses

b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00'
b'{"authentication":"r=hwE9dR7VXM3SYzl/IncHqRGUNdm6G6kuZKALxIdud9U9,s=/alRLo0bmsVf9VXrfVlGMA==,i=4096","success":true}\x00'
b'{"error":"Wrong password","error_code":12,"success":false}\x00'
"""
"""
b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00'
b'{"authentication":"r=hwE9dR7VXM3SYzl/IncHqRGUaFLDYhxd1BQ9k53Mjs94,s=/alRLo0bmsVf9VXrfVlGMA==,i=4096","success":true}\x00'
b'{"error":"Wrong password","error_code":12,"success":false}\x00'
"""


"""
Server responses for auth with wrong name

b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00'
b'{"authentication":"r=hwE9dR7VXM3SYzl/IncHqRGUMvGUClYXHVqQl1MezZKM,s=C3QEaJmaadJe9sSwxAaMKg==,i=4096","success":true}\x00'
b'{"error":"Unknown user","error_code":17,"success":false}\x00'
"""

"""
Server response for modified "c" field [{"authentication":"c=bqws,..]

b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00'
b'{"authentication":"r=hwE9dR7VXM3SYzl/IncHqRGUUDnnbqL0WEZFC7wzfa7Z,s=/alRLo0bmsVf9VXrfVlGMA==,i=4096","success":true}\x00'
b'{"error":"Invalid encoding","error_code":10,"success":false}\x00'
"""