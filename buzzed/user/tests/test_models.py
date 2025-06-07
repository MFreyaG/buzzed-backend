from django.core.exceptions import ValidationError
from django.test import TestCase

from user.models import Contact, User


class ContactTestCase(TestCase):
    fixtures = ["users.json"]

    def test_create_multiple_contacts(self):
        user1 = User.objects.get(username="User1")
        user2 = User.objects.get(username="User2")
        user3 = User.objects.get(username="User3")
        user4 = User.objects.get(username="User4")

        Contact.objects.create(user1=user1, user2=user2)
        Contact.objects.create(user1=user1, user2=user3)
        Contact.objects.create(user1=user1, user2=user4)

        user1_contacts = Contact.objects.filter(user1=user1)
        self.assertEqual(len(user1_contacts), 3)

        for contact in user1_contacts:
            self.assertEqual(contact.user1.username, "User1")

    def test_create_invalid_contact(self):
        user1 = User.objects.get(username="User1")
        contact = Contact(user1=user1, user2=user1)

        with self.assertRaises(ValidationError):
            contact.full_clean()
