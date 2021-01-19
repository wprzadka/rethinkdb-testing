import socket
import threading


def resend_data(source: socket.socket, destination: socket.socket, name: str):
    while True:
        data = source.recv(4096)
        if data:
            print(f'{name}>_{data}\n')
            destination.sendall(data)

        # data = b''
        # while not data or data[-1] != '\x00':
        #     buffer = source.recv(4096)
        #     if buffer:
        #         data += buffer
        #         print(data)
        # print(f'{source}\n>_{data}\n')
        # destination.sendall(data)


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', 28016))
    s.listen(1)
    conn, addr = s.accept()
    print('Connected by', addr)
    # Connected by('127.0.0.1', 54854)
    # b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=xylvqR28RzZY70ErNe7OPc6P"}\x00'

    db_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db_s.connect(('127.0.0.1', 28015))
    # Database>_b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00'

    threading.Thread(target=resend_data, args=(db_s, conn, 'server'), daemon=True).start()
    threading.Thread(target=resend_data, args=(conn, db_s, 'client'), daemon=True).start()

    while True:
        pass

# RFC-SCRAM: https://tools.ietf.org/html/rfc5802

"""
Successful connection (admin with no password)

/home/viking/ComputerScience/software_testing/rethinkdb-testing/venv/bin/python /home/viking/ComputerScience/software_testing/rethinkdb-testing/proxy/proxy.py
Connected by ('127.0.0.1', 39784)
client>_b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=0l62h/2njEnD9WK/inEqzkwR"}\x00'

server>_b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00{"authentication":"r=0l62h/2njEnD9WK/inEqzkwRryYtqRu0hGs6kv1tChj1,s=3NAR/QjYMcmVUvOqb+39FA==,i=1","success":true}\x00'

client>_b'{"authentication":"c=biws,r=0l62h/2njEnD9WK/inEqzkwRryYtqRu0hGs6kv1tChj1,p=mSBqgovxkbl/iK5+fTpmv+JQ6knBIP5nFZbl3s2f9N0="}\x00'

server>_b'{"authentication":"v=K5UecvnvVL4eb1LJ1FbTMqMBiFdCl1X5YhFzy2HJNoE=","success":true}\x00'

client>_b'\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x00\x00\x00[1,[62,[[14,["test"]]]],{}]'

server>_b'\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00{"t":1,"r":[["proxy_test","read_write"]]}'

client>_b'\x01\x00\x00\x00\x00\x00\x00\x00N\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.066173}]],{}]'

server>_b'\x01\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["38c043ed-337a-4aca-b7c7-42ade11b5c14"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x02\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x02\x00\x00\x00\x00\x00\x00\x00!\x01\x00\x00{"t":2,"r":[{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245}],"n":[]}'

client>_b'\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]\x03\x00\x00\x00\x00\x00\x00\x00N\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.140078}]],{}]'

server>_b'\x02\x00\x00\x00\x00\x00\x00\x004\x00\x00\x00{"t":16,"r":["Token 2 not in stream cache."],"b":[]}'

server>_b'\x03\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["3b353614-a8a3-40f4-b692-ada79be47f31"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x04\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x04\x00\x00\x00\x00\x00\x00\x00z\x01\x00\x00{"t":2,"r":[{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245}],"n":[]}'

client>_b'\x04\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]\x05\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.2195728}]],{}]'

server>_b'\x04\x00\x00\x00\x00\x00\x00\x004\x00\x00\x00{"t":16,"r":["Token 4 not in stream cache."],"b":[]}'

server>_b'\x05\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["c0b88ff0-1ede-4728-bd51-610a659c5a51"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x06\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x06\x00\x00\x00\x00\x00\x00\x00\xd4\x01\x00\x00{"t":2,"r":[{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\x06\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]\x07\x00\x00\x00\x00\x00\x00\x00M\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.31306}]],{}]'

server>_b'\x06\x00\x00\x00\x00\x00\x00\x004\x00\x00\x00{"t":16,"r":["Token 6 not in stream cache."],"b":[]}'

server>_b'\x07\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x08\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x08\x00\x00\x00\x00\x00\x00\x00,\x02\x00\x00{"t":2,"r":[{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\x08\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]\t\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.3866408}]],{}]'

server>_b'\x08\x00\x00\x00\x00\x00\x00\x004\x00\x00\x00{"t":16,"r":["Token 8 not in stream cache."],"b":[]}'

server>_b'\t\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["47b34ff0-0f3a-4028-9f0d-fc49eaec63bf"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\n\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\n\x00\x00\x00\x00\x00\x00\x00\x86\x02\x00\x00{"t":2,"r":[{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\n\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]\x0b\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.4395635}]],{}]'

server>_b'\n\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00{"t":16,"r":["Token 10 not in stream cache."],"b":[]}'

server>_b'\x0b\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["7976017f-8e3d-47b5-80ce-1be5ed4ce866"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x0c\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x0c\x00\x00\x00\x00\x00\x00\x00\xe0\x02\x00\x00{"t":2,"r":[{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"7976017f-8e3d-47b5-80ce-1be5ed4ce866","source":"client","time":1611049616.4395636},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\x0c\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]\r\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.4894383}]],{}]'

server>_b'\x0c\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00{"t":16,"r":["Token 12 not in stream cache."],"b":[]}'

server>_b'\r\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["dbd9e0da-e3ef-4b4b-b6f5-2987aa326538"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x0e\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x0e\x00\x00\x00\x00\x00\x00\x00:\x03\x00\x00{"t":2,"r":[{"id":"dbd9e0da-e3ef-4b4b-b6f5-2987aa326538","source":"client","time":1611049616.4894384},{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"7976017f-8e3d-47b5-80ce-1be5ed4ce866","source":"client","time":1611049616.4395636},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\x0e\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'

server>_b'\x0e\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00{"t":16,"r":["Token 14 not in stream cache."],"b":[]}'

client>_b'\x0f\x00\x00\x00\x00\x00\x00\x00N\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.543412}]],{}]'

server>_b'\x0f\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["40bbc737-758f-47e0-bb97-cf5b28cbef27"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x10\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x10\x00\x00\x00\x00\x00\x00\x00\x93\x03\x00\x00{"t":2,"r":[{"id":"dbd9e0da-e3ef-4b4b-b6f5-2987aa326538","source":"client","time":1611049616.4894384},{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"40bbc737-758f-47e0-bb97-cf5b28cbef27","source":"client","time":1611049616.543412},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"7976017f-8e3d-47b5-80ce-1be5ed4ce866","source":"client","time":1611049616.4395636},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\x10\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'

client>_b'\x11\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.6141415}]],{}]'

server>_b'\x10\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00{"t":16,"r":["Token 16 not in stream cache."],"b":[]}'

server>_b'\x11\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["7a0d5c1a-3e96-4453-ac00-4d0ef35184fc"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x12\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x12\x00\x00\x00\x00\x00\x00\x00\xed\x03\x00\x00{"t":2,"r":[{"id":"7a0d5c1a-3e96-4453-ac00-4d0ef35184fc","source":"client","time":1611049616.6141415},{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"40bbc737-758f-47e0-bb97-cf5b28cbef27","source":"client","time":1611049616.543412},{"id":"dbd9e0da-e3ef-4b4b-b6f5-2987aa326538","source":"client","time":1611049616.4894384},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"7976017f-8e3d-47b5-80ce-1be5ed4ce866","source":"client","time":1611049616.4395636},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729}],"n":[]}'

client>_b'\x12\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'

client>_b'\x13\x00\x00\x00\x00\x00\x00\x00O\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611049616.8132355}]],{}]'

server>_b'\x12\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00{"t":16,"r":["Token 18 not in stream cache."],"b":[]}'

server>_b'\x13\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["47252966-1de0-43c1-8ea1-532f2e9b2340"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x14\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x14\x00\x00\x00\x00\x00\x00\x00G\x04\x00\x00{"t":2,"r":[{"id":"7a0d5c1a-3e96-4453-ac00-4d0ef35184fc","source":"client","time":1611049616.6141415},{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"47252966-1de0-43c1-8ea1-532f2e9b2340","source":"client","time":1611049616.8132356},{"id":"40bbc737-758f-47e0-bb97-cf5b28cbef27","source":"client","time":1611049616.543412},{"id":"dbd9e0da-e3ef-4b4b-b6f5-2987aa326538","source":"client","time":1611049616.4894384},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729},{"id":"7976017f-8e3d-47b5-80ce-1be5ed4ce866","source":"client","time":1611049616.4395636}],"n":[]}'

client>_b'\x14\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'

server>_b'\x14\x00\x00\x00\x00\x00\x00\x005\x00\x00\x00{"t":16,"r":["Token 20 not in stream cache."],"b":[]}'
"""

"""
No password provided (admin with password)

/home/viking/ComputerScience/software_testing/rethinkdb-testing/venv/bin/python /home/viking/ComputerScience/software_testing/rethinkdb-testing/proxy/proxy.py
Connected by ('127.0.0.1', 33846)
client>_b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=hSWAcdXLAOSCxIrON7Lo6zIj"}\x00'

server>_b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00{"authentication":"r=hSWAcdXLAOSCxIrON7Lo6zIj0GOMs9mVvupKBEX+o2mJ,s=/alRLo0bmsVf9VXrfVlGMA==,i=4096","success":true}\x00'

client>_b'{"authentication":"c=biws,r=hSWAcdXLAOSCxIrON7Lo6zIj0GOMs9mVvupKBEX+o2mJ,p=SpRBZf1TcgNa/qiV3ZlO1nH611l7LDSZkRuh+sGxZ9o="}\x00'

server>_b'{"error":"Wrong password","error_code":12,"success":false}\x00'
"""

"""
Wrong password provided (admin with password)

/home/viking/ComputerScience/software_testing/rethinkdb-testing/venv/bin/python /home/viking/ComputerScience/software_testing/rethinkdb-testing/proxy/proxy.py
Connected by ('127.0.0.1', 33898)
client>_b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=JE11h8+NHC2s2umxhxvt9qTw"}\x00'

server>_b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00{"authentication":"r=JE11h8+NHC2s2umxhxvt9qTwv+ZR7RdJr0sJX41qlhmU,s=/alRLo0bmsVf9VXrfVlGMA==,i=4096","success":true}\x00'

client>_b'{"authentication":"c=biws,r=JE11h8+NHC2s2umxhxvt9qTwv+ZR7RdJr0sJX41qlhmU,p=IPy9FL2n9DoyF7pQMT9vZUBCR/7j6gxmodvba5B2nU0="}\x00'

server>_b'{"error":"Wrong password","error_code":12,"success":false}\x00'
"""

"""
Correct password provided (admin with password)

/home/viking/ComputerScience/software_testing/rethinkdb-testing/venv/bin/python /home/viking/ComputerScience/software_testing/rethinkdb-testing/proxy/proxy.py
Connected by ('127.0.0.1', 33700)
client>_b'\xc3\xbd\xc24{"protocol_version":0,"authentication_method":"SCRAM-SHA-256","authentication":"n,,n=admin,r=8c3hggOC20viQwBrisXbqwgd"}\x00'

server>_b'{"max_protocol_version":0,"min_protocol_version":0,"server_version":"2.3.2-windows-beta-584-gffe554","success":true}\x00{"authentication":"r=8c3hggOC20viQwBrisXbqwgdeTJZXCPKnC/tc3cvaRna,s=/alRLo0bmsVf9VXrfVlGMA==,i=4096","success":true}\x00'

client>_b'{"authentication":"c=biws,r=8c3hggOC20viQwBrisXbqwgdeTJZXCPKnC/tc3cvaRna,p=JXaKP2ZmiVv0qx8d4qzKl9gp2EAYXcmDETFAHBGfCgo="}\x00'

server>_b'{"authentication":"v=Gna2xpTL+jKZ6kBIstU4LMr4TriaPHFAHqAtjdLxuwQ=","success":true}\x00'

client>_b'\x00\x00\x00\x00\x00\x00\x00\x00\x1b\x00\x00\x00[1,[62,[[14,["test"]]]],{}]'

server>_b'\x00\x00\x00\x00\x00\x00\x00\x00)\x00\x00\x00{"t":1,"r":[["proxy_test","read_write"]]}'

client>_b'\x01\x00\x00\x00\x00\x00\x00\x00N\x00\x00\x00[1,[56,[[15,["proxy_test"]],{"source":"client","time":1611069184.514635}]],{}]'

server>_b'\x01\x00\x00\x00\x00\x00\x00\x00\x94\x00\x00\x00{"t":1,"r":[{"deleted":0,"errors":0,"generated_keys":["3c7e68d0-7a30-49f6-a7c3-aab4e96e0c81"],"inserted":1,"replaced":0,"skipped":0,"unchanged":0}]}'

client>_b'\x02\x00\x00\x00\x00\x00\x00\x00\x1a\x00\x00\x00[1,[15,["proxy_test"]],{}]'

server>_b'\x02\x00\x00\x00\x00\x00\x00\x00T\x05\x00\x00{"t":2,"r":[{"id":"7a0d5c1a-3e96-4453-ac00-4d0ef35184fc","source":"client","time":1611049616.6141415},{"id":"15ee7744-2a65-4419-bd3b-e5ea9c096b0e","source":"client","time":1611054261.9381009},{"id":"05508e73-fc14-436f-b3b4-fe754cc23a3c","source":"client","time":1611041460.9776812},{"id":"3b353614-a8a3-40f4-b692-ada79be47f31","source":"client","time":1611049616.140078},{"id":"47252966-1de0-43c1-8ea1-532f2e9b2340","source":"client","time":1611049616.8132356},{"id":"40bbc737-758f-47e0-bb97-cf5b28cbef27","source":"client","time":1611049616.543412},{"id":"dbd9e0da-e3ef-4b4b-b6f5-2987aa326538","source":"client","time":1611049616.4894384},{"id":"38c043ed-337a-4aca-b7c7-42ade11b5c14","source":"client","time":1611049616.066173},{"id":"3d0895c6-0809-4f6f-9a93-9a2331dad04b","source":"client","time":1611040388.2464245},{"id":"9927facd-daf1-45b9-a6eb-ceed3b2a4665","source":"client","time":1611069000.0708175},{"id":"3c7e68d0-7a30-49f6-a7c3-aab4e96e0c81","source":"client","time":1611069184.514635},{"id":"c0b88ff0-1ede-4728-bd51-610a659c5a51","source":"client","time":1611049616.2195729},{"id":"a36ba2dd-ffc3-4479-b834-e7c9a0e9d7d6","source":"client","time":1611049616.31306},{"id":"7976017f-8e3d-47b5-80ce-1be5ed4ce866","source":"client","time":1611049616.4395636},{"id":"47b34ff0-0f3a-4028-9f0d-fc49eaec63bf","source":"client","time":1611049616.3866409}],"n":[]}'

client>_b'\x02\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00[2]'

server>_b'\x02\x00\x00\x00\x00\x00\x00\x004\x00\x00\x00{"t":16,"r":["Token 2 not in stream cache."],"b":[]}'
"""