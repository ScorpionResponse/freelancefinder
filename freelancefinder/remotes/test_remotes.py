
def test_source_list(client):
    response = client.get('/remotes/source-list/')
    assert response.status_code == 200
