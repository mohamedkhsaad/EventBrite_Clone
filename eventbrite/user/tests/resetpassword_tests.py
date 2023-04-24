from ..models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

class CustomPasswordResetViewTest(TestCase):
    def test_password_reset(self):
        # Create a user for the test
        user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

        # Send a password reset request for the user's email address
        url = reverse('password_reset')
        data = {'email': 'testuser@example.com'}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('password_reset_done'))

        # Check that the password reset email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Password reset for your My App account')
        self.assertEqual(mail.outbox[0].to, [user.email])

        # Get the password reset URL from the email
        email_body = mail.outbox[0].body
        reset_url_start = email_body.index('http')
        reset_url_end = email_body.index('\n')
        reset_url = email_body[reset_url_start:reset_url_end]

        # Check that the reset URL is valid
        response = self.client.get(reset_url)
        self.assertEqual(response.status_code, 200)

        # Get the UID and token from the reset URL
        uid_start = reset_url.index('uidb64=') + 7
        uid_end = reset_url.index('&token=')
        uid = reset_url[uid_start:uid_end]
        token_start = reset_url.index('token=') + 6
        token_end = len(reset_url)
        token = reset_url[token_start:token_end]

        # Submit a new password for the user
        new_password = 'newtestpassword'
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        data = {'new_password1': new_password, 'new_password2': new_password}
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('password_reset_complete'))

        # Check that the user can log in with the new password
        self.assertTrue(self.client.login(username=user.username, password=new_password))
