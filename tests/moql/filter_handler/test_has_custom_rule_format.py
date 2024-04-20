from moapi.moql.filter_handler import has_custom_rule_format


class TestHasCustomRuleFormat:
    def test_when_has_custom_rule(self):
        assert has_custom_rule_format(rule="string", value="string(1)")

    def test_when_does_not_have_custom_rule_format(self):
        assert not has_custom_rule_format(rule="string", value="value")
