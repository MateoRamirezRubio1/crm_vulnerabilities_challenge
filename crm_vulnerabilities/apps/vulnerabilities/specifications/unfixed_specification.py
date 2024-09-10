class UnfixedVulnerabilitiesSpecification:
    def __init__(self, fixed_vulnerabilities) -> None:
        self.fixed_vulnerabilities = fixed_vulnerabilities

    def is_satisfied_by(self, vulnerability):
        return vulnerability["cve"]["id"] not in [
            vuln.id for vuln in self.fixed_vulnerabilities
        ]
