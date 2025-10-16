# OBS WebSocket client wrapper using obswebsocket-py (requests API)
from obswebsocket import obsws, requests as r

class OBSClient:
    def __init__(self, host='127.0.0.1', port=4455, password=''):
        self.host, self.port, self.password = host, port, password
        self.ws = obsws(self.host, self.port, self.password)
        self._connect()

    def _connect(self):
        try:
            if not getattr(self.ws, 'ws', None) or not self.ws.ws.connected:
                self.ws.connect()
        except Exception:
            pass

    # ---- Discovery ----
    def list_scenes(self):
        self._connect()
        res = self.ws.call(r.GetSceneList())
        return [s.get('sceneName') for s in res.getScenes()]

    def current_scene(self):
        self._connect()
        return self.ws.call(r.GetCurrentProgramScene()).getCurrentProgramSceneName()

    def list_inputs(self):
        self._connect()
        try:
            res = self.ws.call(r.GetInputList())
            return [{"inputName": i.get('inputName'), "inputKind": i.get('inputKind')} for i in res.getInputs()]
        except Exception:
            # fallback for older versions
            inputs = set()
            for sc in self.list_scenes():
                for it in self.scene_items(sc):
                    inputs.add(it.get('sourceName'))
            return [{"inputName": name, "inputKind": None} for name in sorted(inputs)]

    def scene_items(self, scene_name):
        self._connect()
        res = self.ws.call(r.GetSceneItemList(sceneName=scene_name))
        return res.getSceneItems()

    # ---- Control ----
    def set_current_scene(self, name):
        self._connect()
        self.ws.call(r.SetCurrentProgramScene(sceneName=name))

    def start_stream(self):
        self._connect()
        self.ws.call(r.StartStream())

    def stop_stream(self):
        self._connect()
        self.ws.call(r.StopStream())

    def start_record(self):
        self._connect()
        self.ws.call(r.StartRecord())

    def stop_record(self):
        self._connect()
        self.ws.call(r.StopRecord())

    def set_text_source(self, input_name, text):
        self._connect()
        self.ws.call(r.SetInputSettings(inputName=input_name, inputSettings={"text": text}, overlay=True))

    def toggle_source_enabled(self, scene_name, source_name, enable=True):
        self._connect()
        res = self.ws.call(r.GetSceneItemList(sceneName=scene_name))
        sid = None
        for item in res.getSceneItems():
            if item.get('sourceName') == source_name:
                sid = item.get('sceneItemId')
                break
        if sid is None:
            raise ValueError(f"Source '{source_name}' not found in scene '{scene_name}'")
        self.ws.call(r.SetSceneItemEnabled(sceneName=scene_name, sceneItemId=sid, sceneItemEnabled=enable))

    # ---- Health ----
    def ping(self):
        try:
            self._connect()
            self.ws.call(r.GetVersion())
            return True
        except Exception:
            return False

    def state(self):
        self._connect()
        streaming = self.ws.call(r.GetStreamStatus()).getStreaming()
        recording = self.ws.call(r.GetRecordStatus()).getIsRecording()
        return {
            "streaming": streaming,
            "recording": recording,
            "current_scene": self.current_scene(),
        }