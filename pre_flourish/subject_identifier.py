from edc_identifier.subject_identifier import SubjectIdentifier


class PreFlourishIdentifier(SubjectIdentifier):

    template = 'PF{protocol_number}-0{site_id}{device_id}{sequence}'
