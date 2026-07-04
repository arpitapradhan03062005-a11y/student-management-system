from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from .models import Student


class AuthTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_login_with_correct_credentials(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertRedirects(response, reverse("home"))

    def test_login_with_wrong_credentials_shows_error(self):
        response = self.client.post(reverse("login"), {
            "username": "testuser",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid username or password")


class StudentCRUDTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.client.login(username="testuser", password="testpass123")

        self.student = Student.objects.create(
            roll_number="R001",
            name="Test Student",
            email="test.student@example.com",
            phone="9876543210",
            gender="Male",
            department="Computer Engineering",
            semester="1",
            date_of_birth=date(2000, 1, 1),
            address="123 Test Street",
        )

    def test_add_student(self):
        response = self.client.post(reverse("add_student"), {
            "roll_number": "R002",
            "name": "New Student",
            "email": "new.student@example.com",
            "phone": "9876543211",
            "gender": "Female",
            "department": "Information Technology",
            "semester": "2",
            "date_of_birth": "2001-05-15",
            "address": "456 Test Avenue",
        })
        self.assertRedirects(response, reverse("view_student"))
        self.assertTrue(Student.objects.filter(roll_number="R002").exists())

    def test_view_student_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse("view_student"))
        self.assertNotEqual(response.status_code, 200)  # should redirect to login

    def test_update_student(self):
        response = self.client.post(
            reverse("update_student", args=[self.student.id]),
            {
                "roll_number": "R001",
                "name": "Updated Name",
                "email": "test.student@example.com",
                "phone": "9876543299",
                "gender": "Male",
                "department": "Computer Engineering",
                "semester": "1",
                "date_of_birth": "2000-01-01",
                "address": "123 Test Street",
            }
        )
        self.assertRedirects(response, reverse("view_student"))
        self.student.refresh_from_db()
        self.assertEqual(self.student.name, "Updated Name")
        self.assertEqual(self.student.phone, "9876543299")

    def test_delete_student(self):
        response = self.client.post(reverse("delete_student", args=[self.student.id]))
        self.assertRedirects(response, reverse("view_student"))
        self.assertFalse(Student.objects.filter(id=self.student.id).exists())


class SecurityTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass123")
        self.student = Student.objects.create(
            roll_number="R001",
            name="Test Student",
            email="test.student@example.com",
            phone="9876543210",
            gender="Male",
            department="Computer Engineering",
            semester="1",
            date_of_birth=date(2000, 1, 1),
            address="123 Test Street",
        )

    def test_id_card_requires_login(self):
        """Anonymous users should NOT be able to download ID cards."""
        response = self.client.get(reverse("student_id_card", args=[self.student.id]))
        self.assertNotEqual(response.status_code, 200)

    def test_id_card_accessible_when_logged_in(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("student_id_card", args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")