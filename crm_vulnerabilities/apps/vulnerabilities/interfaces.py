class IVulnerabilityRepository:
    def get_fixed_vulnerabilities(self):
        raise NotImplementedError("This method should be implemented in a subclass.")

    def add_to_fixed_vulnerabilities(self, vulnerability_ids):
        raise NotImplementedError("This method should be implemented in a subclass.")
