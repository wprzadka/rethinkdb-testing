import time
import couchdb


class CouchTest:
    def __init__(self, schema: str, recreate: bool):
        user = "admin"
        password = "password"
        self.couchserver = couchdb.Server("http://%s:%s@127.0.0.1:5984/" % (user, password))

        if recreate and schema in self.couchserver:
            del self.couchserver[schema]
        try:
            self.db = self.couchserver[schema]
        except couchdb.http.ResourceNotFound:
            self.db = self.couchserver.create(schema)

    def test_inserts_efficiency(self, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            self.db.save({'id': idx, 'time': time.time() - start})
            idx += 1

        print('test finished')

    def test_read_write_efficiency(self, inserts_num: int):
        idx = 0
        print('test started')

        start = time.time()
        while idx < inserts_num:
            self.db.save({'id': idx, 'time': time.time() - start})
            for i in self.db:
                self.db.get(i)
            idx += 1
        print('test finished')

    def get_results(self, schema: str) -> list:
        db = self.couchserver[schema]
        return list(db.get(i) for i in db)