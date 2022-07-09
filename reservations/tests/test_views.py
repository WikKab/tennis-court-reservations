from django.test import RequestFactory, TestCase

from reservations.models import TennisCourt
from reservations.views import CreateExactCourtReservation

class TestViews(TestCase):

    def test_cost_without_rent(self):
        request = RequestFactory().get('/')
        view = CreateExactCourtReservation()
        view.setup(request)
        self.court = TennisCourt(hire_price=100, equipment_rent=False)
        reservation_start = '16:00'
        reservation_end = '18:00'

        expected = 400

        result = view._calculate_cost(reservation_start, reservation_end, self.court, False)

        self.assertEquals(result, expected)

    def test_cost_with_rent(self):
        request = RequestFactory().get('/')
        view = CreateExactCourtReservation()
        view.setup(request)
        self.court = TennisCourt(hire_price=100, equipment_cost=20, equipment_rent=True)
        reservation_start = '16:00'
        reservation_end = '18:00'

        expected = 420

        result = view._calculate_cost(reservation_start, reservation_end, self.court, True)

        self.assertEquals(result, expected)


