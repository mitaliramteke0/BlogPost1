

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import BlogPost, Comment
from .forms import BlogPostForm, CommentForm

class BloggingPlatformTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_blog_create(self):
        response = self.client.post(reverse('blog_create'), {
            'title': 'Test Blog Post',
            'content': 'This is a test blog post content.',
        })
        self.assertEqual(response.status_code, 302)  # add redirection after successful post creation

        # ADD blog post was created in the database
        self.assertEqual(BlogPost.objects.count(), 1)
        post = BlogPost.objects.first()
        self.assertEqual(post.title, 'Test Blog Post')
        self.assertEqual(post.content, 'This is a test blog post content.')
        self.assertEqual(post.author, self.user)

    def test_blog_edit(self):
        post = BlogPost.objects.create(title='Test Blog Post', content='Content', author=self.user)
        response = self.client.post(reverse('blog_edit', args=[post.pk]), {
            'title': 'Updated Blog Post',
            'content': 'This is an updated blog post content.',
        })
        self.assertEqual(response.status_code, 302)  # Assert redirection after successful post update

        # ADD the blog post was updated in the database
        updated_post = BlogPost.objects.get(pk=post.pk)
        self.assertEqual(updated_post.title, 'Updated Blog Post')
        self.assertEqual(updated_post.content, 'This is an updated blog post content.')

    def test_blog_delete(self):
        post = BlogPost.objects.create(title='Test Blog Post', content='Content', author=self.user)
        response = self.client.post(reverse('blog_delete', args=[post.pk]))
        self.assertEqual(response.status_code, 302)  # Assert redirection after successful post deletion

        # ADD blog post was deleted from the database
        self.assertEqual(BlogPost.objects.count(), 0)

    def test_blog_detail(self):
        post = BlogPost.objects.create(title='Test Blog Post', content='Content', author=self.user)
        response = self.client.get(reverse('blog_detail', args=[post.pk]))
        self.assertEqual(response.status_code, 200)  # Assert successful response

        # ADD the correct post and comments are displayed in the response context
        self.assertEqual(response.context['post'].title, 'Test Blog Post')
        self.assertEqual(response.context['post'].content, 'Content')
        self.assertEqual(response.context['comments'].count(), 0)  # Assuming no comments initially
