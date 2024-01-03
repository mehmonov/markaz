from django.test import TestCase
from django.urls import reverse
from home.models import Applicant
from django.contrib.auth.models import User

class NewApplicantTest(TestCase):
    def setUp(self):
        # Create a test user and log in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

    def test_valid_form_submission(self):
        url = reverse('newApplicant')
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'birth_place': 'Tashkent',
            'preferred_time': 'morning',
            'course': 1,
            'preferred_days_of_week': ['monday', 'wednesday'],
            'phone_number': '+998901234567',
            'phone_number2': '+998909876543'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Applicant.objects.count(), 1)
        applicant = Applicant.objects.first()
        self.assertEqual(applicant.first_name, 'Test')
        self.assertEqual(applicant.last_name, 'User')
