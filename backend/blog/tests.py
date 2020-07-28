import datetime

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APITransactionTestCase

from .models import Post

User = get_user_model()


class UserCreateAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        test_user.save()

    def test_create_user(self):
        """
        Ensure we can create a new user.
        """
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(reverse('users-create'), data, format='json')

        self.assertEqual(User.objects.count(), 2)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

    def test_create_user_with_short_password(self):
        """
        Ensure user is not created for password lengths less than 8.
        """
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': 'foo'
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        """
        Ensure user is not created without password.
        """
        data = {
            'username': 'foobar',
            'email': 'foobarbaz@example.com',
            'password': ''
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_username(self):
        """
        Ensure user is not created without username.
        """
        data = {
            'username': '',
            'email': 'foobarbaz@example.com',
            'password': 'foobar'
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        """
        Ensure user is not created, when it already exists.
        """
        data = {
            'username': 'testuser',
            'email': 'user@example.com',
            'password': 'testuser'
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        """
        Ensure user is not created, when email already exists.
        """
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'testuser'
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_invalid_email(self):
        """
        Ensure user is not created without valid email.
        """
        data = {
            'username': 'foobarbaz',
            'email': 'testing',
            'password': 'foobarbaz'
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)

    def test_create_user_with_no_email(self):
        """
        Ensure user is not created without email.
        """
        data = {
            'username': 'foobar',
            'email': '',
            'password': 'foobarbaz'
        }

        response = self.client.post(reverse('users-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


class JWTAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        test_user.save()

    def test_jwt_workflow(self):
        """
        Ensure user can sign up and receive JSON Web Token.
        """

        # Signing up user
        data = {
            'username': 'foobar',
            'email': 'foobar@example.com',
            'password': 'somepassword'
        }

        response = self.client.post(reverse('users-create'), data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertFalse('password' in response.data)

        # Receive access and refresh tokens for user
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'foobar',
                'password': 'somepassword'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)


class PostsAPITest(APITransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUp(cls):
        test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        test_user.save()
        test_user2 = User.objects.create_user(
            'testuser2',
            'test2@example.com',
            'testpassword32'
        )
        test_user2.save()
        post1 = Post.objects.create(
            title='First post',
            owner=test_user,
            content='First ever created post!'
        )
        post1.save()
        post2 = Post.objects.create(
            title='Second post',
            owner=test_user,
            content='Another post.'
        )
        post2.save()

    def test_unauthorized_get_posts(self):
        """
        Ensure unauthorized user can see posts.
        """
        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        self.assertEqual(Post.objects.count(), 2)

    def test_unauthorized_create_post(self):
        """
        Ensure unauthorized user can't create post
        """
        response = self.client.post(
            reverse('posts-list'),
            data={
                'title': 'Test post',
                'content': 'Testing content things'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthorized_user_liked_post(self):
        """
        Ensure unauthorized user can't like post.
        """
        response = self.client.post(reverse('posts-detail', args='2') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('posts-detail', args='2'))
        self.assertEqual(response.data['total_likes'], 0)
        self.assertEqual(response.data['is_fan'], False)

    def test_unauthorized_user_unliked_post(self):
        """
        Ensure unauthorized user can't unlike post.
        """
        response = self.client.post(reverse('posts-detail', args='2') + 'unlike/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(reverse('posts-detail', args='2'))
        self.assertEqual(response.data['total_likes'], 0)
        self.assertEqual(response.data['is_fan'], False)

    def test_unauthorized_user_can_see_post_fans(self):
        """
        Ensure unauthorized user can see who liked post.
        """
        response = self.client.get(reverse('posts-detail', args='2') + 'fans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_authorized_get_posts(self):
        """
        Ensure authorized user can see posts.
        """
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'testuser',
                'password': 'testpassword'
            },
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.get(reverse('posts-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_authorized_create_post(self):
        """
        Ensure authorized user can create post.
        """
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'testuser',
                'password': 'testpassword'
            },
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(
            reverse('posts-list'),
            data={
                'title': 'Test post',
                'content': 'Testing content things'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authorized_update_post(self):
        """
        Ensure authorized user can create post and update it
        """
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'testuser',
                'password': 'testpassword'
            },
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(
            reverse('posts-list'),
            data={
                'title': 'Test post',
                'content': 'Testing content things'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.put(
            reverse('posts-detail', args='3'),
            data={
                'title': 'Test post +1',
                'content': 'New'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test post +1')
        self.assertEqual(response.data['content'], 'New')
        self.assertEqual(response.data['owner'], 'testuser')

    def test_authorized_partial_update_post(self):
        """
        Ensure authorized user can create post and partially update it
        """
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'testuser',
                'password': 'testpassword'
            },
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(
            reverse('posts-list'),
            data={
                'title': 'Test post',
                'content': 'Testing content things'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.patch(
            reverse('posts-detail', args='3'),
            data={
                'content': 'New'
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test post')
        self.assertEqual(response.data['content'], 'New')
        self.assertEqual(response.data['owner'], 'testuser')

    def test_authorized_delete_post(self):
        """
        Ensure authorized user can create post and delete it
        """
        response = self.client.post(
            reverse('token_obtain_pair'), {'username': 'testuser', 'password': 'testpassword'}, format='json'
        )

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(
            reverse('posts-list'),
            data={
                'title': 'Test post',
                'content': 'Testing content things'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.delete(reverse('posts-detail', args='3'))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_authorized_user_liked_post(self):
        """
        Ensure authorized user can like post.
        """
        response = self.client.post(
            reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpassword32'}, format='json'
        )

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(reverse('posts-detail', args='2') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('posts-detail', args='2'))
        self.assertEqual(response.data['total_likes'], 1)
        self.assertEqual(response.data['is_fan'], True)

    def test_authorized_user_unliked_post(self):
        """
        Ensure authorized user can unlike previously liked post.
        """
        response = self.client.post(
            reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpassword32'}, format='json'
        )

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(reverse('posts-detail', args='2') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('posts-detail', args='2'))
        self.assertEqual(response.data['total_likes'], 1)
        self.assertEqual(response.data['is_fan'], True)

        response = self.client.post(reverse('posts-detail', args='2') + 'unlike/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('posts-detail', args='2'))
        self.assertEqual(response.data['total_likes'], 0)
        self.assertEqual(response.data['is_fan'], False)

    def test_authorized_user_can_see_post_fans(self):
        """
        Ensure authorized user can see who liked post.
        """
        response = self.client.post(
            reverse('token_obtain_pair'), {'username': 'testuser2', 'password': 'testpassword32'}, format='json'
        )

        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.get(reverse('posts-detail', args='2') + 'fans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        response = self.client.post(reverse('posts-detail', args='2') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('posts-detail', args='2') + 'fans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AnalyticsAPITest(APITestCase):
    @classmethod
    def setUp(cls):
        test_user = User.objects.create_user(
            'testuser',
            'test@example.com',
            'testpassword'
        )
        test_user.save()
        test_user2 = User.objects.create_user(
            'testuser2',
            'test2@example.com',
            'testpassword32'
        )
        test_user2.save()

    def test_analytics_workflow_for_no_likes(self):
        """
        Ensure analytics endpoint return nothing if data don't provided.
        """
        response = self.client.get(reverse('analytics'), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue('status' in response.data)
        self.assertEqual(response.data['status'], 'There is no data available for know.')

    def test_analytics_workflow_for_likes(self):
        """
        Ensure analytics endpoint return data.
        """

        # First user create post id=1 and post id=2
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'testuser',
                'password': 'testpassword'
            },
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(
            reverse('posts-list'),
            data={'title': 'Test post', 'content': 'Testing content things'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            reverse('posts-list'),
            data={'title': 'Test post 2', 'content': 'Another testing content.'},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # First user like post id=2
        response = self.client.post(reverse('posts-detail', args='2') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Second user like posts id=1 and id=2
        response = self.client.post(
            reverse('token_obtain_pair'),
            data={
                'username': 'testuser2',
                'password': 'testpassword32'
            },
            format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        response = self.client.post(reverse('posts-detail', args='1') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(reverse('posts-detail', args='2') + 'like/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check analytics
        response = self.client.get(reverse('analytics'), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['date'], datetime.date.today())
        self.assertEqual(response.data[0]['total_likes'], 3)
