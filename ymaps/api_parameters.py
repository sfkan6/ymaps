"""
API Parameter Collector for ymaps
"""


class ParameterCollector:
    params_separate_by_comma = ["ll", "spn", "size", "types", "ull", "reverse"]
    params_separate_by_tilda = ["pt", "pl"]
    params_bool_values = ["rspn", "highlight", "strict_bounds", "print_address"]

    def _collect_request_parameters(self, **params):
        correct_params = params

        for key in self.params_separate_by_comma:
            if params.get(key):
                correct_params[key] = ",".join(map(str, params[key]))

        for key in self.params_separate_by_tilda:
            if params.get(key):
                correct_params[key] = "~".join(map(str, params[key]))

        for key in self.params_bool_values:
            if key in params.keys():
                correct_params[key] = 1 if params[key] else 0

        if params.get("bbox"):
            correct_params["bbox"] = "{},{}~{},{}".format(*params["bbox"])

        return correct_params
