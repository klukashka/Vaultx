import logging
from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.constants.identity import ALLOWED_GROUP_TYPES, DEFAULT_MOUNT_POINT
from vaultx.exceptions import VaultxError


logger = logging.getLogger(__name__)


class Identity(VaultApiBase):
    """
    Identity Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/identity/entity.html
    """

    def create_or_update_entity(
        self,
        name: str,
        entity_id: Optional[str] = None,
        metadata: Optional[dict] = None,
        policies: Optional[str] = None,
        disabled: Optional[bool] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update an Entity.

        Supported methods:
            POST: /{mount_point}/entity. Produces: 200 application/json

        :param entity_id: ID of the entity. If set, updates the corresponding existing entity.
        :param name: Name of the entity.
        :param metadata: Metadata to be associated with the entity.
        :param policies: Policies to be tied to the entity.
        :param disabled: Whether the entity is disabled. Disabled entities' associated tokens cannot be used, but are
            not revoked.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse for creates, the generic response object for updates, of the request.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )

        params = utils.remove_nones(
            {
                "id": entity_id,
                "name": name,
                "metadata": metadata,
                "policies": policies,
                "disabled": disabled,
            }
        )
        api_path = f"/v1/{mount_point}/entity"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def create_or_update_entity_by_name(
        self,
        name: str,
        metadata: Optional[dict] = None,
        policies: Optional[str] = None,
        disabled: Optional[bool] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update an entity by a given name.

        Supported methods:
            POST: /{mount_point}/entity/name/{name}. Produces: 200 application/json

        :param name: Name of the entity.
        :param metadata: Metadata to be associated with the entity.
        :param policies: Policies to be tied to the entity.
        :param disabled: Whether the entity is disabled. Disabled
            entities' associated tokens cannot be used, but are not revoked.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse for creates, the generic response of the request for updates.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )

        params = utils.remove_nones(
            {
                "metadata": metadata,
                "policies": policies,
                "disabled": disabled,
            }
        )
        api_path = f"/v1/{mount_point}/entity/name/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_entity(self, entity_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an entity by its identifier.

        Supported methods:
            GET: /auth/{mount_point}/entity/id/{id}. Produces: 200 application/json

        :param entity_id: Identifier of the entity.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/entity/id/{entity_id}"
        return self._adapter.get(url=api_path)

    def read_entity_by_name(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query an entity by its name.

        Supported methods:
            GET: /{mount_point}/entity/name/{name}. Produces: 200 application/json

        :param name: Name of the entity.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/entity/name/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def update_entity(
        self,
        entity_id: str,
        name: Optional[str] = None,
        metadata: Optional[dict] = None,
        policies: Optional[str] = None,
        disabled: Optional[bool] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Update an existing entity.

        Supported methods:
            POST: /{mount_point}/entity/id/{id}. Produces: 200 application/json

        :param entity_id: Identifier of the entity.
        :param name: Name of the entity.
        :param metadata: Metadata to be associated with the entity.
        :param policies: Policies to be tied to the entity.
        :param disabled: Whether the entity is disabled. Disabled entities' associated tokens cannot be used, but
            are not revoked.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse where available, otherwise the generic response object, of the request.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )

        params = utils.remove_nones(
            {
                "name": name,
                "metadata": metadata,
                "policies": policies,
                "disabled": disabled,
            }
        )
        api_path = f"/v1/{mount_point}/entity/id/{entity_id}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def delete_entity(self, entity_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an entity and all its associated aliases.

        Supported methods:
            DELETE: /{mount_point}/entity/id/:id. Produces: 204 (empty body)

        :param entity_id: Identifier of the entity.
        :param mount_point: The "path" the secret engine was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/entity/id/{entity_id}"
        return self._adapter.delete(
            url=api_path,
        )

    def delete_entity_by_name(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an entity and all its associated aliases, given the entity name.

        Supported methods:
            DELETE: /{mount_point}/entity/name/{name}. Produces: 204 (empty body)

        :param name: Name of the entity.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/entity/name/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_entities(self, method: str = "LIST", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List available entities by their identifiers.

        :param method: Supported methods:
            LIST: /{mount_point}/entity/id. Produces: 200 application/json
            GET: /{mount_point}/entity/id?list=true. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if method == "LIST":
            api_path = f"/v1/{mount_point}/entity/id"
            response = self._adapter.list(
                url=api_path,
            )

        elif method == "GET":
            api_path = f"/v1/{mount_point}/entity/id?list=true"
            response = self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; LIST or GET allowed, "{method}" provided')
        return response

    def list_entities_by_name(self, method: str = "LIST", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List available entities by their names.

        :param method: Supported methods:
            LIST: /{mount_point}/entity/name. Produces: 200 application/json
            GET: /{mount_point}/entity/name?list=true. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if method == "LIST":
            api_path = f"/v1/{mount_point}/entity/name"
            response = self._adapter.list(
                url=api_path,
            )

        elif method == "GET":
            api_path = f"/v1/{mount_point}/entity/name?list=true"
            response = self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; LIST or GET allowed, "{method}" provided')
        return response

    def merge_entities(
        self,
        from_entity_ids: list[str],
        to_entity_id: str,
        force: Optional[bool] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        conflicting_alias_ids_to_keep: Optional[list[str]] = None,
    ) -> VaultxResponse:
        """
        Merge many entities into one entity.

        Supported methods:
            POST: /{mount_point}/entity/merge. Produces: 204 (empty body)

        :param from_entity_ids: Entity IDs which needs to get merged.
        :param to_entity_id: Entity ID into which all the other entities need to get merged.
        :param force: Setting this will follow the 'mine' strategy for merging MFA secrets. If there are secrets of the
            same type both in entities that are merged from and in entity into which all others are getting merged,
            secrets in the destination will be unaltered. If not set, this API will throw an error containing all the
            conflicts.
        :param mount_point: The "path" the method/backend was mounted on.
        :param conflicting_alias_ids_to_keep: A list of entity aliases to keep in the case where the to-Entity and
            from-Entity have aliases with the same mount accessor. In the case where alias share mount accessors, the
            alias ID given in this list will be kept or merged, and the other alias will be deleted. Note that merges
            requiring this parameter must have only one from-Entity.
            Requires Vault 1.12 or higher
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "from_entity_ids": from_entity_ids,
                "to_entity_id": to_entity_id,
                "force": force,
                "conflicting_alias_ids_to_keep": conflicting_alias_ids_to_keep,
            }
        )
        api_path = f"/v1/{mount_point}/entity/merge"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def create_or_update_entity_alias(
        self,
        name: str,
        canonical_id: str,
        mount_accessor: str,
        alias_id: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create a new alias for an entity.

        Supported methods:
            POST: /{mount_point}/entity-alias. Produces: 200 application/json

        :param name: Name of the alias. Name should be the identifier of the client in the authentication source. For
            example, if the alias belongs to userpass backend, the name should be a valid username within userpass
            backend. If alias belongs to GitHub, it should be the GitHub username.
        :param alias_id: ID of the entity alias. If set, updates the  corresponding entity alias.
        :param canonical_id: Entity ID to which this alias belongs to.
        :param mount_accessor: Accessor of the mount to which the alias should belong to.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = utils.remove_nones(
            {
                "id": alias_id,
                "name": name,
                "canonical_id": canonical_id,
                "mount_accessor": mount_accessor,
            }
        )
        api_path = f"/v1/{mount_point}/entity-alias"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_entity_alias(self, alias_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query the entity alias by its identifier.

        Supported methods:
            GET: /{mount_point}/entity-alias/id/{id}. Produces: 200 application/json

        :param alias_id: Identifier of entity alias.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/entity-alias/id/{alias_id}"
        return self._adapter.get(
            url=api_path,
        )

    def update_entity_alias(
        self,
        alias_id: str,
        name: str,
        canonical_id: str,
        mount_accessor: str,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Update an existing entity alias.

        Supported methods:
            POST: /{mount_point}/entity-alias/id/{id}. Produces: 200 application/json

        :param alias_id: Identifier of the entity alias.
        :param name: Name of the alias. Name should be the identifier of the client in the authentication source. For
            example, if the alias belongs to userpass backend, the name should be a valid username within userpass
            backend. If alias belongs to GitHub, it should be the GitHub username.
        :param canonical_id: Entity ID to which this alias belongs to.
        :param mount_accessor: Accessor of the mount to which the alias should belong to.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse where available, otherwise the generic response object, of the request.
        """
        params = utils.remove_nones(
            {
                "name": name,
                "canonical_id": canonical_id,
                "mount_accessor": mount_accessor,
            }
        )
        api_path = f"/v1/{mount_point}/entity-alias/id/{alias_id}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def list_entity_aliases(self, method: str = "LIST", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List available entity aliases by their identifiers.

        :param method: Supported methods:
            LIST: /{mount_point}/entity-alias/id. Produces: 200 application/json
            GET: /{mount_point}/entity-alias/id?list=true. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """

        if method == "LIST":
            api_path = f"/v1/{mount_point}/entity-alias/id"
            response = self._adapter.list(
                url=api_path,
            )

        elif method == "GET":
            api_path = f"/v1/{mount_point}/entity-alias/id?list=true"
            response = self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; LIST or GET allowed, "{method}" provided')
        return response

    def delete_entity_alias(self, alias_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete an entity alias.

        Supported methods:
            DELETE: /{mount_point}/entity-alias/id/{alias_id}. Produces: 204 (empty body)

        :param alias_id: Identifier of the entity.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/entity-alias/id/{alias_id}"
        return self._adapter.delete(
            url=api_path,
        )

    @staticmethod
    def validate_member_id_params_for_group_type(
        group_type: str, params: dict, member_group_ids: Optional[str], member_entity_ids: Optional[str]
    ) -> dict:
        """
        Determine whether member ID parameters can be sent with a group create / update request.
        These parameters are only allowed for the internal group type. If they're set for an external group type, Vault
        returns an "error" response.

        :param group_type: Type of the group, internal or external
        :param params: Params dict to conditionally add the member entity/group ID's to.
        :param member_group_ids:  Group IDs to be assigned as group members.
        :param member_entity_ids: Entity IDs to be assigned as  group members.
        :return: Params dict with conditionally added member entity/group ID's.
        """
        if group_type == "external":
            if member_entity_ids is not None:
                logger.warning(
                    "InvalidRequest: member entities can't be set manually "
                    "for external groups ignoring member_entity_ids argument."
                )
        else:
            params["member_entity_ids"] = member_entity_ids

        if group_type == "external":
            if member_group_ids is not None:
                logger.warning(
                    "InvalidRequest: member groups can't be set for external groups; "
                    "ignoring member_group_ids argument."
                )
        else:
            params["member_group_ids"] = member_group_ids

        return params

    def create_or_update_group(
        self,
        name: str,
        group_id: Optional[str] = None,
        group_type: str = "internal",
        metadata: Optional[dict] = None,
        policies: Optional[str] = None,
        member_group_ids: Optional[str] = None,
        member_entity_ids: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a Group.

        Supported methods:
            POST: /{mount_point}/group. Produces: 200 application/json

        :param name: Name of the group.
        :param group_id: ID of the group. If set, updates the corresponding existing group.
        :param group_type: Type of the group, internal or external. Defaults to internal.
        :param metadata: Metadata to be associated with the group.
        :param policies: Policies to be tied to the group.
        :param member_group_ids:  Group IDs to be assigned as group members.
        :param member_entity_ids: Entity IDs to be assigned as  group members.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse where available, otherwise the generic response object, of the request.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )
        if group_type not in ALLOWED_GROUP_TYPES:
            raise VaultxError(
                f'unsupported group_type argument provided "{group_type}", allowed values: ({ALLOWED_GROUP_TYPES})'
            )
        params = utils.remove_nones(
            {
                "id": group_id,
                "name": name,
                "type": group_type,
                "metadata": metadata,
                "policies": policies,
            }
        )

        Identity.validate_member_id_params_for_group_type(
            group_type=group_type,
            params=params,
            member_group_ids=member_group_ids,
            member_entity_ids=member_entity_ids,
        )

        api_path = f"/v1/{mount_point}/group"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_group(self, group_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query the group by its identifier.

        Supported methods:
            GET: /{mount_point}/group/id/{id}. Produces: 200 application/json

        :param group_id: Identifier of the group.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/group/id/{group_id}"
        return self._adapter.get(
            url=api_path,
        )

    def update_group(
        self,
        group_id: str,
        name: str,
        group_type: str = "internal",
        metadata: Optional[dict] = None,
        policies: Optional[str] = None,
        member_group_ids: Optional[str] = None,
        member_entity_ids: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Update an existing group.

        Supported methods:
            POST: /{mount_point}/group/id/{id}. Produces: 200 application/json

        :param group_id: Identifier of the entity.
        :param name: Name of the group.
        :param group_type: Type of the group, internal or external. Defaults to internal.
        :param metadata: Metadata to be associated with the group.
        :param policies: Policies to be tied to the group.
        :param member_group_ids:  Group IDs to be assigned as group members.
        :param member_entity_ids: Entity IDs to be assigned as group members.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse where available, otherwise the generic response object, of the request.
        """
        if metadata is not None and not isinstance(metadata, dict):
            raise VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )
        if group_type not in ALLOWED_GROUP_TYPES:
            raise VaultxError(
                f'unsupported group_type argument provided "{group_type}", allowed values: ({ALLOWED_GROUP_TYPES})'
            )
        params = utils.remove_nones(
            {
                "name": name,
                "type": group_type,
                "metadata": metadata,
                "policies": policies,
            }
        )

        Identity.validate_member_id_params_for_group_type(
            group_type=group_type,
            params=params,
            member_group_ids=member_group_ids,
            member_entity_ids=member_entity_ids,
        )

        api_path = f"/v1/{mount_point}/group/id/{group_id}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def delete_group(self, group_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a group.

        Supported methods:
            DELETE: /{mount_point}/group/id/{id}. Produces: 204 (empty body)

        :param group_id: Identifier of the entity.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/group/id/{group_id}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_groups(self, method: str = "LIST", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List available groups by their identifiers.

        :param method: Supported methods:
            LIST: /{mount_point}/group/id. Produces: 200 application/json
            GET: /{mount_point}/group/id?list=true. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """

        if method == "LIST":
            api_path = f"/v1/{mount_point}/group/id"
            response = self._adapter.list(
                url=api_path,
            )

        elif method == "GET":
            api_path = f"/v1/{mount_point}/group/id?list=true"
            response = self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; LIST or GET allowed, "{method}" provided')

        return response

    def list_groups_by_name(self, method: str = "LIST", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List available groups by their names.

        :param method: Supported methods:
            LIST: /{mount_point}/group/name. Produces: 200 application/json
            GET: /{mount_point}/group/name?list=true. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """

        if method == "LIST":
            api_path = f"/v1/{mount_point}/group/name"
            response = self._adapter.list(
                url=api_path,
            )

        elif method == "GET":
            api_path = f"/v1/{mount_point}/group/name?list=true"
            response = self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; LIST or GET allowed, "{method}" provided')

        return response

    def create_or_update_group_by_name(
        self,
        name: str,
        group_type: str = "internal",
        metadata: Optional[dict] = None,
        policies: Optional[str] = None,
        member_group_ids: Optional[str] = None,
        member_entity_ids: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a group by its name.

        Supported methods:
            POST: /{mount_point}/group/name/{name}. Produces: 200 application/json

        :param name: Name of the group.
        :param group_type: Type of the group, internal or external. Defaults to internal.
        :param metadata: Metadata to be associated with the group.
        :param policies: Policies to be tied to the group.
        :param member_group_ids: Group IDs to be assigned as group members.
        :param member_entity_ids: Entity IDs to be assigned as group members.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """

        if metadata is not None and not isinstance(metadata, dict):
            raise VaultxError(
                f'unsupported metadata argument provided "{metadata}" ({type(metadata)}), required type: dict"'
            )
        if group_type not in ALLOWED_GROUP_TYPES:
            raise VaultxError(
                f'unsupported group_type argument provided "{group_type}", allowed values: ({ALLOWED_GROUP_TYPES})'
            )
        params = utils.remove_nones(
            {
                "type": group_type,
                "metadata": metadata,
                "policies": policies,
            }
        )
        if group_type != "external":
            external_only_params = utils.remove_nones(
                {
                    "member_group_ids": member_group_ids,
                    "member_entity_ids": member_entity_ids,
                }
            )
            params.update(external_only_params)
        api_path = f"/v1/{mount_point}/group/name/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_group_by_name(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query a group by its name.

        Supported methods:
            GET: /{mount_point}/group/name/{name}. Produces: 200 application/json

        :param name: Name of the group.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/group/name/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def delete_group_by_name(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a group, given its name.

        Supported methods:
            DELETE: /{mount_point}/group/name/{name}. Produces: 204 (empty body)

        :param name: Name of the group.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/group/name/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def create_or_update_group_alias(
        self,
        name: str,
        alias_id: Optional[str] = None,
        mount_accessor: Optional[str] = None,
        canonical_id: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a group alias.

        Supported methods:
            POST: /{mount_point}/group-alias. Produces: 200 application/json

        :param alias_id: ID of the group alias. If set, updates the corresponding existing group alias.
        :param name: Name of the group alias.
        :param mount_accessor: Mount accessor to which this alias belongs to
        :param canonical_id: ID of the group to which this is an alias.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = utils.remove_nones(
            {
                "id": alias_id,
                "name": name,
                "mount_accessor": mount_accessor,
                "canonical_id": canonical_id,
            }
        )
        api_path = f"/v1/{mount_point}/group-alias"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def update_group_alias(
        self,
        entity_id: str,
        name: str,
        mount_accessor: Optional[str] = None,
        canonical_id: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Update an existing group alias.

        Supported methods:
            POST: /{mount_point}/group-alias/id/{id}. Produces: 200 application/json

        :param entity_id: ID of the group alias.
        :param name: Name of the group alias.
        :param mount_accessor: Mount accessor to which this alias belongs
            toMount accessor to which this alias belongs to.
        :param canonical_id: ID of the group to which this is an alias.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "name": name,
                "mount_accessor": mount_accessor,
                "canonical_id": canonical_id,
            }
        )
        api_path = f"/v1/{mount_point}/group-alias/id/{entity_id}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_group_alias(self, alias_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query the group alias by its identifier.

        Supported methods:
            GET: /{mount_point}/group-alias/id/:id. Produces: 200 application/json

        :param alias_id: ID of the group alias.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/group-alias/id/{alias_id}"
        return self._adapter.get(
            url=api_path,
        )

    def delete_group_alias(self, entity_id: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a group alias.

        Supported methods:
            DELETE: /{mount_point}/group-alias/id/{id}. Produces: 204 (empty body)

        :param entity_id: ID of the group alias.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/{mount_point}/group-alias/id/{entity_id}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_group_aliases(self, method: str = "LIST", mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List available group aliases by their identifiers.

        :param method: Supported methods:
            LIST: /{mount_point}/group-alias/id. Produces: 200 application/json
            GET: /{mount_point}/group-alias/id?list=true. Produces: 200 application/json
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The "data" key from the VaultxResponse of the request.
        """

        if method == "LIST":
            api_path = f"/v1/{mount_point}/group-alias/id"
            response = self._adapter.list(
                url=api_path,
            )
        elif method == "GET":
            api_path = f"/v1/{mount_point}/group-alias/id?list=true"
            response = self._adapter.get(
                url=api_path,
            )
        else:
            raise VaultxError(f'"method" parameter provided invalid value; LIST or GET allowed, "{method}" provided')
        return response

    def lookup_entity(
        self,
        name: Optional[str] = None,
        entity_id: Optional[str] = None,
        alias_id: Optional[str] = None,
        alias_name: Optional[str] = None,
        alias_mount_accessor: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Query an entity based on the given criteria.

        The criteria can be name, id, alias_id, or a combination of alias_name and alias_mount_accessor.

        Supported methods:
            POST: /{mount_point}/lookup/entity. Produces: 200 application/json

        :param name: Name of the entity.
        :param entity_id: ID of the entity.
        :param alias_id: ID of the alias.
        :param alias_name: Name of the alias. This should be supplied in conjunction with alias_mount_accessor.
        :param alias_mount_accessor: Accessor of the mount to which the alias belongs to.
            This should be supplied in conjunction with alias_name.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request if an entity / entity alias is found in the lookup, None otherwise.
        """
        params = {}
        if name is not None:
            params["name"] = name
        elif entity_id is not None:
            params["id"] = entity_id
        elif alias_id is not None:
            params["alias_id"] = alias_id
        elif alias_name is not None and alias_mount_accessor is not None:
            params["alias_name"] = alias_name
            params["alias_mount_accessor"] = alias_mount_accessor
        api_path = f"/v1/{mount_point}/lookup/entity"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def lookup_group(
        self,
        name: Optional[str] = None,
        group_id: Optional[str] = None,
        alias_id: Optional[str] = None,
        alias_name: Optional[str] = None,
        alias_mount_accessor: Optional[str] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Query a group based on the given criteria.
        The criteria can be a name, id, alias_id, or a combination of alias_name and alias_mount_accessor.

        Supported methods:
            POST: /{mount_point}/lookup/group. Produces: 200 application/json

        :param name: Name of the group.
        :param group_id: ID of the group.
        :param alias_id: ID of the alias.
        :param alias_name: Name of the alias. This should be supplied in conjunction with alias_mount_accessor.
        :param alias_mount_accessor: Accessor of the mount to which the alias belongs to.
            This should be supplied in conjunction with alias_name.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request if a group / group alias is found in the lookup, None otherwise.
        """
        params = {}
        if name is not None:
            params["name"] = name
        elif group_id is not None:
            params["id"] = group_id
        elif alias_id is not None:
            params["alias_id"] = alias_id
        elif alias_name is not None and alias_mount_accessor is not None:
            params["alias_name"] = alias_name
            params["alias_mount_accessor"] = alias_mount_accessor
        api_path = f"/v1/{mount_point}/lookup/group"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def configure_tokens_backend(
        self, issuer: Optional[str] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Update configurations for OIDC-compliant identity tokens issued by Vault.

        Supported methods:
            POST: {mount_point}/oidc/config.

        :param issuer: Issuer URL to be used in the iss claim of the token. If not set, Vault's api_addr will be used.
            The issuer is a case-sensitive URL using the https scheme that contains scheme, host, and optionally, port
            number and path components, but no query or fragment components.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: dict or response of the configure_tokens_backend request. dict returned when messages
            are included in the response body.
        """
        params = utils.remove_nones(
            {
                "issuer": issuer,
            }
        )

        api_path = f"/v1/{mount_point}/oidc/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_tokens_backend_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query vault identity tokens configurations.

        Supported methods:
            GET: {mount_point}/oidc/config.

        :return: The response of the read_tokens_backend_configuration request.
        """
        api_path = f"/v1/{mount_point}/oidc/config"
        return self._adapter.get(
            url=api_path,
        )

    def create_named_key(
        self,
        name: str,
        rotation_period: str = "24h",
        verification_ttl: str = "24h",
        allowed_client_ids: Optional[list[str]] = None,
        algorithm: str = "RS256",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a named key which is used by a role to sign tokens.

        Supported methods:
            POST: {mount_point}/oidc/key/:name.

        :param name: Name of the named key.
        :param rotation_period: How often to generate a new signing key. Can be specified as a number of seconds or as
            a time string like "30m" or "6h".
        :param verification_ttl: Controls how long the public portion of a signing key will be available for
            verification after being rotated.
        :param allowed_client_ids: List of role client ids allowed to use this key for signing.
            If empty, no roles are allowed. If "*", all roles are allowed.
        :param algorithm: Signing algorithm to use. Allowed values are: RS256 (default), RS384, RS512, ES256, ES384,
            ES512, EdDSA.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_a_named_key request.
        """
        params = {
            "name": name,
            "rotation_period": rotation_period,
            "verification_ttl": verification_ttl,
            "allowed_client_ids": allowed_client_ids,
            "algorithm": algorithm,
        }

        api_path = f"/v1/{mount_point}/oidc/key/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_named_key(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query a named key and returns its configurations.

        Supported methods:
            GET: {mount_point}/oidc/key/:name.

        :param name: Name of the key.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the read_a_named_key request.
        """
        api_path = f"/v1/{mount_point}/oidc/key/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def delete_named_key(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a named key.

        Supported methods:
            DELETE: {mount_point}/oidc/key/:name.

        :param name: Name of the key.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the delete_a_named_key request.
        """
        api_path = f"/v1/{mount_point}/oidc/key/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_named_keys(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List all named keys.

        Supported methods:
            LIST: {mount_point}/oidc/key.

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the list_named_keys request.
        """
        api_path = f"/v1/{mount_point}/oidc/key"
        return self._adapter.list(
            url=api_path,
        )

    def rotate_named_key(
        self, name: str, verification_ttl: str, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Rotate a named key.

        Supported methods:
            POST: {mount_point}/oidc/key/:name/rotate.

        :param name: Name of the key to be rotated.
        :param verification_ttl: Controls how long the public portion of the key will be available for
            verification after being rotated.
            Setting verification_ttl here will override the verification_ttl set on the key.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the rotate_a_named_key request.
        """
        params = {
            "verification_ttl": verification_ttl,
        }
        api_path = f"/v1/{mount_point}/oidc/key/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def create_or_update_role(
        self,
        name: str,
        key: str,
        template: Optional[str] = None,
        client_id: Optional[str] = None,
        ttl: str = "24h",
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Create or update a role.
        ID tokens are generated against a role and signed against a named key.

        Supported methods:
            POST: {mount_point}/oidc/role/:name.

        :param name: Name of the role.
        :param key: A configured named key, the key must already exist.
        :param template: The template string to use for generating tokens. This may be in stringified JSON or
            base64 format.
        :param client_id: Optional client ID. A random ID will be generated if left unset.
        :param ttl: TTL of the tokens generated against the role. Can be specified as a number of seconds or as a time
            string like "30m" or "6h".
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the create_or_update_a_role request.
        """
        params = utils.remove_nones(
            {
                "key": key,
                "template": template,
                "client_id": client_id,
                "ttl": ttl,
            }
        )
        api_path = f"/v1/{mount_point}/oidc/role/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Query a role and returns its configuration.

        Supported methods:
            GET: {mount_point}/oidc/role/:name.

        :param name: Name of the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the read_a_role request.
        """
        api_path = f"/v1/{mount_point}/oidc/role/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete a role.

        Supported methods:
            DELETE: {mount_point}/oidc/role/:name.


        :param name: Name of the role.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the delete_a_role request.
        """
        api_path = f"/v1/{mount_point}/oidc/role/{name}"
        return self._adapter.delete(
            url=api_path,
        )

    def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        This endpoint will list all signing keys.

        Supported methods:
            LIST: {mount_point}/oidc/role.


        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the list_roles request.
        """
        api_path = f"/v1/{mount_point}/oidc/role"
        return self._adapter.list(
            url=api_path,
        )

    def generate_signed_id_token(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Generate a signed ID (OIDC) token.

        Supported methods:
            GET: {mount_point}/oidc/token/:name.

        :param name: The name of the role against which to generate a signed ID token
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the generate_a_signed_id_token request.
        """
        api_path = f"/v1/{mount_point}/oidc/token/{name}"
        return self._adapter.get(
            url=api_path,
        )

    def introspect_signed_id_token(
        self, token: str, client_id: Optional[str] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Verify the authenticity and active state of a signed ID token.

        Supported methods:
            POST: {mount_point}/oidc/introspect.


        :param token: A signed OIDC compliant ID token
        :param client_id: Specifying the client ID optimizes validation time
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the introspect_a_signed_id_token request.
        """
        params = utils.remove_nones(
            {
                "token": token,
                "client_id": client_id,
            }
        )
        api_path = f"/v1/{mount_point}/oidc/introspect"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_well_known_configurations(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Retrieve a set of claims about the identity tokens' configuration.
        The response is a compliant OpenID Provider Configuration Response.

        Supported methods:
            GET: {mount_point}/oidc/.well-known/openid-configuration.

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the read_well_known_configurations request.
        """
        api_path = f"/v1/{mount_point}/oidc/.well-known/openid-configuration"
        return self._adapter.get(
            url=api_path,
        )

    def read_active_public_keys(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Retrieve the public portion of named keys.
        Clients can use this to validate the authenticity of an identity token.

        Supported methods:
            GET: {mount_point}/oidc/.well-known/openid-configuration.

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the read_active_public_keys request.
        """
        api_path = f"/v1/{mount_point}/oidc/.well-known/keys"
        return self._adapter.get(
            url=api_path,
        )
