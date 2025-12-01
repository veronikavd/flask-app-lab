import unittest
from app import create_app, db
from app.posts.models import Post
from datetime import datetime
from sqlalchemy import select

class PostTestCase(unittest.TestCase):
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = create_app('testing')
        self.app.config['WTF_CSRF_ENABLED'] = False 
        
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        """Очищення після кожного тесту"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_post(self):
        """Тест: Створення нового поста (US01)"""
        response = self.client.post('/post/create', data={
            'title': 'Test Post Title',
            'content': 'This is the content for the post.',
            'category': 'tech',
            'is_active': 'y',
            'publish_date': datetime.now().strftime('%Y-%m-%dT%H:%M')
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('успішно додано'.encode('utf-8'), response.data)
        
        post_stmt = select(Post).filter_by(title='Test Post Title')
        post = db.session.scalar(post_stmt)
        self.assertIsNotNone(post)

    def test_list_posts(self):
        """Тест: Відображення списку постів (US02)"""
        p = Post(title="Visible Post", content="Content", category="tech")
        db.session.add(p)
        db.session.commit()

        response = self.client.get('/post/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Visible Post", response.data)

    def test_update_post(self):
        """Тест: Редагування поста (US04)"""
        p = Post(title="Old Title", content="Old Content", category="tech")
        db.session.add(p)
        db.session.commit()

        response = self.client.post(f'/post/{p.id}/update', data={
            'title': 'Updated Title',
            'content': 'Updated Content',
            'category': 'news',
            'is_active': 'y',
            'publish_date': datetime.now().strftime('%Y-%m-%dT%H:%M')
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        
        updated_post = db.session.get(Post, p.id)
        self.assertEqual(updated_post.title, "Updated Title")

    def test_delete_post(self):
        """Тест: Видалення поста (US05)"""
        p = Post(title="To Delete", content="Bye", category="other")
        db.session.add(p)
        db.session.commit()

        response = self.client.post(f'/post/{p.id}/delete', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        post = db.session.get(Post, p.id)
        self.assertIsNone(post)

    def test_404_error(self):
        """Тест: Обробка помилки 404 (US06)"""
        response = self.client.get('/post/99999') 
        self.assertEqual(response.status_code, 404)

if __name__ == "__main__":
    unittest.main()