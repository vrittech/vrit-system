# from django.test import TestCase
# from django.utils import timezone
# from accounts.models import CustomUser
# from .models import Blog, BlogTags, BlogCategory

# class BlogModelTest(TestCase):
    
#     def setUp(self):
#         # Create a test user
#         self.user = CustomUser.objects.create_user(username='testuser', password='password')
        
#         # Create a BlogCategory
#         self.category = BlogCategory.objects.create(name='Test Category')
        
#         # Create BlogTags
#         self.tag1 = BlogTags.objects.create(name='Django')
#         self.tag2 = BlogTags.objects.create(name='Python')
        
#     def test_blog_creation(self):
#         # Create a Blog instance
#         blog = Blog.objects.create(
#             user=self.user,
#             title='Test Blog Post',
#             description='This is a test blog description.',
#             site_title='Test Site Title',
#             excerpt='This is an excerpt of the test blog.',
#             is_publish=True,
#             meta_description='Test meta description.',
#             meta_keywords='django, python, test',
#             meta_author='Test Author',
#             category=self.category
#         )
#         # Add tags to the blog
#         blog.tags.set([self.tag1, self.tag2])
        
#         # Verify the blog was created correctly
#         self.assertEqual(blog.title, 'Test Blog Post')
#         self.assertEqual(blog.description, 'This is a test blog description.')
#         self.assertEqual(blog.site_title, 'Test Site Title')
#         self.assertTrue(blog.is_publish)
#         self.assertEqual(blog.meta_author, 'Test Author')
#         self.assertEqual(blog.category.name, 'Test Category')
#         self.assertEqual(blog.tags.count(), 2)
#         self.assertIn(self.tag1, blog.tags.all())
#         self.assertIn(self.tag2, blog.tags.all())
        
#     def test_blog_auto_timestamps(self):
#         # Create a Blog instance
#         blog = Blog.objects.create(
#             user=self.user,
#             title='Test Blog with Timestamps',
#             description='This is a test blog description with timestamps.',
#             site_title='Test Site Title',
#             excerpt='This is an excerpt of the test blog.',
#             is_publish=True,
#             meta_description='Test meta description.',
#             meta_keywords='django, python, timestamps',
#             meta_author='Test Author',
#             category=self.category
#         )
        
#         # Check if `created_at` and `updated_at` are set correctly
#         self.assertIsNotNone(blog.created_at)
#         self.assertIsNotNone(blog.updated_at)
#         self.assertAlmostEqual(blog.created_at, timezone.now(), delta=timezone.timedelta(seconds=1))
#         self.assertAlmostEqual(blog.updated_at, timezone.now(), delta=timezone.timedelta(seconds=1))
        
#     def test_blog_str_method(self):
#         # Create a Blog instance
#         blog = Blog.objects.create(
#             user=self.user,
#             title='String Method Test Blog',
#             description='This is a test blog description.',
#             site_title='Test Site Title',
#             excerpt='This is an excerpt of the test blog.',
#             is_publish=True,
#             meta_description='Test meta description.',
#             meta_keywords='django, python, string method',
#             meta_author='Test Author',
#             category=self.category
#         )
#         # Verify the `__str__` method of the Blog model (if implemented)
#         self.assertEqual(str(blog), blog.title)

#     def test_blog_tags_relationship(self):
#         # Create a Blog instance
#         blog = Blog.objects.create(
#             user=self.user,
#             title='Blog with Tags',
#             description='This is a blog to test tag relationships.',
#             site_title='Test Site Title',
#             excerpt='This is an excerpt of the test blog.',
#             is_publish=True,
#             meta_description='Test meta description.',
#             meta_keywords='django, python, test tags',
#             meta_author='Test Author',
#             category=self.category
#         )
        
#         # Add tags
#         blog.tags.set([self.tag1, self.tag2])
        
#         # Verify that the tags are related to the blog
#         self.assertEqual(blog.tags.count(), 2)
#         self.assertIn(self.tag1, blog.tags.all())
#         self.assertIn(self.tag2, blog.tags.all())

#     def test_blog_category_relationship(self):
#         # Create a Blog instance with category
#         blog = Blog.objects.create(
#             user=self.user,
#             title='Blog with Category',
#             description='This is a blog to test category relationships.',
#             site_title='Test Site Title',
#             excerpt='This is an excerpt of the test blog.',
#             is_publish=True,
#             meta_description='Test meta description.',
#             meta_keywords='django, python, test category',
#             meta_author='Test Author',
#             category=self.category
#         )
        
#         # Verify that the category is set correctly
#         self.assertEqual(blog.category.name, 'Test Category')
