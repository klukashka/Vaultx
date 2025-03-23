from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "transform"


class Transform(AsyncVaultApiBase):
    """
    Transform Secrets Engine (API).

    Reference: https://www.vaultproject.io/api-docs/secret/transform
    """

    async def create_or_update_role(
        self, name: str, transformations: list, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create or update the role with the given name.
        If a role with the name does not exist, it will be created. If the role exists, it will be
        updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/role/:name.

        :param name: the name of the role to create. This is part of the request URL.
        :param transformations: Specifies the transformations that can be used with this role.
            At least one transformation is required.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the create_or_update_role request.
        """
        params = {
            "transformations": transformations,
        }
        api_path = f"/v1/{mount_point}/role/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an existing role by the given name.

        Supported methods:
            GET: /{mount_point}/role/:name.

        :param name: the name of the role to read. This is part of the request URL.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the read_role request.
        """
        api_path = f"/v1/{mount_point}/role/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all existing roles in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/role.

        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the list_roles request.
        """
        api_path = f"/v1/{mount_point}/role"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing role by the given name.

        Supported methods:
            DELETE: /{mount_point}/role/:name.

        :param name: the name of the role to delete. This is part of the request URL.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the delete_role request.
        """
        api_path = f"/v1/{mount_point}/role/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def create_or_update_transformation(
        self,
        name: str,
        transform_type: str,
        template: str,
        tweak_source: str = "supplied",
        masking_character: str = "*",
        allowed_roles: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a transformation with the given name.
        If a transformation with the name does not exist, it will be created. If the
        transformation exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformation/:name.

        :param name: the name of the transformation to create or update. This is part of
            the request URL.
        :param transform_type: Specifies the type of transformation to perform.
            The types currently supported by this backend are fpe and masking.
            This value cannot be modified by an update operation after creation.
        :param template: the template name to use for matching value on encode and decode
            operations when using this transformation.
        :param tweak_source: Only used when the type is FPE.
        :param masking_character: the character to use for masking. If multiple characters are
            provided, only the first one is used and the rest is ignored. Only used when
            the type is masking.
        :param allowed_roles: a list of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the create_or_update_transformation request.
        """
        params = {
            "type": transform_type,
            "template": template,
            "tweak_source": tweak_source,
            "masking_character": masking_character,
        }
        params.update(
            utils.remove_nones(
                {
                    "allowed_roles": allowed_roles,
                }
            )
        )
        api_path = f"/v1/{mount_point}/transformation/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def create_or_update_fpe_transformation(
        self,
        name: str,
        template: str,
        tweak_source: str = "supplied",
        allowed_roles: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update an FPE transformation with the given name.
        If a transformation with the name does not exist, it will be created. If the transformation exists, it will be
        updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformations/fpe/:name.

        :param name: The name of the transformation to create or update. This is part of
            the request URL.
        :param template: The template name to use for matching value on encode and decode
            operations when using this transformation.
        :param tweak_source: Specifies the source of where the tweak value comes from. Valid sources are:
            supplied, generated, and internal.
        :param allowed_roles: A list of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_fpe_transformation request.
        """
        params = utils.remove_nones(
            {
                "template": template,
                "tweak_source": tweak_source,
                "allowed_roles": allowed_roles,
            }
        )
        api_path = f"/v1/{mount_point}/transformations/fpe/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def create_or_update_masking_transformation(
        self,
        name: str,
        template: str,
        masking_character: str = "*",
        allowed_roles: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a masking transformation with the given name. If a
        transformation with the name does not exist, it will be created. If the
        transformation exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformations/masking/:name.

        :param name: The name of the transformation to create or update. This is part of
            the request URL.
        :param template: The template name to use for matching value on encode and decode
            operations when using this transformation.
        :param masking_character: The character to use for masking. If multiple characters are
            provided, only the first one is used and the rest is ignored. Only used when
            the type is masking.
        :param allowed_roles: A list of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_masking_transformation request.
        """
        params = utils.remove_nones(
            {
                "template": template,
                "masking_character": masking_character,
                "allowed_roles": allowed_roles,
            }
        )
        api_path = f"/v1/{mount_point}/transformations/masking/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def create_or_update_tokenization_transformation(
        self,
        name: str,
        max_ttl: int = 0,
        mapping_mode: str = "default",
        allowed_roles: Optional[list] = None,
        stores: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint creates or updates a tokenization transformation with the given name. If a
        transformation with the name does not exist, it will be created. If the
        transformation exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/:name.

        :param name: The name of the transformation to create or update. This is part of
            the request URL.
        :param max_ttl: The maximum TTL of a token. If 0 or unspecified, tokens may have no expiration.
        :param mapping_mode: Specifies the mapping mode for stored tokenization values.

            * `default` is strongly recommended for highest security
            * `exportable` exportable allows for all plaintexts to be decoded via
                the export-decoded endpoint in an emergency.

        :param allowed_roles: aAlist of allowed roles that this transformation can be assigned to.
            A role using this transformation must exist in this list in order for
            encode and decode operations to properly function.
        :param stores: list of tokenization stores to use for tokenization state. Vault's
            internal storage is used by default.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_tokenization_transformation request.
        """
        if stores is None:
            stores = ["builtin/internal"]
        params = utils.remove_nones(
            {
                "max_ttl": max_ttl,
                "mapping_mode": mapping_mode,
                "allowed_roles": allowed_roles,
                "stores": stores,
            }
        )
        api_path = f"/v1/{mount_point}/transformations/tokenization/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_transformation(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an existing transformation by the given name.

        Supported methods:
            GET: /{mount_point}/transformation/:name.

        :param name: Specifies the name of the role to read.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the read_transformation request.
        :rtype: requests.Response
        """
        api_path = f"/v1/{mount_point}/transformation/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_transformations(self, mount_point=DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """List all existing transformations in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/transformation.

        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the list_ation request.
        :rtype: requests.Response
        """
        api_path = f"/v1/{mount_point}/transformation"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_transformation(self, name, mount_point=DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """Delete an existing transformation by the given name.

        Supported methods:
            DELETE: /{mount_point}/transformation/:name.

        :param name: the name of the transformation to delete. This is part of the
            request URL.
        :type name: str | unicode
        :param mount_point: The "path" the secrets engine was mounted on.
        :type mount_point: str | unicode
        :return: The response of the delete_ation request.
        :rtype: requests.Response
        """
        api_path = "/v1/{mount_point}/transformation/{name}".format(
            mount_point=mount_point,
            name=name,
        )
        return await self._adapter.delete(
            url=api_path,
        )

    async def create_or_update_template(
        self, name: str, template_type: str, pattern: str, alphabet: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create or update a template with the given name.
        If a template with the name does not exist, it will be created. If the
        template exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/template/:name.

        :param name: the name of the template to create.
        :param template_type: Specifies the type of pattern matching to perform.
            The only type currently supported by this backend is regex.
        :param pattern: the pattern used to match a particular value. For regex type
            matching, capture group determines the set of character that should be matched
            against. Any matches outside of capture groups are retained
            post-transformation.
        :param alphabet: the name of the alphabet to use when this template is used for FPE
            encoding and decoding operations.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the create_or_update_template request.
        """
        params = {
            "type": template_type,
            "pattern": pattern,
            "alphabet": alphabet,
        }
        api_path = f"/v1/{mount_point}/template/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_template(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an existing template by the given name.

        Supported methods:
            GET: /{mount_point}/template/:name.

        :param name: Specifies the name of the role to read.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the read_template request.
        """
        api_path = f"/v1/{mount_point}/template/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_templates(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all existing templates in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/transformation.

        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the list_template request.
        """
        api_path = f"/v1/{mount_point}/template"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_template(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing template by the given name.

        Supported methods:
            DELETE: /{mount_point}/template/:name.

        :param name: the name of the template to delete. This is part of the
            request URL.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the delete_template request.
        """
        params = {
            "name": name,
        }
        api_path = f"/v1/{mount_point}/template/{name}"
        return await self._adapter.delete(
            url=api_path,
            json=params,
        )

    async def create_or_update_alphabet(
        self, name: str, alphabet: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create or update an alphabet with the given name.
        If an alphabet with the name does not exist, it will be created. If the
        alphabet exists, it will be updated with the new attributes.

        Supported methods:
            POST: /{mount_point}/alphabet/:name.

        :param name: Specifies the name of the transformation alphabet to create.
        :param alphabet: the set of characters that can exist within the provided value
            and the encoded or decoded value for a FPE transformation.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the create_or_update_alphabet request.
        """
        params = {
            "alphabet": alphabet,
        }
        api_path = f"/v1/{mount_point}/alphabet/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_alphabet(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an existing alphabet by the given name.

        Supported methods:
            GET: /{mount_point}/alphabet/:name.

        :param name: the name of the alphabet to delete. This is part of the request URL.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the read_alphabet request.
        """
        api_path = f"/v1/{mount_point}/alphabet/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_alphabets(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all existing alphabets in the secrets engine.

        Supported methods:
            LIST: /{mount_point}/alphabet.

        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the list_alphabets request.
        """
        api_path = f"/v1/{mount_point}/alphabet"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_alphabet(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an existing alphabet by the given name.

        Supported methods:
            DELETE: /{mount_point}/alphabet/:name.

        :param name: the name of the alphabet to delete. This is part of the request URL.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the delete_alphabet request.
        """
        api_path = f"/v1/{mount_point}/alphabet/{name}"
        return await self._adapter.delete(
            url=api_path,
        )

    async def create_or_update_tokenization_store(
        self,
        name: str,
        driver: str,
        connection_string: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        _type: str = "sql",
        supported_transformations: Optional[list[str]] = None,
        schema: str = "public",
        max_open_connections: int = 4,
        max_idle_connections: int = 4,
        max_connection_lifetime: int = 0,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a storage configuration for use with tokenization.
        The database user configured here should only have permission to SELECT, INSERT, and UPDATE rows in the tables.

        Supported methods:
            POST: /{mount_point}/store/:name.

        :param name: The name of the store to create or update.
        :param _type: Specifies the type of store. Currently only `sql` is supported.
        :param driver: Specifies the database driver to use, and thus which SQL database type.
            Currently, the supported options are `postgres` or `mysql`
        :param supported_transformations: The types of transformations this store can host.
            Currently only `tokenization` is supported.
        :param connection_string: database connection string with template slots for username and password that
            Vault will use for locating and connecting to a database.  Each
            database driver type has a different syntax for its connection strings.
        :param username: username value to use when connecting to the database.
        :param password: password value to use when connecting to the database.
        :param schema: schema within the database to expect tokenization state tables.
        :param max_open_connections: maximum number of connections to the database at any given time.
        :param max_idle_connections: maximum number of idle connections to the database at any given time.
        :param max_connection_lifetime: means no limit.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_tokenization_store request.
        """
        if supported_transformations is None:
            supported_transformations = ["tokenization"]
        params = utils.remove_nones(
            {
                "type": _type,
                "driver": driver,
                "supported_transformations:": supported_transformations,
                "connection_string": connection_string,
                "username": username,
                "password": password,
                "schema": schema,
                "max_open_connections": max_open_connections,
                "max_idle_connections": max_idle_connections,
                "max_connection_lifetime": max_connection_lifetime,
            }
        )
        api_path = f"/v1/{mount_point}/store/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def encode(
        self,
        role_name: str,
        value: Optional[str] = None,
        transformation: Optional[str] = None,
        tweak: Optional[str] = None,
        batch_input: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Encode the provided value using a named role.

        Supported methods:
            POST: /{mount_point}/encode/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :param value: the value to be encoded.
        :param transformation: the transformation within the role that should be used for this
            encode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :param tweak: the tweak source.
        :param batch_input: a list of items to be encoded in a single batch. When this
            parameter is set, the 'value', 'transformation' and 'tweak' parameters are
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the encode request.
        """
        params = utils.remove_nones(
            {
                "value": value,
                "transformation": transformation,
                "tweak": tweak,
                "batch_input": batch_input,
            }
        )
        api_path = f"/v1/{mount_point}/encode/{role_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def decode(
        self,
        role_name: str,
        value: Optional[str] = None,
        transformation: Optional[str] = None,
        tweak: Optional[str] = None,
        batch_input: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Decode the provided value using a named role.

        Supported methods:
            POST: /{mount_point}/decode/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :param value: the value to be decoded.
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :param tweak: the tweak source.
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value', 'transformation' and 'tweak' parameters are
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :param mount_point: The "path" the secrets engine was mounted on.
        :return: The response of the decode request.
        """
        params = utils.remove_nones(
            {
                "value": value,
                "transformation": transformation,
                "tweak": tweak,
                "batch_input": batch_input,
            }
        )
        api_path = f"/v1/{mount_point}/decode/{role_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def validate_token(
        self,
        role_name: str,
        value: str,
        transformation: str,
        batch_input: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Determine if a provided tokenized value is valid and unexpired.
        Only valid for tokenization transformations.

        Supported methods:
            POST: /{mount_point}/validate/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :param value: the token for which to check validity.
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value' parameter is
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the validate_token request.
        """
        params = utils.remove_nones(
            {
                "value": value,
                "transformation": transformation,
                "batch_input": batch_input,
            }
        )
        api_path = f"/v1/{mount_point}/validate/{role_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def check_tokenization(
        self,
        role_name: str,
        value: str,
        transformation: str,
        batch_input: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Determine if a provided plaintext value has an valid, unexpired tokenized value.
        Note that this cannot return await the token, just confirm that a
        tokenized value exists. This endpoint is only valid for tokenization
        transformations.

        Supported methods:
            POST: /{mount_point}/tokenized/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :param value: the token to test for whether it has a valid tokenization.
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value' parameter is
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the check_tokenization request.
        """
        params = utils.remove_nones(
            {
                "value": value,
                "transformation": transformation,
                "batch_input": batch_input,
            }
        )
        api_path = f"/v1/{mount_point}/tokenized/{role_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def retrieve_token_metadata(
        self,
        role_name: str,
        value: str,
        transformation: str,
        batch_input: Optional[list] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        This endpoint retrieves metadata for a tokenized value using a named role.
        Only valid for tokenization transformations.

        Supported methods:
            POST: /{mount_point}/metadata/:role_name.

        :param role_name: the role name to use for this operation. This is specified as part
            of the URL.
        :param value: the token for which to retrieve metadata.
        :param transformation: the transformation within the role that should be used for this
            decode operation. If a single transformation exists for role, this parameter
            may be skipped and will be inferred. If multiple transformations exist, one
            must be specified.
        :param batch_input: a list of items to be decoded in a single batch. When this
            parameter is set, the 'value' parameter is
            ignored. Instead, the aforementioned parameters should be provided within
            each object in the list.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the retrieve_token_metadata request.
        """
        params = utils.remove_nones(
            {
                "value": value,
                "transformation": transformation,
                "batch_input": batch_input,
            }
        )
        api_path = f"/v1/{mount_point}/metadata/{role_name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def snapshot_tokenization_state(
        self, name: str, limit: int = 1000, continuation: str = "", mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        This endpoint starts or continues retrieving a snapshot of the stored
        state of a tokenization transform.  This state is protected as it is
        in the underlying store, and so is safe for storage or transport.  Snapshots
        may be used for backup purposes or to migrate from one store to another.
        If more than one store is configured for a tokenization transform, the
        snapshot data contains the contents of the first store.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/snapshot/:name.

        :param name: the name of the transformation to snapshot.
        :param limit: maximum number of tokenized value states to return await on this call.
        :param continuation: absent or empty, a new snapshot is started.  If present, the
            snapshot should continue at the next available value.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the snapshot_tokenization_state request.
        """
        params = utils.remove_nones(
            {
                "limit": limit,
                "continuation": continuation,
            }
        )
        api_path = f"/v1/{mount_point}/transformations/tokenization/snapshot/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def restore_tokenization_state(
        self, name: str, values: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        This endpoint restores previously snapshotted tokenization state values
        to the underlying store(s) of a tokenization transform.  Calls to this
        endpoint are idempotent, so multiple outputs from a snapshot run can
        be applied via restore in any order and duplicates will not cause a problem.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/restore/:name.

        :param name: the name of the transformation to restore.
        :param values: number of tokenization state values from a previous snapshot call.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the restore_tokenization_state request.
        """
        params = {
            "values": values,
        }
        api_path = f"/v1/{mount_point}/transformations/tokenization/restore/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def export_decoded_tokenization_state(
        self, name: str, limit: int = 1000, continuation: str = "", mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Start or continue retrieving an export of tokenization state, including the tokens and their decoded values.
        This call is only supported on tokenization stores configured with the exportable mapping mode.
        Refer to the Tokenization documentation for when to use the exportable mapping mode.
        Decoded values are in Base64 representation.

        Supported methods:
            POST: /{mount_point}/transformations/tokenization/export-decoded/:name.

        :param name: the name of the transformation to export.
        :param limit: maximum number of tokenized value states to return await on this call.
        :param continuation: absent or empty, a new export is started.  If present, the
            export should continue at the next available value.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the export_decoded_tokenization_state request.
        """
        params = utils.remove_nones(
            {
                "limit": limit,
                "continuation": continuation,
            }
        )
        api_path = f"/v1/{mount_point}/transformations/tokenization/export-decoded/{name}"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def rotate_tokenization_key(
        self, transform_name: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Rotate the version of the named key.
        After rotation, new requests will be encoded with the new version of the key.

        Supported methods:
            POST: /{mount_point}/tokenization/keys/{transform_name}/rotate.

        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the rotate_tokenization_key request.
        """
        api_path = f"/v1/{mount_point}/tokenization/keys/{transform_name}/rotate"
        return await self._adapter.post(
            url=api_path,
        )

    async def update_tokenization_key_config(
        self, transform_name: str, min_decryption_version: int, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Allow the minimum key version to be set for decode operations.
        Only valid for tokenization transformations.

        Supported methods:
            POST: /{mount_point}/tokenization/keys/{transform_name}/config.

        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :param min_decryption_version: the minimum key version that vault can use to decode values for the
            corresponding transform.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the update_tokenization_key_config request.
        """
        params = {
            "transform_name": transform_name,
            "min_decryption_version": min_decryption_version,
        }
        api_path = f"/v1/{mount_point}/tokenization/keys/{transform_name}/config"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def list_tokenization_key_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all tokenization keys.
        Only valid for tokenization transformations.

        Supported methods:
            LIST: /{mount_point}/tokenization/keys/.

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the list_tokenization_key_configuration request.
        """
        api_path = f"/v1/{mount_point}/tokenization/keys/"
        return await self._adapter.list(
            url=api_path,
        )

    async def read_tokenization_key_configuration(
        self, transform_name: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Read tokenization key configuration for a particular transform.
        Only valid for tokenization transformations.

        Supported methods:
            GET: /{mount_point}/tokenization/keys/:{mount_point}_name.

        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the read_tokenization_key_configuration request.
        """
        api_path = f"/v1/{mount_point}/tokenization/keys/{transform_name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def trim_tokenization_key_version(
        self, transform_name: str, min_available_version: int, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Trim older key versions setting a minimum version for the keyring.
        Once trimmed, previous versions of the key cannot be recovered.

        Supported methods:
            POST: /{mount_point}/tokenization/keys/{transform_name}/trim.

        :param transform_name: the transform name to use for this operation. This is specified as part
            of the URL.
        :param min_available_version:
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the trim_tokenization_key_version request.
        """
        params = {
            "min_available_version": min_available_version,
        }
        api_path = f"/v1/{mount_point}/tokenization/keys/{transform_name}/trim"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )
