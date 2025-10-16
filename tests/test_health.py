import json
from app.server import app

def test_health():
    with app.test_client() as c:
        res = c.get('/api/health')
        assert res.status_code == 200
        data = json.loads(res.data)
        assert 'ok' in data