from flask import Flask, request, jsonify, render_template, abort
from .obs_client import OBSClient
from .auth import require_role, resolve_role
from .config import cfg

# Load .env for any launch mode
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

app = Flask(__name__, template_folder='../web/templates', static_folder='../web/static')
app.secret_key = cfg('FLASK_SECRET', 'change-me')
obs = OBSClient(
    host=cfg('OBS_HOST', '127.0.0.1'),
    port=int(cfg('OBS_PORT', 4455)),
    password=cfg('OBS_PASSWORD', '')
)

@app.route('/')
def index():
    # Shell page; UI will fetch data after login
    return render_template('index.html', scenes=[], state={"streaming": False, "recording": False, "current_scene": None}, safe_mode=cfg('SAFE_MODE','true').lower()=="true")

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/api/health')
def health():
    return jsonify({"ok": True, "obs_connected": obs.ping()})

@app.route('/api/whoami')
@require_role(['admin','producer'])
def whoami():
    token = request.headers.get('X-Auth-Token') or request.args.get('token')
    return jsonify({"ok": True, "role": resolve_role(token)})

@app.route('/api/state')
@require_role(['admin','producer'])
def get_state():
    return jsonify(obs.state())

@app.route('/api/scenes')
@require_role(['admin','producer'])
def get_scenes():
    return jsonify({"scenes": obs.list_scenes(), "current": obs.current_scene()})

@app.route('/api/scene/items')
@require_role(['admin','producer'])
def get_scene_items():
    scene = request.args.get('scene')
    if not scene:
        abort(400, description='Missing scene')
    return jsonify({"scene": scene, "items": obs.scene_items(scene)})

@app.route('/api/inputs')
@require_role(['admin','producer'])
def get_inputs():
    return jsonify({"inputs": obs.list_inputs()})

@app.route('/api/stream/start', methods=['POST'])
@require_role(['admin'])
def stream_start():
    if cfg('SAFE_MODE','true').lower()=="true":
        abort(403, description='Safe mode enabled')
    obs.start_stream()
    return jsonify({"ok": True})

@app.route('/api/stream/stop', methods=['POST'])
@require_role(['admin'])
def stream_stop():
    obs.stop_stream()
    return jsonify({"ok": True})

@app.route('/api/record/start', methods=['POST'])
@require_role(['admin','producer'])
def record_start():
    obs.start_record()
    return jsonify({"ok": True})

@app.route('/api/record/stop', methods=['POST'])
@require_role(['admin','producer'])
def record_stop():
    obs.stop_record()
    return jsonify({"ok": True})

@app.route('/api/scene', methods=['POST'])
@require_role(['admin','producer'])
def set_scene():
    scene = request.json.get('name')
    obs.set_current_scene(scene)
    return jsonify({"ok": True})

@app.route('/api/source/toggle', methods=['POST'])
@require_role(['admin','producer'])
def toggle_source():
    scene = request.json.get('scene')
    source = request.json.get('source')
    enable = bool(request.json.get('enable', True))
    obs.toggle_source_enabled(scene, source, enable)
    return jsonify({"ok": True})

@app.route('/api/text', methods=['POST'])
@require_role(['admin','producer'])
def set_text():
    source = request.json.get('source')
    text = request.json.get('text', '')
    obs.set_text_source(source, text)
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(host=cfg('BIND_HOST','0.0.0.0'), port=int(cfg('BIND_PORT',8080)))