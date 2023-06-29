from fastapi.testclient import TestClient

from web.api import app
from web.checks import create_access_token

client = TestClient(app)


def test_registration_new_user():
    """
    Тест проверяет регистрацию нового пользователя
    """
    data = {'email': '1235@gmail.com',
            'password': '123',
            'phone': '375296171303'}
    response = client.post('/web/user/register', params=data)
    assert response.status_code == 200
    assert response.json()['created_user'] == "success"
    global user_id
    user_id = response.json()['id']


def test_get_user():
    """
    Тест проверяет выдачу конкретного юзера
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.get(f'/web/user/{user_id}', headers={"Authorization": f"Bearer {token}"})
    expected_keys = {'_id', 'username', 'first_name', 'id_telegram', 'gyms', 'records', 'person'}
    assert expected_keys == response.json().keys()
    assert response.status_code == 200


# def test_update_user():
#     """
#     Тест проверяет изменение пользователя
#     """
#     data = {
#         'user_id': user_id,
#         'name': 'ivan',
#         'secondname': 'pertov',
#         'phone': '123123123',
#         'age': '22'
#     }
#     token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
#     response = client.put('/web/user/update', params=data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()['message'] == 'Items updated successfully'
#

# def test_delete_user():
#     """
#     Тест проверяет удаление пользователя, закрыл тк для тестов нужен юзер
#     """
#     data = {'user_id': user_id}
#     token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
#     response = client.delete('/web/user/delete', params=data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()['delete'] == 'success'


# def test_delete_non_user_in_db():
#     """
#     Тест проверяет удаление из бд если пользователя нет в базе, запускаем если нету юзера в базе
#     """
#     data = {'user_id': user_id}
#     token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
#     response = client.delete('/web/user/delete', params=data, headers={"Authorization": f"Bearer {token}"})
#     assert response.status_code == 200
#     assert response.json()['delete'] == 'id not in db'


def test_get_users():
    """
    Тест проверяет вывод всех пользователей
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.get('/web/users/', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200


def test_login():
    """
    Тест проверяет авторизацию пользователей
    """
    data = {'email': '1235@gmail.com',
            'password': '123'}
    response = client.post('/web/login', params=data)
    expected_keys = {'access_token', 'refresh_token'}
    assert response.status_code == 200
    assert expected_keys == response.json().keys()


def test_login_failed():
    """
    Тест проверяет авторизацию пользователей если их нет в базу
    """
    data = {'email': '1235@gmail.com',
            'password': 'hello'}
    response = client.post('/web/login', params=data)
    assert response.status_code == 200
    assert response.json()['message'] == 'access invalid'


def test_refresh_token():
    """
    Тест проверяет выдачу ре фреш токена
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.post('/web/refresh', headers={"Authorization": f"Bearer {token}"})
    expected_keys = {'access_token', 'data'}
    assert expected_keys == response.json().keys()
    assert response.status_code == 200


def test_get_gyms():
    """
    Тест проверяет вывод всех залов
    """
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.get('/web/gyms', headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    gyms = response.json()
    assert isinstance(gyms, list)
    for gym in gyms:
        assert '_id' in gym
        assert 'title' in gym
        assert 'address' in gym
        assert 'trainers' in gym


def test_user_gyms():
    """
    Тест проверяет привязанные залы пользователя
    """
    data = {'user_id': user_id}
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.post('/web/user_gyms', params=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    gyms = response.json()
    for gym in gyms:
        assert 'users_gyms' in gym


def test_add_gym():
    """
    Тест проверяет привязанные залы пользователя
    """
    data = {'id_user': user_id,
            'id_gym': '642d6b231874a9bfa3f08250'}
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.post('/web/add_gym/', params=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['added_gyms'] == 'success added Gym1'


#
def test_delete_gym():
    """
    Тест удаляет привязанный зал пользователя
    """
    data = {'id_user': '649da5595f14f9134b27882b',
            'id_gym': '642d6b231874a9bfa3f08250'}
    token = create_access_token('artem', '6482fee1f3ff4b3b60ed4119', 'admin')
    response = client.delete('/web/delete_gym/', params=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()['delete'] == 'success'
