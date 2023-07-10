from pre_flourish.helper_classes.match_helper import MatchHelper


class HEUHUUMatch(MatchHelper):
    def __init__(self, subject_identifiers=None, heu_bmi_age_data=None):
        self.subject_identifiers = subject_identifiers
        self.heu_bmi_age_data = heu_bmi_age_data
