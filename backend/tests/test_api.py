from fastapi.testclient import TestClient

def test_create_course(client: TestClient) -> None:
    pass

def test_get_dna(client: TestClient) -> None:
    # Testing the analysis DNA endpoint
    # Note: test DB is mocked or real, we expect 404 if course 999 is missing, or we mock it.
    response = client.get("/api/analysis/dna?course_id=999")
    assert response.status_code == 404

def test_get_predictions(client: TestClient) -> None:
    # Testing the new prediction endpoint for a non-existent subject
    response = client.get("/api/predictions/NonExistentSubject")
    assert response.status_code == 404
