from typing import Optional

from vaultx import utils
from vaultx.adapters import VaultxResponse
from vaultx.api.vault_api_base import AsyncVaultApiBase


DEFAULT_MOUNT_POINT = "pki"


class Pki(AsyncVaultApiBase):
    """
    Pki Secrets Engine (API).

    Reference: https://www.vaultproject.io/api/secret/pki/index.html
    """

    async def read_ca_certificate(self, mount_point: str = DEFAULT_MOUNT_POINT) -> str:
        """
        Read CA Certificate.
        Retrieve the CA certificate in raw DER-encoded form.

        Supported methods:
            GET: /{mount_point}/ca/pem. Produces: String

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The certificate as pem.
        """
        api_path = f"/v1/{mount_point}/ca/pem"
        response = await self._adapter.get(
            url=api_path,
        )
        return str(response.raw.text)

    async def read_ca_certificate_chain(self, mount_point: str = DEFAULT_MOUNT_POINT) -> str:
        """
        Read CA Certificate Chain.
        Retrieve the CA certificate chain, including the CA in PEM format.

        Supported methods:
            GET: /{mount_point}/ca_chain. Produces: String

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The certificate chain as pem.
        """
        api_path = f"/v1/{mount_point}/ca_chain"
        response = await self._adapter.get(
            url=api_path,
        )
        return str(response.raw.text)

    async def read_certificate(self, serial: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read Certificate.
        Retrieve one of a selection of certificates.

        Supported methods:
            GET: /{mount_point}/cert/{serial}. Produces: 200 application/json

        :param serial: the serial of the key to read.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/cert/{serial}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_certificates(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List Certificates.
        The list of the current certificates by serial number only.

        Supported methods:
            LIST: /{mount_point}/certs. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/certs"
        return await self._adapter.list(
            url=api_path,
        )

    async def submit_ca_information(self, pem_bundle: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Submit CA Information.
        Submitting the CA information for the backend.

        Supported methods:
            POST: /{mount_point}/config/ca. Produces: 200 application/json

        :param pem_bundle: Specifies the unencrypted private key and certificate, concatenated in PEM format.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        params = {
            "pem_bundle": pem_bundle,
        }
        api_path = f"/v1/{mount_point}/config/ca"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_crl_configuration(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read CRL Configuration.
        Getting the duration for which the generated CRL should be marked valid.

        Supported methods:
            GET: /{mount_point}/config/crl. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/crl"
        return await self._adapter.get(
            url=api_path,
        )

    async def set_crl_configuration(
        self,
        expiry: Optional[str] = None,
        disable: Optional[bool] = None,
        extra_params: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Set CRL Configuration.

        Setting the duration for which the generated CRL should be marked valid.
        If the CRL is disabled, it will return await a signed but zero-length CRL for any
        request. If enabled, it will re-build the CRL.

        Supported methods:
            POST: /{mount_point}/config/crl. Produces: 200 application/json

        :param expiry: The amount of time the generated CRL should be valid.
        :param disable: Disables or enables CRL building.
        :param extra_params: Other extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/config/crl"
        params = extra_params
        params.update(
            utils.remove_nones(
                {
                    "expiry": expiry,
                    "disable": disable,
                }
            )
        )

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_urls(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read URLs.
        Fetch the URLs to be encoded in generated certificates.

        Supported methods:
            GET: /{mount_point}/config/urls. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/urls"
        return await self._adapter.get(
            url=api_path,
        )

    async def set_urls(self, params: dict, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Set URLs.

        Setting the issuing certificate endpoints, CRL distribution points, and OCSP server endpoints that will be
        encoded into issued certificates. You can update any of the values at any time without affecting the other
        existing values. To remove the values, simply use a blank string as the parameter.

        Supported methods:
            POST: /{mount_point}/config/urls. Produces: 200 application/json

        :param params: The parameters to insert as json.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/config/urls"
        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_crl(self, mount_point: str = DEFAULT_MOUNT_POINT) -> str:
        """
        Read CRL.

        Retrieves the current CRL in PEM format.
        This endpoint is an unauthenticated.

        Supported methods:
            GET: /{mount_point}/crl/pem. Produces: 200 application/pkix-crl

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The content of the request e.g. CRL string representation.
        """
        api_path = f"/v1/{mount_point}/crl/pem"
        response = await self._adapter.get(
            url=api_path,
        )
        return str(response.raw.text)

    async def rotate_crl(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Rotate CRLs.
        Force a rotation of the CRL.

        Supported methods:
            GET: /{mount_point}/crl/rotate. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/crl/rotate"
        return await self._adapter.get(
            url=api_path,
        )

    async def generate_intermediate(
        self,
        _type: str,
        common_name: str,
        extra_params: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Generate Intermediate.
        Generate a new private key and a CSR for signing.

        Supported methods:
            POST: /{mount_point}/intermediate/generate/{type}. Produces: 200 application/json

        :param _type: Specifies the type to create. `exported` (private key also exported) or `internal`.
        :param common_name: Specifies the requested CN for the certificate.
        :param extra_params: Dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :param wrap_ttl: Specifies response wrapping token creation with duration. IE: '15s', '20m', '25h'.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/intermediate/generate/{_type}"

        params = extra_params
        params["common_name"] = common_name

        return await self._adapter.post(
            url=api_path,
            json=params,
            wrap_ttl=wrap_ttl,
        )

    async def set_signed_intermediate(self, certificate: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Set Signed Intermediate.
        Allow submitting the signed CA certificate corresponding to a private key generated via "Generate Intermediate"

        Supported methods:
            POST: /{mount_point}/intermediate/set-signed. Produces: 200 application/json

        :param certificate: Specifies the certificate in PEM format.
        :param mount_point: The "path" the method/backend was mounted on.
        """
        api_path = f"/v1/{mount_point}/intermediate/set-signed"
        params = {"certificate": certificate}

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def generate_certificate(
        self,
        name: str,
        common_name: str,
        extra_params: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Generate Certificate.
        Generates a new set of credentials (private key and certificate) based on the role named in the endpoint.

        Supported methods:
            POST: /{mount_point}/issue/{name}. Produces: 200 application/json

        :param name: The name of the role to create the certificate against.
        :param common_name: The requested CN for the certificate.
        :param extra_params: A dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :param wrap_ttl: Specifies response wrapping token creation with duration. IE: '15s', '20m', '25h'.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/issue/{name}"

        params = extra_params
        params["common_name"] = common_name

        return await self._adapter.post(
            url=api_path,
            json=params,
            wrap_ttl=wrap_ttl,
        )

    async def revoke_certificate(self, serial_number: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Revoke Certificate.
        Revoke a certificate using its serial number.

        Supported methods:
            POST: /{mount_point}/revoke. Produces: 200 application/json

        :param serial_number: The serial number of the certificate to revoke.
        :param mount_point: The "path" the method/backend was mounted on.
        """
        api_path = f"/v1/{mount_point}/revoke"
        params = {"serial_number": serial_number}

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def create_or_update_role(
        self, name: str, extra_params: Optional[dict] = None, mount_point=DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Create/Update Role.
        Create or updates the role definition.

        Supported methods:
            POST: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: The name of the role to create.
        :param extra_params: A dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/roles/{name}"

        params = extra_params
        params["name"] = name

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read Role.
        Query the role definition.

        Supported methods:
            GET: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: The name of the role to read.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"
        return await self._adapter.get(
            url=api_path,
        )

    async def list_roles(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List Roles.
        Get a list of available roles.

        Supported methods:
            LIST: /{mount_point}/roles. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles"
        return await self._adapter.list(
            url=api_path,
        )

    async def delete_role(self, name: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete Role.
        Delete the role definition.

        Supported methods:
            DELETE: /{mount_point}/roles/{name}. Produces: 200 application/json

        :param name: The name of the role to delete.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/roles/{name}"

        return await self._adapter.delete(
            url=api_path,
        )

    async def generate_root(
        self,
        _type: str,
        common_name: str,
        extra_params: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
        wrap_ttl: Optional[str] = None,
    ) -> VaultxResponse:
        """
        Generate Root.
        Generate a new self-signed CA certificate and private key.

        Supported methods:
            POST: /{mount_point}/root/generate/{type}. Produces: 200 application/json

        :param _type: Specifies the type to create. `exported` (private key also exported) or `internal`.
        :param common_name: The requested CN for the certificate.
        :param extra_params: A dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :param wrap_ttl: Specifies response wrapping token creation with duration. IE: '15s', '20m', '25h'.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/root/generate/{_type}"

        params = extra_params
        params["common_name"] = common_name

        return await self._adapter.post(
            url=api_path,
            json=params,
            wrap_ttl=wrap_ttl,
        )

    async def delete_root(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete Root.
        Delete the current CA key.

        Supported methods:
            DELETE: /{mount_point}/root. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/root"

        return await self._adapter.delete(
            url=api_path,
        )

    async def sign_intermediate(
        self, csr: str, common_name: str, extra_params: Optional[dict] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Sign Intermediate.
        Issue a certificate with appropriate values for acting as an intermediate CA.

        Supported methods:
            POST: /{mount_point}/root/sign-intermediate. Produces: 200 application/json

        :param csr: The PEM-encoded CSR.
        :param common_name: The requested CN for the certificate.
        :param extra_params: Dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/root/sign-intermediate"

        params = extra_params
        params["csr"] = csr
        params["common_name"] = common_name

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def sign_self_issued(self, certificate: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Sign Self-Issued.
        Sign a self-issued certificate.

        Supported methods:
            POST: /{mount_point}/root/sign-self-issued. Produces: 200 application/json

        :param certificate: The PEM-encoded self-issued certificate.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/root/sign-self-issued"

        params = {"certificate": certificate}

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def sign_certificate(
        self,
        name: str,
        csr: str,
        common_name: str,
        extra_params: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Sign Certificate.
        Sign a new certificate based upon the provided CSR and the supplied parameters.

        Supported methods:
            POST: /{mount_point}/sign/{name}. Produces: 200 application/json

        :param name: The role to sign the certificate.
        :param csr: The PEM-encoded CSR.
        :param common_name: The requested CN for the certificate.
            If the CN is allowed by role policy, it will be issued.
        :param extra_params: A dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/sign/{name}"

        params = extra_params
        params["csr"] = csr
        params["common_name"] = common_name

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def sign_verbatim(
        self,
        csr: str,
        name: Optional[str] = None,
        extra_params: Optional[dict] = None,
        mount_point: str = DEFAULT_MOUNT_POINT,
    ) -> VaultxResponse:
        """
        Sign Verbatim.
        Sign a new certificate based upon the provided CSR.

        Supported methods:
            POST: /{mount_point}/sign-verbatim. Produces: 200 application/json

        :param csr: The PEM-encoded CSR.
        :param name: Specifies a role.
        :param extra_params: A dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/sign-verbatim"
        if name:
            api_path = api_path + f"/{name}"

        params = extra_params
        params["csr"] = csr

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def tidy(self, extra_params: Optional[dict] = None, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Tidy.
        Allow tidying up the storage backend and/or CRL by removing certificates that have
        expired and are past a certain buffer period beyond their expiration time.

        Supported methods:
            POST: /{mount_point}/tidy. Produces: 200 application/json

        :param extra_params: A dictionary with extra parameters.
        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        if extra_params is None:
            extra_params = {}
        api_path = f"/v1/{mount_point}/tidy"
        params = extra_params

        return await self._adapter.post(
            url=api_path,
            json=params,
        )

    async def read_issuer(self, issuer_ref, mount_point=DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Read issuer.
        Get configuration of an issuer by its reference ID.

        Supported methods:
            GET: /{mount_point}/issuer/{issuer_ref}. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :param issuer_ref: The reference ID of the issuer to get
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/issuer/{issuer_ref}"

        return await self._adapter.get(
            url=api_path,
        )

    async def list_issuers(self, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        List issuers.
        Get list of all issuers for a given pki mount.

        Supported methods:
            LIST: /{mount_point}/issuers. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/issuers"

        return await self._adapter.list(
            url=api_path,
        )

    async def update_issuer(
        self, issuer_ref: str, extra_params: Optional[dict] = None, mount_point: str = DEFAULT_MOUNT_POINT
    ) -> VaultxResponse:
        """
        Update issuer.
        Update a given issuer.

        Supported methods:
            POST: /{mount_point}/issuer/{issuer_ref}. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :param issuer_ref: The reference ID of the issuer to update
        :param extra_params: Dictionary with extra parameters.
        :return: The VaultxResponse of the request.
        """
        params = extra_params

        api_path = f"/v1/{mount_point}/issuer/{issuer_ref}"

        return await self._adapter.post(url=api_path, json=params)

    async def revoke_issuer(self, issuer_ref: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Revoke issuer.
        Revoke a given issuer.

        Supported methods:
            POST: /{mount_point}/issuer/{issuer_ref}/revoke. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :param issuer_ref: The reference ID of the issuer to revoke
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/issuer/{issuer_ref}/revoke"

        return await self._adapter.post(
            url=api_path,
        )

    async def delete_issuer(self, issuer_ref: str, mount_point: str = DEFAULT_MOUNT_POINT) -> VaultxResponse:
        """
        Delete issuer.
        Delete a given issuer. Deleting the default issuer will result in a warning

        Supported methods:
            DELETE: /{mount_point}/issuer/{issuer_ref}. Produces: 200 application/json

        :param mount_point: The "path" the method/backend was mounted on.
        :param issuer_ref: The reference ID of the issuer to delete
        :return: The VaultxResponse of the request.
        """
        api_path = f"/v1/{mount_point}/issuer/{issuer_ref}"

        return await self._adapter.delete(
            url=api_path,
        )
