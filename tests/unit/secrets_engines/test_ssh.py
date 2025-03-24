import unittest
from unittest import mock

from httpx import Response

from vaultx.api.async_secrets_engines.ssh import Ssh as AsyncSsh
from vaultx.api.secrets_engines.ssh import Ssh


class TestSsh(unittest.TestCase):
    def setUp(self):
        self.mock_adapter = mock.Mock()
        self.ssh = Ssh(self.mock_adapter)

    def test_create_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.create_role(
            name="test-role",
            key="test-key",
            admin_user="admin",
            default_user="user",
            cidr_list="192.168.1.0/24",
            exclude_cidr_list="192.168.1.1/32",
            port=22,
            key_type="rsa",
            key_bits=2048,
            install_script="install.sh",
            allowed_users="user1,user2",
            allowed_users_template="false",
            allowed_domains="example.com",
            key_option_specs="option1,option2",
            ttl="1h",
            max_ttl="2h",
            allowed_critical_options="option1,option2",
            allowed_extensions="ext1,ext2",
            default_critical_options={"option1": "value1"},
            default_extensions={"ext1": "value1"},
            allow_user_certificates="true",
            allow_host_certificates=True,
            allow_bare_domains=True,
            allow_subdomains=True,
            allow_user_key_ids=True,
            key_id_format="test-format",
            allowed_user_key_lengths={"rsa": 2048},
            algorithm_signer="rsa-sha2-256",
        )
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/roles/test-role",
            json={
                "key": "test-key",
                "admin_user": "admin",
                "default_user": "user",
                "cidr_list": "192.168.1.0/24",
                "exclude_cidr_list": "192.168.1.1/32",
                "port": 22,
                "key_type": "rsa",
                "key_bits": 2048,
                "install_script": "install.sh",
                "allowed_users": "user1,user2",
                "allowed_users_template": "false",
                "allowed_domains": "example.com",
                "key_option_specs": "option1,option2",
                "ttl": "1h",
                "max_ttl": "2h",
                "allowed_critical_options": "option1,option2",
                "allowed_extensions": "ext1,ext2",
                "default_critical_options": {"option1": "value1"},
                "default_extensions": {"ext1": "value1"},
                "allow_user_certificates": "true",
                "allow_host_certificates": True,
                "allow_bare_domains": True,
                "allow_subdomains": True,
                "allow_user_key_ids": True,
                "key_id_format": "test-format",
                "allowed_user_key_lengths": {"rsa": 2048},
                "algorithm_signer": "rsa-sha2-256",
            },
        )

    def test_read_role(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ssh.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ssh/roles/test-role",
        )

    def test_list_roles(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = self.ssh.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/ssh/roles",
        )

    def test_delete_role(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.ssh.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ssh/roles/test-role",
        )

    def test_list_zeroaddress_roles(self):
        mock_response = Response(200, json={"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ssh.list_zeroaddress_roles()
        self.assertEqual(result.json(), {"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ssh/config/zeroaddress",
        )

    def test_configure_zeroaddress_roles(self):
        mock_response = Response(200, json={"data": {"message": "Zero-address roles configured"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.configure_zeroaddress_roles(roles="role1,role2")
        self.assertEqual(result.json(), {"data": {"message": "Zero-address roles configured"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/config/zeroaddress",
            json={"roles": "role1,role2"},
        )

    def test_delete_zeroaddress_role(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.ssh.delete_zeroaddress_role()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ssh/config/zeroaddress",
        )

    def test_generate_ssh_credentials(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "ip": "192.168.1.1"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.generate_ssh_credentials(name="test-role", username="test-user", ip="192.168.1.1")
        self.assertEqual(result.json(), {"data": {"username": "test-user", "ip": "192.168.1.1"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/creds/test-role",
            json={"username": "test-user", "ip": "192.168.1.1"},
        )

    def test_list_roles_by_ip(self):
        mock_response = Response(200, json={"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.list_roles_by_ip(ip="192.168.1.1")
        self.assertEqual(result.json(), {"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/lookup",
            json={"ip": "192.168.1.1"},
        )

    def test_verify_ssh_otp(self):
        mock_response = Response(200, json={"data": {"valid": True}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.verify_ssh_otp(otp="123456")
        self.assertEqual(result.json(), {"data": {"valid": True}})
        self.mock_adapter.post.assert_called_once_with(
            url="v1/ssh/verify",
            json={"otp": "123456"},
        )

    def test_submit_ca_information(self):
        mock_response = Response(200, json={"data": {"message": "CA information submitted"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.submit_ca_information(
            private_key="-----BEGIN PRIVATE KEY-----",
            public_key="-----BEGIN PUBLIC KEY-----",
            generate_signing_key=True,
            key_type="ssh-rsa",
            key_bits=2048,
        )
        self.assertEqual(result.json(), {"data": {"message": "CA information submitted"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/config/ca",
            json={
                "private_key": "-----BEGIN PRIVATE KEY-----",
                "public_key": "-----BEGIN PUBLIC KEY-----",
                "generate_signing_key": True,
                "key_type": "ssh-rsa",
                "key_bits": 2048,
            },
        )

    def test_delete_ca_information(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = self.ssh.delete_ca_information()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ssh/config/ca",
        )

    def test_read_public_key(self):
        mock_response = Response(200, json={"data": {"public_key": "-----BEGIN PUBLIC KEY-----"}})
        self.mock_adapter.get.return_value = mock_response

        result = self.ssh.read_public_key()
        self.assertEqual(result.json(), {"data": {"public_key": "-----BEGIN PUBLIC KEY-----"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ssh/config/ca",
        )

    def test_sign_ssh_key(self):
        mock_response = Response(200, json={"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.return_value = mock_response

        result = self.ssh.sign_ssh_key(
            name="test-role",
            public_key="-----BEGIN PUBLIC KEY-----",
            ttl="1h",
            valid_principals="user1,user2",
            cert_type="user",
            key_id="test-key-id",
            critical_options={"option1": "value1"},
            extensions={"ext1": "value1"},
        )
        self.assertEqual(result.json(), {"data": {"certificate": "-----BEGIN CERTIFICATE-----"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/sign/test-role",
            json={
                "public_key": "-----BEGIN PUBLIC KEY-----",
                "ttl": "1h",
                "valid_principals": "user1,user2",
                "cert_type": "user",
                "key_id": "test-key-id",
                "critical_options": {"option1": "value1"},
                "extensions": {"ext1": "value1"},
            },
        )


class TestAsyncSsh(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.mock_adapter = mock.AsyncMock()
        self.ssh = AsyncSsh(self.mock_adapter)

    async def test_create_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.ssh.create_role(
            name="test-role",
            key="test-key",
            admin_user="admin",
            default_user="user",
            cidr_list="192.168.1.0/24",
            exclude_cidr_list="192.168.1.1/32",
            port=22,
            key_type="rsa",
            key_bits=2048,
            install_script="install.sh",
            allowed_users="user1,user2",
            allowed_users_template="false",
            allowed_domains="example.com",
            key_option_specs="option1,option2",
            ttl="1h",
            max_ttl="2h",
            allowed_critical_options="option1,option2",
            allowed_extensions="ext1,ext2",
            default_critical_options={"option1": "value1"},
            default_extensions={"ext1": "value1"},
            allow_user_certificates="true",
            allow_host_certificates=True,
            allow_bare_domains=True,
            allow_subdomains=True,
            allow_user_key_ids=True,
            key_id_format="test-format",
            allowed_user_key_lengths={"rsa": 2048},
            algorithm_signer="rsa-sha2-256",
        )
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/roles/test-role",
            json={
                "key": "test-key",
                "admin_user": "admin",
                "default_user": "user",
                "cidr_list": "192.168.1.0/24",
                "exclude_cidr_list": "192.168.1.1/32",
                "port": 22,
                "key_type": "rsa",
                "key_bits": 2048,
                "install_script": "install.sh",
                "allowed_users": "user1,user2",
                "allowed_users_template": "false",
                "allowed_domains": "example.com",
                "key_option_specs": "option1,option2",
                "ttl": "1h",
                "max_ttl": "2h",
                "allowed_critical_options": "option1,option2",
                "allowed_extensions": "ext1,ext2",
                "default_critical_options": {"option1": "value1"},
                "default_extensions": {"ext1": "value1"},
                "allow_user_certificates": "true",
                "allow_host_certificates": True,
                "allow_bare_domains": True,
                "allow_subdomains": True,
                "allow_user_key_ids": True,
                "key_id_format": "test-format",
                "allowed_user_key_lengths": {"rsa": 2048},
                "algorithm_signer": "rsa-sha2-256",
            },
        )

    async def test_read_role_async(self):
        mock_response = Response(200, json={"data": {"name": "test-role"}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ssh.read_role(name="test-role")
        self.assertEqual(result.json(), {"data": {"name": "test-role"}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ssh/roles/test-role",
        )

    async def test_list_roles_async(self):
        mock_response = Response(200, json={"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.return_value = mock_response

        result = await self.ssh.list_roles()
        self.assertEqual(result.json(), {"data": {"keys": ["role1", "role2"]}})
        self.mock_adapter.list.assert_called_once_with(
            url="/v1/ssh/roles",
        )

    async def test_delete_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.ssh.delete_role(name="test-role")
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ssh/roles/test-role",
        )

    async def test_list_zeroaddress_roles_async(self):
        mock_response = Response(200, json={"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.get.return_value = mock_response

        result = await self.ssh.list_zeroaddress_roles()
        self.assertEqual(result.json(), {"data": {"roles": ["role1", "role2"]}})
        self.mock_adapter.get.assert_called_once_with(
            url="/v1/ssh/config/zeroaddress",
        )

    async def test_configure_zeroaddress_roles_async(self):
        mock_response = Response(200, json={"data": {"message": "Zero-address roles configured"}})
        self.mock_adapter.post.return_value = mock_response

        result = await self.ssh.configure_zeroaddress_roles(roles="role1,role2")
        self.assertEqual(result.json(), {"data": {"message": "Zero-address roles configured"}})
        self.mock_adapter.post.assert_called_once_with(
            url="/v1/ssh/config/zeroaddress",
            json={"roles": "role1,role2"},
        )

    async def test_delete_zeroaddress_role_async(self):
        mock_response = Response(204)
        self.mock_adapter.delete.return_value = mock_response

        result = await self.ssh.delete_zeroaddress_role()
        self.assertEqual(result.status_code, 204)
        self.mock_adapter.delete.assert_called_once_with(
            url="/v1/ssh/config/zeroaddress",
        )

    async def test_generate_ssh_credentials_async(self):
        mock_response = Response(200, json={"data": {"username": "test-user", "ip": "192.168.1.1"}})
        self.mock_adapter.post.return_value = mock_response
