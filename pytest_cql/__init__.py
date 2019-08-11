from __future__ import print_function

import os.path
import tempfile
from contextlib import contextmanager
import shutil

import pytest
from _pytest.python import FunctionDefinition
from ccmlib.scylla_cluster import ScyllaCluster
from cassandra.cluster import Cluster  # pylint: disable=no-name-in-module


@contextmanager
def cql_session(node, **kwargs):
    node_ip, node_port = node.network_interfaces["binary"]

    with Cluster(
        [node_ip],
        port=node_port,
        connect_timeout=5,
        max_schema_agreement_wait=60,
        control_connection_timeout=6.0,
        **kwargs
    ) as cluster:
        yield cluster.connect()


def pytest_addoption(parser):
    parser.addoption("--scylla-version", help="run all combinations")
    parser.addoption("--scylla-directory", help="run all combinations")
    parser.addoption(
        "--keep-cluster",
        action="store_true",
        help="decide if to remove cluster directory",
    )


@pytest.fixture(scope="session")
def test_path(request):
    dtest_root = os.path.join(os.path.expanduser("~"), ".cql-test")
    if not os.path.exists(dtest_root):
        os.makedirs(dtest_root)
    temp_dir = tempfile.mkdtemp(dir=dtest_root, prefix="cql-test-")

    yield temp_dir

    keep_cluster = request.config.getoption("--keep-cluster", False)
    if not keep_cluster:
        shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture(scope="session")
def scylla_1_node_cluster(request, test_path):  # pylint: disable=redefined-outer-name
    name = "cql-test"

    scylla_version = request.config.getoption("--scylla-version", None)
    scylla_directory = request.config.getoption("--scylla-directory", None)

    if scylla_version and scylla_directory:
        raise ValueError(
            "can't use both --scylla-version and --scylla-directory, choose one"
        )
    if not scylla_version and not scylla_directory:
        raise ValueError(
            "need to use --scylla-version or --scylla-directory, choose one"
        )

    if scylla_version:
        cluster = ScyllaCluster(test_path, name, cassandra_version=scylla_version)

    if scylla_directory:
        cluster = ScyllaCluster(
            test_path,
            name,
            cassandra_dir=scylla_directory,
            install_dir=scylla_directory,
        )

    _id = 2
    cluster.set_id(_id)
    cluster.set_ipprefix("127.0.%d." % _id)
    cluster.set_configuration_options({"skip_wait_for_gossip_to_settle": 0})
    cluster.populate(1)
    cluster.start()
    yield cluster

    cluster.stop()
    keep_cluster = request.config.getoption("--keep-cluster", False)
    if not keep_cluster:
        cluster.remove()


@pytest.mark.usefixtures("scylla_1_node_cluster")
def test_function():
    # function to hold the default fixture cql test would use
    pass


def pytest_collect_file(parent, path):
    if path.basename.endswith(".test.cql"):
        return CqlFile(path, parent)
    return None


class CqlFile(pytest.File):
    obj = test_function

    def collect(self):
        fixture_manager = (
            self.session._fixturemanager  # pylint: disable=protected-access
        )
        definition = FunctionDefinition(
            name="test_function", parent=self, callobj=test_function
        )
        fixtureinfo = fixture_manager.getfixtureinfo(definition, test_function, None)
        # TODO: read the file and add/replace fixtures
        yield CqlItem(
            os.path.relpath(self.fspath), self, self.fspath, test_function, fixtureinfo
        )


class CqlItem(pytest.Function):  # pylint: disable=too-many-ancestors
    def __init__(
        self, name, parent, filename, callobj, fixtureinfo
    ):  # pylint: disable=too-many-arguments
        super(CqlItem, self).__init__(
            name, parent, callobj=callobj, fixtureinfo=fixtureinfo
        )
        self.filename = filename

    def runtest(self):
        cluster = self.funcargs.get("scylla_1_node_cluster")

        with cql_session(cluster.nodelist()[0]) as session:
            for line in open(self.filename):
                print(line.strip())
                return_value = session.execute(line)
                response = [list(row) for row in return_value]
                if response:
                    print("# {}".format(response))
