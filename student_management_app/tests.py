from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from .models import CustomUser

class AddStaffTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.add_staff_url = reverse('add_staff')
        # Asegúrate de ajustar los siguientes valores a los que necesitas para tu prueba
        self.username = "Jamdevpy"
        self.password = "root198735"
        self.email = "jamreyes26@gmail.com"
        self.first_name = "Jose"
        self.last_name = "Molina"
        self.address = "Test Address"
    
    def test_add_staff_get_request(self):
        # Prueba enviar un GET en lugar de POST
        response = self.client.get(self.add_staff_url)
        self.assertEqual(response.status_code, 200)
    
    def test_add_staff_post_request_with_valid_data(self):
        # Prueba enviar un POST con datos válidos
        response = self.client.post(self.add_staff_url, {
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'address': self.address
        })
        self.assertEqual(response.status_code, 302) # Redirecciona si tiene éxito
        self.assertTrue(CustomUser.objects.filter(username=self.username).exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Successfully Added Staff")
    
    def test_add_staff_post_request_with_invalid_data(self):
        # Prueba enviar un POST con datos inválidos
        response = self.client.post(self.add_staff_url, {})
        self.assertEqual(response.status_code, 302) # Asumiendo que redirecciona de todas formas
        self.assertFalse(CustomUser.objects.filter(username="baduser").exists())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Failed to Add Staff")
