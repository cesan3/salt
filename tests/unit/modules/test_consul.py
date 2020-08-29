# Import Python libs

import salt.modules.consul as consul

# Import Salt Libs
import salt.utils.http
import salt.utils.json
from salt.exceptions import SaltInvocationError
from salt.ext.six.moves import http_client

# Import Salt Testing Libs
from tests.support.mixins import LoaderModuleMockMixin
from tests.support.mock import MagicMock, patch
from tests.support.unit import TestCase


class ConsulTestCase(TestCase, LoaderModuleMockMixin):
    """
    Test cases for salt.modules.consul
    """

    def setup_loader_modules(self):
        return {consul: {}}

    def test_get(self):
        """
        Test for get a consul key/value
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = {"test": "good"}
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.put(consul_url="", key=key, value="test")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                result = consul.get(consul_url=consul_url, key=key)
                expected = {"data": mock_result, "res": True}
                self.assertEqual(expected, result)

    def test_put(self):
        """
        Test for put a consul key/value
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = {"test": "good"}
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.put(consul_url="", key=key, value="test")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        # no key
        with patch.dict(consul.__salt__, {"config.get": mock_url}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                self.assertRaises(
                    SaltInvocationError,
                    consul.put,
                    consul_url="",
                    key=None,
                    value="test",
                )
                self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Added key cluster/key with value {}."
                    value = "string test"
                    result = consul.put(consul_url=consul_url, key=key, value=value)
                    expected = {"data": msg.format(value), "res": True}
                    self.assertEqual(expected, result)

                    value = {"dict": "test"}
                    result = consul.put(consul_url=consul_url, key=key, value=value)
                    expected = {"data": msg.format(value), "res": True}
                    self.assertEqual(expected, result)

                    value = ["item1", "item2"]
                    result = consul.put(consul_url=consul_url, key=key, value=value)
                    expected = {"data": msg.format(value), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to add key cluster/key with value {}."
                    value = "string test"
                    result = consul.put(consul_url=consul_url, key=key, value=value)
                    expected = {"data": msg.format(value), "res": False}
                    self.assertEqual(expected, result)

    def test_delete(self):
        """
        Test for delete consul key/value
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = {"test": "good"}
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value="http://test")
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.delete(consul_url="", key=key)
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Deleted key cluster/key."
                    value = "string test"
                    result = consul.delete(consul_url=consul_url, key=key)
                    expected = {
                        "data": mock_result,
                        "message": msg.format(value),
                        "res": True,
                    }
                    self.assertEqual(expected, result)

                    value = {"dict": "test"}
                    result = consul.delete(consul_url=consul_url, key=key)
                    expected = {
                        "data": mock_result,
                        "message": msg.format(value),
                        "res": True,
                    }
                    self.assertEqual(expected, result)

                    value = ["item1", "item2"]
                    result = consul.delete(consul_url=consul_url, key=key)
                    expected = {
                        "data": mock_result,
                        "message": msg.format(value),
                        "res": True,
                    }
                    self.assertEqual(expected, result)

    def test_agent_maintenance(self):
        """
        Test consul agent maintenance
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_maintenance(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        # no required argument
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = 'Required parameter "enable" is missing.'
                    result = consul.agent_maintenance(consul_url=consul_url)
                    expected = {"message": msg, "res": False}
                    self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Agent maintenance mode {}ed."
                    value = "enabl"
                    result = consul.agent_maintenance(
                        consul_url=consul_url, enable=value
                    )
                    expected = {"message": msg.format(value), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to change maintenance mode for agent."
                    value = "enabl"
                    result = consul.agent_maintenance(
                        consul_url=consul_url, enable=value
                    )
                    expected = {"message": msg, "res": True}
                    self.assertEqual(expected, result)

    def test_agent_join(self):
        """
        Test consul agent join
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_join(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        # no required argument
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = 'Required parameter "address" is missing.'
                    self.assertRaises(
                        SaltInvocationError, consul.agent_join, consul_url=consul_url
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Agent joined the cluster"
                    result = consul.agent_join(consul_url=consul_url, address="test")
                    expected = {"message": msg, "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to join the cluster."
                    value = "enabl"
                    result = consul.agent_join(consul_url=consul_url, address="test")
                    expected = {"message": msg, "res": False}
                    self.assertEqual(expected, result)

    def test_agent_leave(self):
        """
        Test consul agent leave
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_join(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        node = "node1"

        # no required argument
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError, consul.agent_leave, consul_url=consul_url
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Node {} put in leave state."
                    result = consul.agent_leave(consul_url=consul_url, node=node)
                    expected = {"message": msg.format(node), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to change state for {}."
                    result = consul.agent_leave(consul_url=consul_url, node=node)
                    expected = {"message": msg.format(node), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_check_register(self):
        """
        Test consul agent check register
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_check_register(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        name = "name1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_check_register,
                        consul_url=consul_url,
                    )

                    # missing script, or http
                    msg = 'Required parameter "script" or "http" is missing.'
                    result = consul.agent_check_register(
                        consul_url=consul_url, name=name
                    )
                    expected = {"message": msg, "res": False}
                    self.assertEqual(expected, result)

                    # missing interval
                    msg = 'Required parameter "interval" is missing.'
                    result = consul.agent_check_register(
                        consul_url=consul_url,
                        name=name,
                        script="test",
                        http="test",
                        ttl="test",
                    )
                    expected = {"message": msg, "res": False}
                    self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Check {} added to agent."
                    result = consul.agent_check_register(
                        consul_url=consul_url,
                        name=name,
                        script="test",
                        http="test",
                        ttl="test",
                        interval="test",
                    )
                    expected = {"message": msg.format(name), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to add check to agent."
                    result = consul.agent_check_register(
                        consul_url=consul_url,
                        name=name,
                        script="test",
                        http="test",
                        ttl="test",
                        interval="test",
                    )
                    expected = {"message": msg.format(name), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_check_deregister(self):
        """
        Test consul agent check register
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_check_register(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        checkid = "id1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_check_deregister,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Check {} removed from agent."
                    result = consul.agent_check_deregister(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to remove check from agent."
                    result = consul.agent_check_deregister(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_check_pass(self):
        """
        Test consul agent check pass
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_check_register(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        checkid = "id1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_check_pass,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Check {} marked as passing."
                    result = consul.agent_check_pass(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to update check {}."
                    result = consul.agent_check_pass(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_check_warn(self):
        """
        Test consul agent check warn
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_check_register(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        checkid = "id1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_check_warn,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Check {} marked as warning."
                    result = consul.agent_check_warn(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to update check {}."
                    result = consul.agent_check_warn(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_check_fail(self):
        """
        Test consul agent check warn
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_check_register(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        checkid = "id1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_check_fail,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Check {} marked as critical."
                    result = consul.agent_check_fail(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to update check {}."
                    result = consul.agent_check_fail(
                        consul_url=consul_url, checkid=checkid
                    )
                    expected = {"message": msg.format(checkid), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_service_register(self):
        """
        Test consul agent service register
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_service_register(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        name = "name1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_service_register,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Service {} registered on agent."
                    result = consul.agent_service_register(
                        consul_url=consul_url,
                        name=name,
                        script="test",
                        http="test",
                        ttl="test",
                        interval="test",
                    )
                    expected = {"message": msg.format(name), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to register service {}."
                    result = consul.agent_service_register(
                        consul_url=consul_url,
                        name=name,
                        script="test",
                        http="test",
                        ttl="test",
                        interval="test",
                    )
                    expected = {"message": msg.format(name), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_service_deregister(self):
        """
        Test consul agent service deregister
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_service_deregister(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        serviceid = "sid1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_service_deregister,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Service {} removed from agent."
                    result = consul.agent_service_deregister(
                        consul_url=consul_url, serviceid=serviceid
                    )
                    expected = {"message": msg.format(serviceid), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to remove service {}."
                    result = consul.agent_service_deregister(
                        consul_url=consul_url, serviceid=serviceid
                    )
                    expected = {"message": msg.format(serviceid), "res": False}
                    self.assertEqual(expected, result)

    def test_agent_service_maintenance(self):
        """
        Test consul agent service maintenance
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.agent_service_maintenance(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        serviceid = "sid1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.agent_service_maintenance,
                        consul_url=consul_url,
                    )

                    # missing enable
                    msg = 'Required parameter "enable" is missing.'
                    result = consul.agent_service_maintenance(
                        consul_url=consul_url, serviceid=serviceid
                    )
                    expected = {"message": msg, "res": False}
                    self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Service {} set in maintenance mode."
                    result = consul.agent_service_maintenance(
                        consul_url=consul_url, serviceid=serviceid, enable=True
                    )
                    expected = {"message": msg.format(serviceid), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to set service {} to maintenance mode."
                    result = consul.agent_service_maintenance(
                        consul_url=consul_url, serviceid=serviceid, enable=True
                    )
                    expected = {"message": msg.format(serviceid), "res": False}
                    self.assertEqual(expected, result)

    def test_session_create(self):
        """
        Test consul session create
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            with patch.object(
                salt.modules.consul, "session_list", return_value=mock_result
            ):
                result = consul.session_create(consul_url="")
                expected = {"message": "No Consul URL found.", "res": False}
                self.assertEqual(expected, result)

        name = "name1"

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    self.assertRaises(
                        SaltInvocationError,
                        consul.session_create,
                        consul_url=consul_url,
                    )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Created session {}."
                    result = consul.session_create(consul_url=consul_url, name=name)
                    expected = {"message": msg.format(name), "res": True}
                    self.assertEqual(expected, result)

        with patch.object(
            salt.utils.http, "query", return_value=mock_http_result_false
        ):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                with patch.object(
                    salt.modules.consul, "session_list", return_value=mock_result
                ):
                    msg = "Unable to create session {}."
                    result = consul.session_create(consul_url=consul_url, name=name)
                    expected = {"message": msg.format(name), "res": False}
                    self.assertEqual(expected, result)

    def test_session_list(self):
        """
        Test consul session list
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            result = consul.session_list(consul_url="")
            expected = {"message": "No Consul URL found.", "res": False}
            self.assertEqual(expected, result)

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                result = consul.session_list(consul_url=consul_url)
                expected = {"data": "test", "res": True}
                self.assertEqual(expected, result)

    def test_session_destroy(self):
        """
        Test consul session destroy
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        session = "sid1"
        name = "test"

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            result = consul.session_destroy(consul_url="")
            expected = {"message": "No Consul URL found.", "res": False}
            self.assertEqual(expected, result)

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                self.assertRaises(
                    SaltInvocationError, consul.session_destroy, consul_url=consul_url,
                )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                msg = "Created Service {}."
                result = consul.session_destroy(
                    consul_url=consul_url, session=session, name="test"
                )
                expected = {"message": msg.format(name), "res": True}
                self.assertEqual(expected, result)

    def test_session_info(self):
        """
        Test consul session info
        """
        consul_url = "http://localhost:1313"
        key = "cluster/key"

        mock_result = "test"
        mock_http_result = {"status": http_client.OK, "dict": mock_result}
        mock_http_result_false = {"status": http_client.NO_CONTENT, "dict": mock_result}
        mock_url = MagicMock(return_value=consul_url)
        mock_nourl = MagicMock(return_value=None)

        session = "sid1"

        # no consul url error
        with patch.dict(consul.__salt__, {"config.get": mock_nourl}):
            result = consul.session_info(consul_url="")
            expected = {"message": "No Consul URL found.", "res": False}
            self.assertEqual(expected, result)

        # no required arguments
        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                self.assertRaises(
                    SaltInvocationError, consul.session_info, consul_url=consul_url,
                )

        with patch.object(salt.utils.http, "query", return_value=mock_http_result):
            with patch.dict(consul.__salt__, {"config.get": mock_url}):
                result = consul.session_info(consul_url=consul_url, session=session)
                expected = {"data": "test", "res": True}
                self.assertEqual(expected, result)

    def test_catalog_register(self):
        pass

    def test_catalog_deregister(self):
        pass

    def test_catalog_datacenters(self):
        pass

    def test_catalog_nodes(self):
        pass

    def test_catalog_services(self):
        pass

    def test_catalog_service(self):
        pass

    def test_catalog_node(self):
        pass

    def test_health_node(self):
        pass

    def test_health_checks(self):
        pass

    def test_health_service(self):
        pass

    def test_health_state(self):
        pass

    def test_status_leader(self):
        pass

    def test_status_peers(self):
        pass

    def test_acl_create(self):
        pass

    def test_acl_update(self):
        pass

    def test_acl_delete(self):
        pass

    def test_acl_info(self):
        pass

    def test_acl_clone(self):
        pass

    def test_acl_list(self):
        pass

    def test_event_fire(self):
        pass

    def test_event_list(self):
        pass
