import logging
from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import VaultApiBase
from vaultx.constants.gcp import ALLOWED_ROLE_TYPES, GCP_CERTS_ENDPOINT
from vaultx.exceptions import VaultxError
from vaultx.utils import list_to_comma_delimited, validate_list_of_strings_param


DEFAULT_MOUNT_POINT = "gcp"


logger = logging.getLogger(__name__)


class Gcp(VaultApiBase):
    """
    Google Cloud Auth Method (API).

    Reference: https://www.vaultproject.io/api/auth/{mount_point}/index.html
    """

    def configure(
        self,
        credentials: Optional[str] = None,
        google_certs_endpoint: str = GCP_CERTS_ENDPOINT,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Configure the credentials required for the GCP auth method to perform API calls to Google Cloud.

        These credentials will be used to query the status of IAM entities and get service account or other Google
        public certificates to confirm signed JWTs passed in during login.

        Supported methods:
            POST: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param credentials: A JSON string containing the contents of a GCP credentials file. The credentials file must
            have the following permissions: `iam.serviceAccounts.get`, `iam.serviceAccountKeys.get`.
            If this value is empty, Vault will try to use Application Default Credentials from the machine on which the
            Vault server is running. The project must have the iam.googleapis.com API enabled.
        :param google_certs_endpoint: The Google OAuth2 endpoint from which to obtain public certificates. This is used
            for testing and should generally not be set by end users.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "credentials": credentials,
                "google_certs_endpoint": google_certs_endpoint,
            }
        )
        api_path = f"/v1/auth/{mount_point}/config"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
        """
        Read the configuration, if any, including credentials.

        Supported methods:
            GET: /auth/{mount_point}/config. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        response = self._adapter.get(
            url=api_path,
        )
        return response.value["data"]

    def delete_config(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete all GCP configuration data. This operation is idempotent.

        Supported methods:
            DELETE: /auth/{mount_point}/config. Produces: 204 (empty body)

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        api_path = f"/v1/auth/{mount_point}/config"
        return self._adapter.delete(
            url=api_path,
        )

    def create_role(  # noqa: C901
        self,
        name: str,
        role_type: str,
        project_id: str,
        ttl: Optional[str] = None,
        max_ttl: Optional[str] = None,
        period: Optional[str] = None,
        policies: Optional[list[str]] = None,
        bound_service_accounts: Optional[list[str]] = None,
        max_jwt_exp: Optional[str] = None,
        allow_gce_inference: Optional[bool] = None,
        bound_zones: Optional[list[str]] = None,
        bound_regions: Optional[list[str]] = None,
        bound_instance_groups: Optional[list[str]] = None,
        bound_labels: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Register a role in the GCP auth method.

        Role types have specific entities that can perform login operations against this endpoint. Constraints specific
            to the role type must be set on the role. These are applied to the authenticated entities attempting to
            log in.

        Supported methods:
            POST: /auth/{mount_point}/role/{name}. Produces: 204 (empty body)

        :param name: The name of the role.
        :param role_type: The type of this role. Certain fields correspond to specific roles and will be rejected
            otherwise.
        :param project_id: The GCP project ID. Only entities belonging to this project can authenticate with this role.
        :param ttl: The TTL period of tokens issued using this role. This can be specified as an integer number of
            seconds or as a duration value like "5m".
        :param max_ttl: The maximum allowed lifetime of tokens issued in seconds using this role. This can be specified
            as an integer number of seconds or as a duration value like "5m".
        :param period: If set, indicates that the token generated using this role should never expire. The token should
            be renewed within the duration specified by this value. At each renewal, the token's TTL will be set to the
            value of this parameter. This can be specified as an integer number of seconds or as a duration value like
            "5m".
        :param policies: The list of policies to be set on tokens issued using this role.
        :param bound_service_accounts: <required for iam> A list of service account emails or IDs that login is
            restricted  to. If set to `*`, all service accounts are allowed (role will still be bound by project).
            Will be inferred from service account used to issue metadata token for GCE instances.
        :param max_jwt_exp: <iam only> The number of seconds past the time of authentication that the login param JWT
            must expire within. For example, if a user attempts to log in with a token that expires within an hour and
            this is set to 15 minutes, Vault will return an error prompting the user to create a new signed JWT with a
            shorter exp. The GCE metadata tokens currently do not allow the exp claim to be customized.
        :param allow_gce_inference: <iam only> A flag to determine if this role should allow GCE instances to
            authenticate by inferring service accounts from the GCE identity metadata token.
        :param bound_zones: <gce only> The list of zones that a GCE instance must belong to in order to be
            authenticated. If bound_instance_groups is provided, it is assumed to be a zonal group and the group must
            belong to this zone.
        :param bound_regions: <gce only> The list of regions that a GCE instance must belong to in order to be
            authenticated. If bound_instance_groups is provided, it is assumed to be a regional group and the group
            must belong to this region. If bound_zones provided, this attribute ignored.
        :param bound_instance_groups: <gce only> The instance groups that an authorized instance must belong to in
            order to be authenticated. If specified, either bound_zones or bound_regions must be set too.
        :param bound_labels: <gce only> A list of GCP labels formatted as "key:value" strings that must be set on
            authorized GCE instances. Because GCP labels are not currently ACL'd, we recommend that this be used in
            conjunction with other restrictions.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        type_specific_params = {
            "iam": {
                "max_jwt_exp": None,
                "allow_gce_inference": None,
            },
            "gce": {
                "bound_zones": None,
                "bound_regions": None,
                "bound_instance_groups": None,
                "bound_labels": None,
            },
        }

        list_of_strings_params = {
            "policies": policies,
            "bound_service_accounts": bound_service_accounts,
            "bound_zones": bound_zones,
            "bound_regions": bound_regions,
            "bound_instance_groups": bound_instance_groups,
            "bound_labels": bound_labels,
        }
        for param_name, param_argument in list_of_strings_params.items():
            validate_list_of_strings_param(
                param_name=param_name,
                param_arg=param_argument,
            )

        if role_type not in ALLOWED_ROLE_TYPES:
            role_types = ",".join(ALLOWED_ROLE_TYPES)
            raise VaultxError(f'unsupported role_type argument provided "{role_type}", supported types: "{role_types}"')

        params = {
            "type": role_type,
            "project_id": project_id,
            "policies": list_to_comma_delimited(policies),
        }
        params.update(
            utils.remove_nones(
                {
                    "ttl": ttl,
                    "max_ttl": max_ttl,
                    "period": period,
                }
            )
        )
        if bound_service_accounts is not None:
            params["bound_service_accounts"] = list_to_comma_delimited(bound_service_accounts)
        if role_type == "iam":
            params.update(
                utils.remove_nones(
                    {
                        "max_jwt_exp": max_jwt_exp,
                        "allow_gce_inference": allow_gce_inference,
                    }
                )
            )
            for param, default_arg in type_specific_params["gce"].items():
                if locals().get(param) != default_arg:
                    warning_msg = f'Argument for parameter "{param}" ignored for role type iam'
                    logger.warning(warning_msg)
        elif role_type == "gce":
            if bound_zones is not None:
                params["bound_zones"] = list_to_comma_delimited(bound_zones)
            if bound_regions is not None:
                params["bound_regions"] = list_to_comma_delimited(bound_regions)
            if bound_instance_groups is not None:
                params["bound_instance_groups"] = list_to_comma_delimited(bound_instance_groups)
            if bound_labels is not None:
                params["bound_labels"] = list_to_comma_delimited(bound_labels)
            for param, default_arg in type_specific_params["iam"].items():
                if locals().get(param) != default_arg:
                    warning_msg = f'Argument for parameter "{param}" ignored for role type gce'
                    logger.warning(warning_msg)

        api_path = f"/v1/auth/{mount_point}/role/{name}"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def edit_service_accounts_on_iam_role(
        self,
        name: str,
        add: Optional[list[str]] = None,
        remove: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Edit service accounts for an existing IAM role in the GCP auth method.

        This allows you to add or remove service accounts from the list of service accounts on the role.

        Supported methods:
            POST: /auth/{mount_point}/role/{name}/service-accounts. Produces: 204 (empty body)

        :param name: The name of an existing iam type role. This will return an error if role is not an iam type role.
        :param add: The list of service accounts to add to the role's service accounts.
        :param remove: The list of service accounts to remove from the role's service accounts.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = utils.remove_nones(
            {
                "add": add,
                "remove": remove,
            }
        )
        api_path = f"/v1/auth/{mount_point}/role/{name}/service-accounts"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def edit_labels_on_gce_role(
        self,
        name: str,
        add: Optional[list[str]] = None,
        remove: Optional[list[str]] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Edit labels for an existing GCE role in the backend.

        This allows you to add or remove labels (keys, values, or both) from the list of keys on the role.

        Supported methods:
            POST: /auth/{mount_point}/role/{name}/labels. Produces: 204 (empty body)

        :param name: The name of an existing gce role. This will return an error if role is not a gce type role.
        :param add: The list of key:value labels to add to the GCE role's bound labels.
        :param remove: The list of label keys to remove from the role's bound labels. If any of the specified keys do
            not exist, no error is returned (idempotent).
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the edit_labels_on_gce_role request.
        """
        params = utils.remove_nones(
            {
                "add": add,
                "remove": remove,
            }
        )
        api_path = f"/v1/auth/{mount_point}/role/{name}/labels"
        return self._adapter.post(
            url=api_path,
            json=params,
        )

    def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read the previously registered role configuration.

        Supported methods:
            GET: /auth/{mount_point}/role/{name}. Produces: 200 application/json

        :param name: The name of the role to read.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the read_role request.
        """
        params = {
            "name": name,
        }
        api_path = f"/v1/auth/{mount_point}/role/{name}"
        response = self._adapter.get(
            url=api_path,
            json=params,
        )
        return response.value["data"]

    def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> dict:
        """
        List all the roles that are registered with the plugin.

        Supported methods:
            LIST: /auth/{mount_point}/roles. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The data key from the VaultxResponse of the request.
        """
        api_path = f"/v1/auth/{mount_point}/roles"
        response = self._adapter.list(
            url=api_path,
        )
        return response.value["data"]

    def delete_role(self, role: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete the previously registered role.

        Supported methods:
            DELETE: /auth/{mount_point}/role/{role}. Produces: 204 (empty body)

        :param role: The name of the role to delete.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The response of the request.
        """
        params = {
            "role": role,
        }
        api_path = f"/v1/auth/{mount_point}/role/{role}"
        return self._adapter.delete(
            url=api_path,
            json=params,
        )

    def login(
        self, role: str, jwt: str, use_token: bool = True, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Login to retrieve a Vault token via the GCP auth method.

        This endpoint takes a signed JSON Web Token (JWT) and a role name for some entity. It verifies the JWT
            signature with Google Cloud to authenticate that entity and then authorizes the entity for the given role.

        Supported methods:
            POST: /auth/{mount_point}/login. Produces: 200 application/json

        :param role: The name of the role against which the login is being attempted.
        :param jwt: A signed JSON web token
        :param use_token: if True, uses the token in the response received from the auth request to set the "token"
            attribute on the :py:meth:`vaultx.adapters.Adapter` instance under the _adapter Client attribute.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse response of the request.
        """
        params = {
            "role": role,
            "jwt": jwt,
        }
        api_path = f"/v1/auth/{mount_point}/login"
        return self._adapter.login(
            url=api_path,
            use_token=use_token,
            json=params,
        )
