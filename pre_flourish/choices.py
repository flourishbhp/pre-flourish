from edc_constants.constants import OTHER, YES, NO, DWTA, NOT_APPLICABLE
from edc_constants.constants import NEG, POS, IND

IDENTITY_TYPE = (
    ('country_id', 'Country ID number'),
    ('country_id_rcpt', 'Country ID receipt'),
    ('passport', 'Passport'),
    ('drivers_license', 'Drivers license'),
    ('marriage_certificate', 'Marriage certificate'),
)

POS_NEG_IND = (
    (POS, 'Positive'),
    (NEG, 'Negative'),
    (IND, 'Indeterminate')
)

RECRUIT_SOURCE = (
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
    (OTHER, 'Other, specify'),
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

YES_NO_THINKING = (
    (YES, YES),
    (NO, NO),
    ('thinking', 'Still thinking'),
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
    (
    'no_response_vm_not_left', 'Phone rang no response and no option to leave voicemail'),
    ('disconnected', 'Phone did not ring/number disconnected'),
    ('number_changed', 'No longer the phone number of BHP participant'),
    (NOT_APPLICABLE, 'Not Applicable'),
)

MAY_CALL = (
    (YES, 'Yes, we may continue to contact the participant.'),
    ('no_flourish_study_calls',
     'No, the participant has asked to not be contacted about the FLOURISH study.'),
    ('no_any_bhp_study_calls',
     'No, the participant has asked not to be contacted about ANY BHP study'),
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

CAREGIVER_OFF_STUDY_REASON = (
    ('multiple_vialble_gestations',
     'Multiple (2 or more) viable gestations seen on ultrasound'),
    ('unable_to_determine_ga', 'Unable to confirm GA by Ultrasound.'),
    ('miscarriage_or_arbotion',
     'Miscarriage or abortion'),
    ('fetal_death_gt_20wks',
     'fetal Death at >= 20weeks GA (IUFD) or still born'),
    ('took_art_less_than_4weeks',
     'Biological mother took ART for less than 4 weeks during pregnancy'),
    ('caregiver_death',
     'Caregiver death (complete the Death Report Form AF005)'),
    ('moving_out_of_study_area',
     'Participant stated that they will be moving out of the study area or '
     'unable to stay in study area'),
    ('loss_to_followup',
     'Participant lost to follow-up/unable to locate'),
    ('loss_to_followup_contacted',
     'Participant lost to follow-up, contacted but did not come to study '
     'clinic'),
    ('caregiver_withdrew_consent',
     'Caregiver changed mind and withdrew consent'),
    ('father_refused',
     'Father of the infant/child/adolescent refused to participate and therefore'
     ' participant withdrew consent '),
    ('family_member_refused',
     'Other family member refused the study and therefore participant withdrew '
     'consent'),
    ('caregiver_hiv_infected',
     'Caregiver was found to be HIV-infected and the date of infection cannot '
     'be determined prior to the birth of their child'),
    ('infant_hiv_infected',
     'Infant/Child/Adolescent found to be HIV-infected'),
    ('infant_death',
     'Infant/Child/Adolescent death (complete Infant Death Report Form)'),
    ('protocol_completion',
     'Completion of protocol required period of time for observation '
     '(see Study Protocol for definition of "Completion") (skip to end of form)'),
    ('enrolled_erroneously',
     'Enrolled erroneously – did not meet eligibility criteria prior to consent'),
    ('in_eligible', 'Did not meet eligibility criteria, after consent obtained'),
    ('incarcerated',
     'Participant is incarcerated'),
    (OTHER, 'Other'),
)

CHILD_OFF_STUDY_REASON = (
    ('moving',
     'Participant stated she will be moving out of the study area or unable to'
     ' stay in study area'),
    ('ltfu', 'Participant lost to follow-up/ unable to locate'),
    ('lost_no_contact',
     'Participant lost to follow-up, contacted but did not come to study clinic'),
    ('child_withdrew', 'Child/Adolescent changed mind and withdrew consent'),
    ('withdrew_by_mother',
     'Mother of the infant/child/adolescent changed mind and withdrew consent'),
    ('withdrew_by_father',
     'Father of the infant/child/adolescent refused to participate and therefore'
     ' participant withdrew consent'),
    ('withdrew_by_family',
     'Other family member refused the study and therefore participant withdrew'
     ' consent '),
    ('hiv_pos', 'Infant/child/adolescent found to be HIV-infected'),
    ('death',
     ('Infant/child/adolescent Death (complete the Infant Death Report Form)')),
    ('complete',
     (' Completion of protocol required period of time for observation'
      ' (see Study Protocol for definition of Completion.)'
      ' [skip to end of form]')),
    ('enrolled_erroneously',
     'Enrolled erroneously – did not meet eligibility criteria prior to consent'),
    ('in_eligible', 'Did not meet eligibility criteria, after consent obtained'),
    ('incarcerated', 'Adolescent is incarcerated'),
    (OTHER, ' Other'),
)
