def test_get_organisations(client):
    response = client.get('/api/organisations')
    assert 200 == response.status_code
    #assert [{'id': 35, 'image': '/hse_logo.png', 'link': 'https://habr.com/ru/articles/321256/'}, {'id': 36, 'image': '/hse_logo.png', 'link': 'https://t.me/vyshkochka'}] == response.json
    assert [] == response.json