import logging
from typing import List, Dict

logger = logging.getLogger("vulnerabilities")


class UnfixedVulnerabilitiesSpecification:

    def __init__(self, fixed_vulnerabilities) -> None:
        """
        Initializes the specification with the fixed vulnerabilities.

        :param fixed_vulnerabilities: List of vulnerabilities that are already fixed.
        """
        self.fixed_vulnerabilities = fixed_vulnerabilities

    def is_satisfied_by(self, vulnerability: Dict) -> bool:
        """
        Determines if the given vulnerability is not in the list of fixed vulnerabilities.

        :param vulnerability: Vulnerability to check.
        :return: True if the vulnerability is not in the list of fixed vulnerabilities, False otherwise.
        :raises Exception: If any error occurs during the verification process.
        """
        try:
            vulnerability_id = vulnerability.get("cve", {}).get("id")
            if not vulnerability_id:
                logger.warning("Vulnerability without ID provided: %s", vulnerability)
                return False

            fixed_ids = [vuln.id for vuln in self.fixed_vulnerabilities]
            result = vulnerability_id not in fixed_ids

            """
            logger.debug(
                "Vulnerability ID '%s' is %s in the list of fixed vulnerabilities.",
                vulnerability_id,
                "not present" if result else "present",
            )
            """

            return result
        except Exception as e:
            logger.error(
                "Error while checking the vulnerability: %s", str(e), exc_info=True
            )
            raise
