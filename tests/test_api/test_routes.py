from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_frames_by_depth():
    response = client.post(
        "/api/v1/frames/by-depth",
        json={"depth_min": 9000.1, "depth_max": 9000.3, "color_map": "viridis"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if len(data) > 0:
        assert "id" in data[0]
        assert "depth" in data[0]
        assert "pixels" in data[0]
