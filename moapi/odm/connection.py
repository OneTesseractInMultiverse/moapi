from abc import ABCMeta, abstractmethod
from pymongo import MongoClient, database

MONGO_CONN_SINGLE_HOST_PREFIX: str = "mongodb://"
MONGO_CONN_SRV_LOOKUP_PREFIX: str = "mongodb+srv://"
MONGO_TLS_REQUIRED_PARAM: str = "&tls=true"
MONGO_AUTH_SOURCE_PARAM: str = "?authSource="
MONGO_REPLICA_SET_PARAM: str = "&replicaSet="
MONGO_WITHOUT_REPLICA_SET: str = (
    ""  # When there is no replica set, we should pass an empty string
)
MONGO_WITHOUT_TLS: str = (
    ""  # When Mongo does not require TLS, we simply return empty string
)


class MongoDBParameters:
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def mongo_user(self) -> str:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def mongo_password(self) -> str:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def mongo_host(self) -> str:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def mongo_port(self) -> int:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def db_name(self) -> str:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def auth_source(self) -> str:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def requires_srv_lookup(self) -> bool:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def requires_tls(self) -> bool:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def is_cluster(self) -> bool:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    @abstractmethod
    def replica_set(self) -> str:
        # No need to test abstract methods
        pass  # pragma: no cover

    @property
    def replica_set_value(self):
        if self.is_cluster:
            return f"{MONGO_REPLICA_SET_PARAM}{self.replica_set}"
        return MONGO_WITHOUT_REPLICA_SET

    @property
    def tls_value(self) -> str:
        if self.requires_tls:
            return MONGO_TLS_REQUIRED_PARAM
        return MONGO_WITHOUT_TLS

    @property
    def auth_source_value(self):
        return f"{MONGO_AUTH_SOURCE_PARAM}{self.auth_source}"

    @property
    def base_connection(self) -> str:
        return (
            f"{self.mongo_user}:{self.mongo_password}@"
            f"{self.mongo_host}:{self.mongo_port}/{self.db_name}"
            f"{self.auth_source_value}"
            f"{self.replica_set_value}"
            f"{self.tls_value}"
        )

    @property
    def srv_lookup_connection_str(self) -> str:
        return f"{MONGO_CONN_SRV_LOOKUP_PREFIX}{self.base_connection}"

    @property
    def single_host_connection_str(self) -> str:
        return f"{MONGO_CONN_SINGLE_HOST_PREFIX}{self.base_connection}"

    @property
    def connection_with_prefix(self) -> str:
        if self.requires_srv_lookup:
            return self.srv_lookup_connection_str
        return self.single_host_connection_str

    @property
    def db(self) -> database.Database:
        # We don't unit-test this line because requires an
        # actual DB connection.
        return MongoClient(self.connection_with_prefix)[
            self.db_name
        ]  # pragma: no cover
