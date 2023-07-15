class MysqlConfig:
    def __init__(self, ip="127.0.0.1", port=0, username="test", password="", database="", pool_size=1, max_overflow=1,
                 timeout=3000,
                 pool_recycle=3000):
        self.ip = ip
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.timeout = timeout
        self.pool_recycle = pool_recycle
