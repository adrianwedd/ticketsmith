# 🚀 Developer Setup – TICKETSMITH

## Prerequisites
- Docker + Docker Compose
- Node.js & Python 3.11 (for local dev, optional)

## Quick Start

```bash
# Launch both frontend and backend
docker-compose up --build
```

Then access:
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:5000](http://localhost:5000)

## Project Structure

- `/frontend` – React UI to trigger Jira tasks
- `/api/skeleton.py` – Flask mockup backend
- `ticketsmith_cli.py` – CLI to create Jira/Confluence objects
- `.github/workflows/` – CI/CD with Forge deploy

## Development Notes

- Forge credentials must be set via GitHub secret: `FORGE_AUTH`
- Update `requirements.txt` for backend dependencies
- Backend auto-reloads in Docker with volume mount
- Frontend served via `react-scripts`

Happy shipping!
