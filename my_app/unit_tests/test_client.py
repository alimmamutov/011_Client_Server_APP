
import unittest
from my_app.client import create_presence, create_auth, process_ans
from my_app.common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, AUTH, PASSWORD, RESPONSE,ALERT


# Класс с тестами
class TestClass(unittest.TestCase):
    def test_presense_Guest(self):
        test = create_presence('Guest')
        test[TIME] = 1.1  # время необходимо приравнять принудительно иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_presense_User1(self):
        test = create_presence('User1')
        test[TIME] = 1.1  # время необходимо приравнять принудительно иначе тест никогда не будет пройден
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_auth_guest(self):
        test = create_auth('Guest','123456')
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: AUTH, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest', PASSWORD: '123456'}})

    def test_auth_user1(self):
        test = create_auth('Guest', '123456')
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: AUTH, TIME: 1.1, USER: {ACCOUNT_NAME: 'User1', PASSWORD: '123456'}})

    # Исключение где нет поля RESPONSE
    def test_ans_without_resp(self):
        self.assertRaises(ValueError, process_ans, {'not_response': '...'})

    # Корректная работа запроса
    def test_200_ans(self):
        self.assertRaises(ValueError, process_ans, {RESPONSE: 200})


if __name__ == '__main__':
    unittest.main()