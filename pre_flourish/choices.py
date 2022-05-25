from edc_constants.constants import OTHER, YES, NO, DWTA, NOT_APPLICABLE
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

APPT_STATUS = (
    ('pending', 'Pending'),
    ('done', 'Done'),
    ('re_schedule', 'Re Schedule'),
)

APPT_GRADING = (
    ('firm', 'Firm appointment'),
    ('weak', 'Possible appointment'),
    ('guess', 'Estimated by RA'),
)

APPT_LOCATIONS = (
    ('home', 'At home'),
    ('work', 'At work'),
    ('telephone', 'By telephone'),
    ('clinic', 'At clinic'),
    ('OTHER', 'Other location'),
)

APPT_REASONS_UNWILLING = (
    ('not_interested', 'Not interested in participating'),
    ('busy', 'Busy during the suggested times'),
    ('away', 'Out of town during the suggested times'),
    ('unavailable', 'Not available during the suggested times'),
    (DWTA, 'Prefer not to say why I am unwilling.'),
    (OTHER, 'Other reason ...'),
)

APPT_TYPE = (
    ('screening', 'Screening'),
    ('re_call', 'Re-call'),
    ('consenting', 'Consenting'),
    (OTHER, 'Other')

)

CONTACT_FAIL_REASON = (
    ('no_response', 'Phone rang, no response but voicemail left'),
    ('no_response_vm_not_left', 'Phone rang no response and no option to leave voicemail'),
    ('disconnected', 'Phone did not ring/number disconnected'),
    ('number_changed', 'No longer the phone number of BHP participant'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

MAY_CALL = (
    (YES, 'Yes, we may continue to contact the participant.'),
    ('no_flourish_study_calls', 'No, the participant has asked to not be contacted about the FLOURISH study.'),
    ('no_any_bhp_study_calls', 'No, the participant has asked not to be contacted about ANY BHP study'),
    (NOT_APPLICABLE, 'Not Applicable')
)

UNSUCCESSFUL_VISIT = (
    ('no_one_was_home', 'No one was home'),
    ('location_no_longer_used', 'Previous BHP participant no longer uses this location'),
    (NOT_APPLICABLE, 'Not Applicable'),
    (OTHER, 'Other'),
)

HOME_VISIT = (
    (NOT_APPLICABLE, 'Not Applicable'),
    ('never_answer', 'Decide to do home visit because the phone is never answered'),
    ('requested_home_visit', 'Participants prefers/requested a home visit'),
    (OTHER, 'Other reason ...'),
)

PHONE_SUCCESS = (
    ('subject_cell', 'subject_cell'),
    ('subject_cell_alt', 'subject_cell_alt'),
    ('subject_phone', 'subject_phone'),
    ('subject_phone_alt', 'subject_phone_alt'),
    ('subject_work_phone', 'subject_work_phone'),
    ('indirect_contact_cell', 'indirect_contact_cell'),
    ('indirect_contact_phone', 'indirect_contact_phone'),
    ('caretaker_cell', 'caretaker_cell'),
    ('caretaker_tel', 'caretaker_tel'),
    ('none_of_the_above', 'None of the above'),
)

PHONE_USED = (
    ('subject_cell', 'subject_cell'),
    ('subject_cell_alt', 'subject_cell_alt'),
    ('subject_phone', 'subject_phone'),
    ('subject_phone_alt', 'subject_phone_alt'),
    ('subject_work_phone', 'subject_work_phone'),
    ('indirect_contact_cell', 'indirect_contact_cell'),
    ('indirect_contact_phone', 'indirect_contact_phone'),
    ('caretaker_cell', 'caretaker_cell'),
    ('caretaker_tel', 'caretaker_tel'),
)

YES_NO_ST_NA = (
    (YES, YES),
    (NO, NO),
    ('thinking', 'Still thinking'),
    (NOT_APPLICABLE, 'Not applicable'),
)
