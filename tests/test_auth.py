import unittest
from app import create_app, db, bcrypt
from app.models import User

class AuthTestCase(unittest.TestCase):
    
    def setUp(self):
        """Налаштування перед кожним тестом"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False # Вимикаємо CSRF для тестів
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # БД в оперативній пам'яті
        
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        db.create_all()

    def tearDown(self):
        """Очищення після кожного тесту"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_page_loads(self):
        """Перевірка: сторінка реєстрації завантажується"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        # Шукаємо слово "Реєстрація" (у заголовку або кнопці)
        self.assertIn('Реєстрація'.encode('utf-8'), response.data)

    def test_login_page_loads(self):
        """Перевірка: сторінка входу завантажується"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        # Шукаємо слово "Вхід" (у заголовку h2 "Вхід до системи")
        self.assertIn('Вхід'.encode('utf-8'), response.data)

    def test_user_registration(self):
        """Перевірка: користувач успішно реєструється та зберігається в БД"""
        response = self.client.post('/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)
        
        # Перевіряємо, чи зберігся користувач у базі даних
        user = db.session.execute(db.select(User).filter_by(email='test@example.com')).scalar_one_or_none()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_user_login_logout(self):
        """Перевірка: користувач може увійти та вийти"""
        
        # 1. Створюємо користувача вручну
        hashed_pw = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(username='loginuser', email='login@test.com', password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        # 2. Виконуємо вхід
        response = self.client.post('/login', data={
            'email': 'login@test.com',
            'password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        # Перевіряємо, що ми на сторінці профілю (шукаємо "Профіль")
        self.assertIn('Профіль'.encode('utf-8'), response.data)

        # 3. Виконуємо вихід
        response = self.client.get('/logout', follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)
        # Перевіряємо повідомлення про успішний вихід
        self.assertIn('Ви вийшли із системи'.encode('utf-8'), response.data)

if __name__ == '__main__':
    unittest.main()