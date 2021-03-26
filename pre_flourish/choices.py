from edc_constants.constants import OTHER, YES, NO
from edc_constants.constants import NEG, POS, IND

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    (OTHER, 'Other'),
)

POS_NEG_IND = (
  (POS, 'Positive'),
  (NEG, 'Negative'),
  (IND, 'Indeterminate')
)

RECRUIT_SOURCE = (
    ('ANC clinic staff', 'ANC clinic staff'),
    ('BHP recruiter/clinician', 'BHP recruiter/clinician'),
    (OTHER, 'Other, specify'),
)

RECRUIT_CLINIC = (
    ('Prior', 'Prior BHP Study'),
    ('PMH', 'Gaborone(PMH)'),
    ('G.West Clinic', 'G.West Clinic'),
    ('BH3 Clinic', 'BH3 Clinic'),
    ('Ext2', 'Extension 2 Clinic'),
    ('Nkoyaphiri', 'Nkoyaphiri Clinic'),
    ('Lesirane', 'Lesirane Clinic'),
    ('Old Naledi', 'Old Naledi'),
    ('Mafitlhakgosi', 'Mafitlhakgosi'),
    ('Schools', 'Schools'),
    (OTHER, 'Other health facilities not associated with study site'),
)

UNCERTAIN_GEST_AGE = (
    ('born_on_time', 'This child was born on time'),
    ('born_early', 'This child was born early'),
    ('born_late', 'This child was born late'),
    ('unknown', 'This child’s gestational age is unknown')
)

YES_NO_UNCERTAIN = (
    ('0', NO),
    ('1', YES),
    ('2', 'Uncertain'),
)

YES_NO_UNKNOWN = (
    (YES, YES),
    (NO, NO),
    ('Unknown', 'Unknown'),
)
