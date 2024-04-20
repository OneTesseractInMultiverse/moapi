import mongomock
from pymongo import database

from moapi.odm.connection import MongoDBParameters

MOCKED_USER: str = "mocked_user"
MOCKED_PWD: str = "mocked_pwd"
MOCKED_HOST: str = "mongo.example.com"
MOCKED_PORT: int = 27017
MOCKED_DB_NAME: str = "sample"
MOCKED_AUTH_SOURCE: str = "admin"
MOCKED_REPLICA_SET: str = "my_cluster"


class MongoDBParametersMock(MongoDBParameters):
    def __init__(
        self,
        requires_tls: bool = False,
        is_cluster: bool = False,
        requires_srv_lookup: bool = False,
    ):
        self.mocked_requires_tls: bool = requires_tls
        self.mocked_is_cluster: bool = is_cluster
        self.mocked_requires_srv: bool = requires_srv_lookup

    @property
    def mongo_user(self) -> str:
        return MOCKED_USER

    @property
    def mongo_password(self) -> str:
        return MOCKED_PWD

    @property
    def mongo_host(self) -> str:
        return MOCKED_HOST

    @property
    def mongo_port(self) -> int:
        return MOCKED_PORT

    @property
    def db_name(self) -> str:
        return MOCKED_DB_NAME

    @property
    def auth_source(self) -> str:
        return MOCKED_AUTH_SOURCE

    @property
    def requires_srv_lookup(self) -> bool:
        return self.mocked_requires_srv

    @property
    def requires_tls(self) -> bool:
        return self.mocked_requires_tls

    @property
    def is_cluster(self) -> bool:
        return self.mocked_is_cluster

    @property
    def replica_set(self) -> str:
        return MOCKED_REPLICA_SET

    @property
    def db(self) -> database.Database:
        """
        Returns an instance of MongoMock that will behave like
        a real MongoDB instance but runs entirely from memory
        and does not require an actual MongoDB instance.
        :return:
        """
        return mongomock.MongoClient().db
