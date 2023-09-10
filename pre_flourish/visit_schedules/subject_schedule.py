from edc_visit_schedule import SubjectSchedule


class PfSubjectSchedule(SubjectSchedule):
    """A class that puts a subject on to a schedule or takes a subject
    off of a schedule.

    This class is instantiated by the Schedule class.
    """

    registered_subject_model = 'pre_flourish.preflourishregisteredsubject'
