import unittest, json
from my_app.common.utils import get_message, send_message
from my_app.common.variables import ENCODING, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, RESPONSE


class TestSocket:
    def __init__(self, test_dict):
        self.testdict = test_dict

    # тестовая функция отправки, корретно  кодирует сообщение, так-же сохраняет что должно было отправлено в сокет.
    def send(self, message_to_send):
        json_test_message = json.dumps(self.testdict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.testdict)
        return json_test_message.encode(ENCODING)


class MyTestCase(unittest.TestCase):
    test_dict_send = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }
    test_dict_recv_ok = {RESPONSE: 200}
    test_dict_recv_err = {
        RESPONSE: 400
    }

    def test_send_message(self):
        # экземпляр тестового словаря, хранит собственно тестовый словарь
        test_socket = TestSocket(self.test_dict_send)
        # вызов тестируемой функции, результаты будут сохранены в тестовом сокете
        send_message(test_socket, self.test_dict_send)
        # проверка корретности кодирования словаря. сравниваем результат довренного кодирования и результат от тестируемой функции
        self.assertEqual(test_socket.encoded_message, test_socket.receved_message)
        # дополнительно, проверим генерацию исключения, при не словаре на входе.
        self.assertRaises(ValueError, send_message, test_socket, '999')
        self.assertRaises(ValueError, send_message, test_socket, {'ASD': 999})


if __name__ == '__main__':
    unittest.main()
