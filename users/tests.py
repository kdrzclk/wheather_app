from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserViewTest(TestCase):

    def test_list_users(self):

        url = reverse('users')
        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.admin_token = Token.objects.create(user=self.admin_user)
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response_data), 2)
        
        self.assertIn('email', response_data[0])
        self.assertIn('first_name', response_data[0])
        self.assertIn('last_name', response_data[0])
        self.assertIn('id', response_data[0])

    def test_not_admin_list_users(self):
        
        url = reverse('users')
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
    
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):

        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.admin_token = Token.objects.create(user=self.admin_user)

        data = {
            "email": "test9@mail.com",
            "first_name": "Test11",
            "last_name": "User",
            "password": "Tt123456",
            "password2": "Tt123456"
            }
        url = reverse('users')
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        
        self.assertIn('email', response.data)
        self.assertIn('first_name', response.data)
        self.assertIn('last_name', response.data)
        self.assertIn('id', response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.get(email='test9@mail.com').email, 'test9@mail.com')
        self.assertEqual(User.objects.get(email='test9@mail.com').first_name, 'Test11')
        self.assertEqual(User.objects.get(email='test9@mail.com').last_name, 'User')

    def test_not_admin_create_user(self):

        url = reverse('users')
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        data = {
            "email": "test9@mail.com",
            "first_name": "Test11",
            "last_name": "User",
            "password": "Tt123456",
            "password2": "Tt123456"
            }
        response = self.client.post(url, data, HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_invalid_user_create(self):
        
        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.admin_token = Token.objects.create(user=self.admin_user)

        invalid_data = {
            "user": "",
            "first_name": "Test11",
            "last_name": "User",
            "password": "Tt123456",
            "password2": "Tt123456"
            }
        url = reverse('users')
        response = self.client.post(url, invalid_data, HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UserViewRUDTest(TestCase):
    
    def test_list_one_user(self):

        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.admin_token = Token.objects.create(user=self.admin_user)
        url = reverse('userdetail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + self.admin_token.key)
        response_data = response.json()
        self.assertEqual(response.status_code, 200)
        
        self.assertIn('email', response_data)
        self.assertIn('first_name', response_data)
        self.assertIn('last_name', response_data)
        self.assertIn('id', response_data)

        self.assertEqual(User.objects.get(email='test2@mail.com').email, 'test2@mail.com')
        self.assertEqual(User.objects.get(email='test2@mail.com').first_name, 'Test1')
        self.assertEqual(User.objects.get(email='test2@mail.com').last_name, 'User')


    def test_not_admin_and_self_list_one_user(self):

        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        url = reverse('userdetail', kwargs={'pk': self.user.pk})
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + 'asdasdasd')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user(self):

        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.admin_token = Token.objects.create(user=self.admin_user)
        url = reverse('userdetail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, {'first_name':'Test1 Update'}, HTTP_AUTHORIZATION='Token ' + self.admin_token.key, content_type='application/json')
        self.user.refresh_from_db()
        response_data = response.json()
        self.assertEqual(response.status_code, 200)

        self.assertIn('email', response_data)
        self.assertIn('first_name', response_data)
        self.assertIn('last_name', response_data)
        self.assertIn('id', response_data)

        self.assertEqual(User.objects.get(email='test2@mail.com').email, 'test2@mail.com')
        self.assertEqual(User.objects.get(email='test2@mail.com').first_name, 'Test1 Update')
        self.assertEqual(User.objects.get(email='test2@mail.com').last_name, 'User')

    def test_not_admin_and_self_update_user(self):

        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        url = reverse('userdetail', kwargs={'pk': self.user.pk})
        response = self.client.patch(url, {'first_name':'Test1 Update'}, HTTP_AUTHORIZATION='Token ' + 'sasdd44asdas2fdas5', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):

        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        url = reverse('userdetail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + self.user_token.key, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(pk=self.user.pk).exists())

    def test_not_admin_and_self_delete_user(self):

        self.admin_user = User.objects.create_superuser(email='admin@mail.com', 
                                              password='Tt123456',
                                              first_name='Admin',
                                              last_name="User")
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        url = reverse('userdetail', kwargs={'pk': self.user.pk})
        response = self.client.delete(url, HTTP_AUTHORIZATION='Token ' + 'sadmkasmdasd45a1asd', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RegisterViewTest(TestCase):

    def test_addnewuser(self):
        data = {
            "email": "test9@mail.com",
            "first_name": "Test11",
            "last_name": "User",
            "password": "Tt123456",
            "password2": "Tt123456"
            }

        url = reverse('addnewuser')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        response_data = response.json()

        self.assertIn('token', response_data)
        self.assertIn('first_name', response_data)
        self.assertIn('last_name', response_data)
        self.assertIn('email', response_data)

        self.assertEqual(response_data['email'], data['email'])
        self.assertEqual(response_data['first_name'], data['first_name'])
        self.assertEqual(response_data['last_name'], data['last_name'])

    def test_invalid_addnewuser(self):

        data = {
            "email": "",
            "first_name": "Test11",
            "last_name": "User",
            "password": "Tt123456",
            "password2": "Tt123456"
            }

        url = reverse('addnewuser')
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CustomAuthTokenTest(TestCase):

    def test_successful_login(self):

        self.user = User.objects.create_user(email='test@mail.com', 
                                              password='Tt123456',
                                              first_name='Test',
                                              last_name="User")
        data = {
            "username" : "test@mail.com",
            "password" : "Tt123456"
            }
        url = reverse('login')
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('token', response.data)
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_unsuccessful_login(self):

        self.user = User.objects.create_user(email='test@mail.com', 
                                              password='Tt123456',
                                              first_name='Test',
                                              last_name="User")
        data = {
            "username" : "test@mail.com",
            "password" : "Tt1234567"
            }
        url = reverse('login')
        response = self.client.post(url, data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['non_field_errors'], ['Unable to log in with provided credentials.'])

class LogoutViewTest(TestCase):

    def test_successful_logout(self):

        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        url = reverse("logout")
        response = self.client.get(url, HTTP_AUTHORIZATION='Token ' + self.user_token.key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Successfully logged out..."})

    def test_unsuccessful_logout(self):

        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        url = reverse("logout")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"message": "No active session found."})

class ResetPasswordTest(TestCase):

    def test_reset_password(self):

        self.user = User.objects.create_user(email='kadir.ozcelik16@gmail.com', 
                                              password='Tt123456',
                                              first_name='Kadir',
                                              last_name="Özçelik")
        url = reverse("resetpassword")
        response = self.client.post(url, {"email" : self.user.email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Your Password Reset Succesfully"})

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [self.user.email])
        self.assertIn("Your New Password is", mail.outbox[0].body)

        self.user.refresh_from_db()
        new_password = mail.outbox[0].body.split("Your New Password is ")[1]
        print(new_password)
        self.assertTrue(self.user.check_password(new_password))

    def test_reset_password_no_email(self):
        self.user = User.objects.create_user(email='kadir.ozcelik16@gmail.com', 
                                              password='Tt123456',
                                              first_name='Kadir',
                                              last_name="Özçelik")
        url = reverse("resetpassword")
        response = self.client.post(url, {"email" : "kadir@gmail.com"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'No such email address exists')

class ChangePasswordViewTest(TestCase):

    def test_change_password(self):
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        data = {
            'old_password': 'Tt123456',
            'new_password': 'Tt456789'
        }
        url = reverse("changepassword")
        response = self.client.put(url, data, HTTP_AUTHORIZATION='Token ' + self.user_token.key, content_type='application/json')
        self.user.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Your password successfully changed.')
        self.assertFalse(self.user.check_password('old_password'))
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_change_password_wrong_old_password(self):
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        data = {
            'old_password': 'Tt1234567',
            'new_password': 'Tt456789'
        }
        url = reverse("changepassword")
        response = self.client.put(url, data, HTTP_AUTHORIZATION='Token ' + self.user_token.key, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['old_password'], 'Wrong password.')

    def test_change_password_invalid_data(self):
        self.user = User.objects.create_user(email='test2@mail.com', 
                                              password='Tt123456',
                                              first_name='Test1',
                                              last_name="User")
        self.user_token = Token.objects.create(user=self.user)
        data = {
            'old_password': 'Tt1234567',
            'new_password': ''
        }
        url = reverse("changepassword")
        response = self.client.put(url, data, HTTP_AUTHORIZATION='Token ' + self.user_token.key, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('new_password', response.data)
        
    
