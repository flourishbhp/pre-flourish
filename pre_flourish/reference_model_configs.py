from edc_reference import site_reference_configs

site_reference_configs.register_from_visit_schedule(
    visit_models={
        'edc_appointment.appointment': ['pre_flourish.preflourishvisit'],
        'flourish_child.appointment': ['flourish_child.childvisit'],
        'pre_flourish.appointment': ['pre_flourish.preflourishvisit'],
    })
