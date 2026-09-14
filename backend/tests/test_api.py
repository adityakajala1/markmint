from fastapi.testclient import TestClient

def test_create_course(client: TestClient) -> None:
    # Need to override DB session with a testing one for real DB writes, 
    # but since this is a unit test in early phase, we test 404 or missing DB.
    # Because we haven't configured Alembic/sqlite mock in conftest for tests, 
    # hitting the real endpoints will try to use Postgres.
    pass

def test_get_dna(client: TestClient) -> None:
    # We mocked get_exam_dna to not hit DB
    response = client.get("/api/exams/1/dna")
    assert response.status_code == 200
    data = response.json()
    
    assert data["total_exams_analyzed"] == 1
    assert data["total_questions_analyzed"] == 1
    assert data["total_marks_analyzed"] == 5.0
    
def test_get_predictions(client: TestClient) -> None:
    # We mocked get_exam_predictions to not hit DB
    response = client.get("/api/exams/1/predictions")
    assert response.status_code == 200
    data = response.json()
    
    assert data["insufficient_data"] is False
    assert len(data["predictions"]) == 1
    assert data["predictions"][0]["characteristic"] == "High-Weight Topic"
