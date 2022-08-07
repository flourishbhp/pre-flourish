from django.test import TestCase, tag
from django.conf import settings
from django.shortcuts import reverse
from edc_constants.constants import NO, YES
from pre_flourish.models.caregiver.eligibility import Eligibility

@tag('eligible')
class TestEligibility(TestCase):
    def test_participant_age_ineligible(self):
        eligibility =  Eligibility(
            age_in_years=16, 
            has_omang=YES, 
            has_child=YES, 
            remain_in_study=YES)
        
        self.assertFalse(eligibility.is_eligible)
    
    def test_participant_no_omang_ineligible(self):
        eligibility =  Eligibility(
            age_in_years=20, 
            has_omang=NO, 
            has_child=YES, 
            remain_in_study=YES)
        
        self.assertFalse(eligibility.is_eligible)
        
    def test_participant_no_omang_ineligible(self):
        eligibility =  Eligibility(
            age_in_years=20, 
            has_omang=YES, 
            has_child=NO, 
            remain_in_study=YES)
        
        self.assertFalse(eligibility.is_eligible)
        
    def test_participant_no_omang_ineligible(self):
        eligibility =  Eligibility(
            age_in_years=20, 
            has_omang=YES, 
            has_child=NO, 
            remain_in_study=YES)
        
        self.assertFalse(eligibility.is_eligible)
        

