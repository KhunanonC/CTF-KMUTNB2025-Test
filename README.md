# Simple CTF Docker
ctf-docker/
├── Dockerfile              # Defines how to build the Docker image (Python + Flask app)
├── docker-compose.yml      # Coordinates container setup and ports (e.g. localhost:8000)
├── requirements.txt        # Lists Python dependencies (Flask, etc.)
├── .dockerignore           # Tells Docker which files to exclude from the image (e.g. venv, __pycache__)
├── README.md               # Documentation for your challenge
├── app.py                  # Main Flask application (routes, logic, etc.)
├── static/                 # Front-end static assets
│   └── style.css           # Your stylesheet
└── templates/              # Jinja2 HTML templates for Flask
    ├── login.html
    ├── dashboard.html
    └── profile.html
This is a small intentionally vulnerable CTF app (for local/lab use only).

Flags:
- Flag 1: shown on dashboard after login.
- Flag 2: in the HTML source of the login page.
- Flag 3: accessible via IDOR at `/profile?id=0` after login.

Default behavior:
- Any username except `admin` can log in if the password equals `base64(username)`.
- If username exists in `USERS` it uses that id; otherwise a new user id is created.
- `admin` account exists at id `0` and cannot be logged in via the form.

Run locally:
```bash
# build and run
docker build -t simple-ctf .
docker run -d --name simple-ctf -p 8000:8000 simple-ctf

# or using docker-compose
docker-compose up --build -d