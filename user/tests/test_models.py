from django.core.exceptions import ValidationError
from django.test import TestCase

from user.models import Contact, User


class ContactTestCase(TestCase):
    fixtures = ["addresses.json", "users.json"]

    def test_create_multiple_contacts(self):
        user1 = User.objects.get(pk="11111111-1111-4111-a111-000000000001")
        user2 = User.objects.get(pk="22222222-2222-4222-a222-000000000002")
        user3 = User.objects.get(pk="33333333-3333-4333-a333-000000000003")
        user4 = User.objects.get(pk="44444444-4444-4444-a444-000000000004")

        Contact.objects.create(user1=user1, user2=user2)
        Contact.objects.create(user1=user1, user2=user3)
        Contact.objects.create(user1=user1, user2=user4)

        user1_contacts = Contact.objects.filter(user1=user1)
        self.assertEqual(len(user1_contacts), 3)

        for contact in user1_contacts:
            self.assertEqual(contact.user1.pk, user1.pk)

    def test_create_invalid_contact(self):
        user1 = User.objects.get(pk="11111111-1111-4111-a111-000000000001")
        contact = Contact(user1=user1, user2=user1)

        with self.assertRaises(ValidationError):
            contact.full_clean()
