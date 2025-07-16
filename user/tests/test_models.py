from django.core.exceptions import ValidationError
from django.test import TestCase

from user.models import Contact, User


class ContactTestCase(TestCase):
    fixtures = ["addresses.json", "users.json"]

    def test_create_invalid_contact(self):
        follower = User.objects.get(pk="11111111-1111-4111-a111-000000000001")
        contact = Contact(follower=follower, followed=follower)

        with self.assertRaises(ValidationError):
            contact.full_clean()
