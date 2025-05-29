class RuleManager:
    def __init__(self):
        self.rules = []

    def add_rule(self, rule):
        self.rules.append(rule)

    def remove_rule(self, rule):
        if rule in self.rules:
            self.rules.remove(rule)

    def get_rules(self):
        return self.rules

    def apply_rules(self, response):
        for rule in self.rules:
            response = rule.apply(response)
        return response