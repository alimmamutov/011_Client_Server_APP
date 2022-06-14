import unittest
from my_app.server import process_client_message
from my_app.common.variables import TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME, AUTH, PASSWORD, RESPONSE,ALERT, ERROR


class MyTestCase(unittest.TestCase):
    def test_presense_Guest(self):
        bad_resp = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        mes1 = {
            ACTION: PRESENCE,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        mes2 = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest',
            }
        }
        mes3 = {
            ACTION: AUTH,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest',
                PASSWORD: '123456'
            }
        }
        resp1 = process_client_message(mes1)
        resp2 = process_client_message(mes2)
        resp3 = process_client_message(mes3)
        # Правильный запрос
        self.assertEqual(resp1, bad_resp)
        # Правильный запрос
        self.assertEqual(resp2['response'], 200)
        # Специально вызываю ошибку авторизации
        self.assertEqual(resp3['response'], 200)


if __name__ == '__main__':
    unittest.main()
