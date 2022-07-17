from django.test import TestCase

from reservations.forms import hour_range, hour_range_model_form


class TestForms(TestCase):

    def test_hour_range_no_minutes(self):
        start_hour = '16:00:00'
        end_hour = '18:00:00'

        expected = [
            ('16:00', '16:00'),
            ('16:30', '16:30'),
            ('17:00', '17:00'),
            ('17:30', '17:30'),
            ('18:00', '18:00'),
        ]
        result = hour_range(start_hour, end_hour)

        self.assertEquals(result, expected)


    def test_hour_range_with_minutes(self):
        start_hour = '16:30:00'
        end_hour = '18:30:00'

        expected = [
            ('16:30', '16:30'),
            ('17:00', '17:00'),
            ('17:30', '17:30'),
            ('18:00', '18:00'),
            ('18:30', '18:30'),
        ]
        result = hour_range(start_hour, end_hour)

        self.assertEquals(result, expected)


    def test_hour_range_model_form_with_minutes(self):
        start_hour = '16:30:00'
        end_hour = '18:30:00'

        expected = [
            ('16.30', '16.30'),
            ('17.00', '17.00'),
            ('17.30', '17.30'),
            ('18.00', '18.00'),
            ('18.30', '18.30'),
        ]
        result = hour_range_model_form(start_hour, end_hour)

        self.assertEquals(result, expected)

