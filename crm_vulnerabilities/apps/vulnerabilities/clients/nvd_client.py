import requests


class ExternalAPIError(Exception):
    """Exception raised for errors in the external API."""

    pass


class NVDClient:
    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

    def __init__(self):
        self._vulnerabilities_cache = None

    def fetch_vulnerabilities(self, start_index=0, max_results=2000):
        """Obtiene las vulnerabilidades desde la API del NIST con paginación"""
        try:
            params = {"startIndex": start_index, "resultsPerPage": max_results}
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            raise ExternalAPIError(
                "Error fetching vulnerabilities from NIST API"
            ) from e

        # Cache the vulnerabilities to avoid redundant API calls
        self._vulnerabilities_cache = (
            response.json().get("result", {}).get("CVE_Items", [])
        )
        data = response.json()["vulnerabilities"]
        return data

    def vulnerability_exists(self, vulnerability_id):
        """Verifica si una vulnerabilidad existe en el conjunto de datos obtenido de la API del NIST"""
        if self._vulnerabilities_cache is None:
            self.fetch_vulnerabilities()

        # Check if the vulnerability_id is in the cached list of vulnerabilities
        return any(
            vuln.get("cve", {}).get("CVE_data_meta", {}).get("ID") == vulnerability_id
            for vuln in self._vulnerabilities_cache
        )
