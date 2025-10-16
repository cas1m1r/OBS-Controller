from obswebsocket import requests as r
from obswebsocket import obsws
from dotenv import load_dotenv
import os

load_dotenv()

# Connect to OBS
ws = obsws("localhost", 4455, password=os.environ['OBS_PASSWORD'])
ws.connect()


async def switch_scene(scene_name):
	# Switch Scene
	ws.call(r.SetCurrentProgramScene(sceneName=scene_name))


async def start_stream():
	ws.call(r.StartStream())


async def stop_stream():
	ws.call(r.StopStream())


async def toggle_ticker(sceneName, newText):
	scenes = ws.call(r.GetSceneList())
	for s in scenes.getScenes():
		name = s.get('sceneName')
		if name == sceneName:
			ws.call(r.SetInputSettings(inputName='Chyron', inputSettings={"text": newText}))


async def toggle_text(sceneName, labelName, newText):
	scenes = ws.call(r.GetSceneList())
	for s in scenes.getScenes():
		if s.get('sceneName') == sceneName:
			ws.call(r.SetInputSettings(inputName=labelName, inputSettings={"text": newText}))

