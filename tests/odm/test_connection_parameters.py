from moapi.mocks.connection.mongo_parameters import (
    MongoDBParametersMock,
    MOCKED_USER,
    MOCKED_PWD,
    MOCKED_HOST,
    MOCKED_PORT,
    MOCKED_AUTH_SOURCE,
    MOCKED_DB_NAME,
    MOCKED_REPLICA_SET,
)
from moapi.odm.connection import (
    MongoDBParameters,
    MONGO_WITHOUT_REPLICA_SET,
    MONGO_REPLICA_SET_PARAM,
    MONGO_AUTH_SOURCE_PARAM,
    MONGO_TLS_REQUIRED_PARAM,
    MONGO_CONN_SINGLE_HOST_PREFIX,
    MONGO_CONN_SRV_LOOKUP_PREFIX,
)

BASE_CONNECTION_STRING: str = (
    f"{MOCKED_USER}:{MOCKED_PWD}@"
    f"{MOCKED_HOST}:{MOCKED_PORT}/{MOCKED_DB_NAME}"
    f"{MONGO_AUTH_SOURCE_PARAM}{MOCKED_AUTH_SOURCE}"
)
CONNECTION_STRING_FOR_REPLICA_SET: str = (
    f"{BASE_CONNECTION_STRING}"
    f"{MONGO_REPLICA_SET_PARAM}{MOCKED_REPLICA_SET}"
)
CONNECTION_STRING_WITH_TLS_ONLY: str = (
    f"{BASE_CONNECTION_STRING}" f"{MONGO_TLS_REQUIRED_PARAM}"
)

CONNECTION_STRING_FOR_TLS_CLUSTER: str = (
    f"{BASE_CONNECTION_STRING}"
    f"{MONGO_REPLICA_SET_PARAM}{MOCKED_REPLICA_SET}"
    f"{MONGO_TLS_REQUIRED_PARAM}"
)

FULL_CONNECTION_STRING_WITHOUT_SRV: str = (
    f"{MONGO_CONN_SINGLE_HOST_PREFIX}"
    f"{CONNECTION_STRING_FOR_TLS_CLUSTER}"
)

FULL_CONNECTION_STRING_WITH_SRV: str = (
    f"{MONGO_CONN_SRV_LOOKUP_PREFIX}"
    f"{CONNECTION_STRING_FOR_TLS_CLUSTER}"
)

MONGOMOCK_DB_NAME: str = "db"


def get_simple_parameter_mock() -> MongoDBParameters:
    return MongoDBParametersMock()


def get_parameter_mock_with_tls() -> MongoDBParameters:
    return MongoDBParametersMock(requires_tls=True)


def get_parameter_mock_for_cluster() -> MongoDBParameters:
    return MongoDBParametersMock(is_cluster=True)


def get_parameter_mock_with_srv_lookup() -> MongoDBParameters:
    return MongoDBParametersMock(requires_srv_lookup=True)


def get_parameter_mock_with_tls_and_cluster() -> MongoDBParameters:
    return MongoDBParametersMock(requires_tls=True, is_cluster=True)


def get_parameter_mock_with_tls_cluster_and_srv() -> MongoDBParameters:
    return MongoDBParametersMock(
        requires_tls=True, is_cluster=True, requires_srv_lookup=True
    )


class TestPropertyMappingsTestCases:
    def test_mongo_user(self):
        expected: str = MOCKED_USER
        actual: str = get_simple_parameter_mock().mongo_user
        assert expected == actual

    def test_mongo_password(self):
        expected: str = MOCKED_PWD
        actual: str = get_simple_parameter_mock().mongo_password
        assert expected == actual

    def test_mongo_host(self):
        expected: str = MOCKED_HOST
        actual: str = get_simple_parameter_mock().mongo_host
        assert expected == actual

    def test_mongo_port(self):
        expected: int = MOCKED_PORT
        actual: int = get_simple_parameter_mock().mongo_port
        assert expected == actual

    def test_db_name(self):
        expected: str = MOCKED_DB_NAME
        actual: str = get_simple_parameter_mock().db_name
        assert expected == actual

    def test_auth_source(self):
        expected: str = MOCKED_AUTH_SOURCE
        actual: str = get_simple_parameter_mock().auth_source
        assert expected == actual

    def test_replica_set(self):
        expected: str = MOCKED_REPLICA_SET
        actual: str = get_simple_parameter_mock().replica_set
        assert expected == actual

    def test_when_does_not_require_srv_lookup(self):
        expected: bool = False
        actual: bool = get_simple_parameter_mock().requires_srv_lookup
        assert expected == actual

    def test_when_require_srv_lookup(self):
        expected: bool = True
        actual: bool = (
            get_parameter_mock_with_srv_lookup().requires_srv_lookup
        )
        assert expected == actual

    def test_when_require_tls(self):
        expected: bool = True
        actual: bool = get_parameter_mock_with_tls().requires_tls
        assert expected == actual

    def test_when_does_not_require_tls(self):
        expected: bool = False
        actual: bool = get_simple_parameter_mock().requires_tls
        assert expected == actual

    def test_when_is_cluster(self):
        expected: bool = True
        actual: bool = get_parameter_mock_for_cluster().is_cluster
        assert expected == actual

    def test_when_is_not_cluster(self):
        expected: bool = False
        actual: bool = get_simple_parameter_mock().is_cluster
        assert expected == actual


class TestConnectionStringTestCases:
    def test_replica_set_value_when_no_replica_set(self):
        expected: str = MONGO_WITHOUT_REPLICA_SET
        actual: str = get_simple_parameter_mock().replica_set_value
        assert expected == actual

    def test_replica_set_value_when_replica_set(self):
        expected: str = f"{MONGO_REPLICA_SET_PARAM}{MOCKED_REPLICA_SET}"
        actual: str = get_parameter_mock_for_cluster().replica_set_value
        assert expected == actual

    def test_base_connection_string(self):
        expected: str = BASE_CONNECTION_STRING
        actual: str = get_simple_parameter_mock().base_connection
        assert expected == actual

    def test_base_connection_for_cluster(self):
        expected: str = CONNECTION_STRING_FOR_REPLICA_SET
        actual: str = get_parameter_mock_for_cluster().base_connection
        assert expected == actual

    def test_base_connection_for_cluster_with_tls(self):
        expected: str = CONNECTION_STRING_FOR_TLS_CLUSTER
        actual: str = (
            get_parameter_mock_with_tls_and_cluster().base_connection
        )
        assert expected == actual

    def test_base_connection_with_tls(self):
        expected: str = CONNECTION_STRING_WITH_TLS_ONLY
        actual: str = get_parameter_mock_with_tls().base_connection
        assert expected == actual

    def test_full_connection_string_without_srv(self):
        expected: str = FULL_CONNECTION_STRING_WITHOUT_SRV
        actual: str = (
            get_parameter_mock_with_tls_and_cluster().connection_with_prefix
        )
        assert expected == actual

    def test_full_connection_string_with_srv(self):
        expected: str = FULL_CONNECTION_STRING_WITH_SRV
        parameters = get_parameter_mock_with_tls_cluster_and_srv()
        actual: str = parameters.connection_with_prefix
        assert expected == actual


class TestDBProperty:
    def test_db_name_in_database_obj(self):
        expected: str = MONGOMOCK_DB_NAME
        parameters = get_parameter_mock_with_tls_cluster_and_srv()
        actual: str = parameters.db.name
        assert expected == actual
