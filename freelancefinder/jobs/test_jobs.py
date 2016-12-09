
def test_job_list(client):
    response = client.get('/jobs/job-list/')
    assert response.status_code == 200


def test_post_list(client):
    response = client.get('/jobs/post-list/')
    assert response.status_code == 200
