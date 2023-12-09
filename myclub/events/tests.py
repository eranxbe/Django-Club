from django.test import TestCase
from .models import ClubUser

# Create your tests here.
class UsersTests(TestCase):
    def setUp(self):
        ClubUser.objects.create(first_name='Geek', last_name='Automation', email='heyholetsgo@gmai.com')

    def test_user(self):
        user = ClubUser.objects.filter(first_name__contains="Geek").first()
        self.assertEqual(user.last_name, 'Automation')
       

