
def test_homepage(client):
    response = client.get('/')
    assert b'Paul' in response.content
