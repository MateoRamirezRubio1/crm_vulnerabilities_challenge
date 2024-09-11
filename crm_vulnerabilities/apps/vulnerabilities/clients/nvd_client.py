import requests
import time
from typing import List, Dict
import logging

# Configure logger for this module
logger = logging.getLogger("vulnerabilities")


class ExternalAPIError(Exception):
    """Exception raised for errors in the external API."""

    pass


class NVDClient:
    BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"
    CACHE_TIMEOUT = 3600

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(NVDClient, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self._vulnerabilities_cache = None
        self._cache_timestamp = 0

    def _is_cache_valid(self) -> bool:
        """Check if the cache is still valid based on the timeout."""
        current_time = time.time()
        if self._vulnerabilities_cache is None:
            logger.debug("Cache is invalid: No cache found.")
            return False
        is_valid = (current_time - self._cache_timestamp) < self.CACHE_TIMEOUT
        if is_valid:
            logger.debug("Cache is valid.")
        else:
            logger.debug("Cache is invalid: Timeout exceeded.")
        return is_valid

    def _fetch_vulnerabilities_from_api(self, start_index=0, max_results=2000):
        """Get vulnerabilities from NIST API with paging"""
        try:
            params = {"startIndex": start_index, "resultsPerPage": max_results}
            response = requests.get(self.BASE_URL, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error("Error fetching vulnerabilities from NIST API", exc_info=True)
            raise ExternalAPIError(
                "Error fetching vulnerabilities from NIST API"
            ) from e

        data = response.json().get("vulnerabilities", [])
        logger.debug("Fetched %d vulnerabilities from API.", len(data))
        return data

    def fetch_vulnerabilities(self, start_index=0, max_results=2000) -> List[Dict]:
        """Fetches vulnerabilities with caching."""
        if not self._is_cache_valid():
            # Fetch new data and update cache
            self._vulnerabilities_cache = self._fetch_vulnerabilities_from_api(
                start_index, max_results
            )
            self._cache_timestamp = time.time()
            logger.debug("Data fetched from API. Cache updated.")
        else:
            logger.debug("Data retrieved from cache.")

        return self._vulnerabilities_cache

    def vulnerability_exists(self, vulnerability_id):
        """Verifica si una vulnerabilidad existe en el conjunto de datos obtenido de la API del NIST"""
        if self._vulnerabilities_cache is None or not self._is_cache_valid():
            self.fetch_vulnerabilities()

        # Check if the vulnerability_id is in the cached list of vulnerabilities
        exists = any(
            vuln.get("cve", {}).get("CVE_data_meta", {}).get("ID") == vulnerability_id
            for vuln in self._vulnerabilities_cache
        )
        logger.debug("Vulnerability %s existence check: %s", vulnerability_id, exists)
        return exists
