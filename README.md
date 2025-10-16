# OBS Remote over Tailnet — Starter Kit
Control OBS from any device on your private tailnet (Tailscale/WireGuard). 

## Features
- Start/Stop Stream & Recording
- Switch Scenes, Toggle Sources, Set Text
- Safe Mode (off by default for stream)
- Simple role tokens (admin/producer)

## Quickstart
1. Enable OBS WebSocket (Tools → WebSocket Server)
2. Copy `.env.example` → `.env` and fill in values
3. `pip install -r app/requirements.txt`
4. `FLASK_APP=app.server:app flask run -h 0.0.0.0 -p 8080`
5. Visit `http://<tailnet-host>:8080/?token=ADMIN_TOKEN`

## Security
Use on a tailnet. Prefer HTTPS via reverse proxy or Tailscale Funnel. Set strong tokens.

## License
Single user. Commercial use allowed for your own channels. No resale of code.
