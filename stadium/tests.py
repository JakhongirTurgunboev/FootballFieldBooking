from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from account.models import CustomUser
from .models import FootballField, FootballFieldImages, Booking

class FootballFieldModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.football_field_data = {
            'name': 'Field 1',
            'address': 'Test Address',
            'contact': '1234567890',
            'price_per_hour': 20.00,
            'owner': self.user,
            'latitude': 12.34,
            'longitude': 56.78,
        }

    def test_create_football_field(self):
        football_field = FootballField.objects.create(**self.football_field_data)

        self.assertEqual(football_field.name, self.football_field_data['name'])
        self.assertEqual(football_field.address, self.football_field_data['address'])
        self.assertEqual(football_field.contact, self.football_field_data['contact'])
        self.assertEqual(football_field.price_per_hour, self.football_field_data['price_per_hour'])
        self.assertEqual(football_field.owner, self.football_field_data['owner'])
        self.assertEqual(football_field.latitude, self.football_field_data['latitude'])
        self.assertEqual(football_field.longitude, self.football_field_data['longitude'])

    def test_create_football_field_images(self):
        football_field = FootballField.objects.create(**self.football_field_data)
        image_data = {'image': 'path/to/image.jpg'}
        football_field_image = FootballFieldImages.objects.create(football_field=football_field, **image_data)

        self.assertEqual(football_field_image.football_field, football_field)
        self.assertEqual(str(football_field_image), str(football_field))

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')
        self.football_field = FootballField.objects.create(
            name='Field 1',
            address='Test Address',
            contact='1234567890',
            price_per_hour=20.00,
            owner=self.user,
            latitude=12.34,
            longitude=56.78,
        )
        self.booking_data = {
            'user': self.user,
            'football_field': self.football_field,
            'booking_start_time': timezone.now() + timedelta(days=1),
            'booking_duration_in_hours': 2,
        }

    def test_create_booking(self):
        booking = Booking.objects.create(**self.booking_data)

        self.assertEqual(booking.user, self.booking_data['user'])
        self.assertEqual(booking.football_field, self.booking_data['football_field'])
        self.assertEqual(booking.booking_start_time, self.booking_data['booking_start_time'])
        self.assertEqual(booking.booking_duration_in_hours, self.booking_data['booking_duration_in_hours'])

    def test_booking_clean_method(self):
        Booking.objects.create(
            user=self.user,
            football_field=self.football_field,
            booking_start_time=timezone.now() + timedelta(days=1),
            booking_duration_in_hours=2,
        )

        # Attempt to create another booking that intersects with the existing one
        with self.assertRaises(ValidationError):
            Booking.objects.create(
                user=self.user,
                football_field=self.football_field,
                booking_start_time=timezone.now() + timedelta(days=1, hours=1),
                booking_duration_in_hours=2,
            )
