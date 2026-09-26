# Feelcast

Feelcast is a "how it actually feels" weather advisor. Instead of raw
temperature numbers, it tells you what to wear, taking into account not just
the official weather but also how a specific person perceives it (runs colder
or hotter than average) and live feedback from other users in the same city
today.

## How it works

1. Users are identified by an `X-Device-ID` header (no signup/password) — an
   account is created automatically on first contact from a device.
2. During onboarding, the user answers a few questions (cold/heat
   sensitivity, climate, activity level, attitude to rain) which are used to
   compute a personal thermal offset (`thermo_offset`).
3. The app fetches current weather for a city from the OpenWeather API.
4. A baseline clothing recommendation is computed from "feels like"
   temperature adjusted by the personal thermal offset.
5. An LLM (via LangChain + Groq) rewrites and enriches the advice in natural
   language, also factoring in recent reviews from other users in that city
   (e.g. "everyone says it's colder than the thermometer shows").
6. After a walk, the user can submit a check-in — how hot/cold it actually
   felt compared to the advice — which adjusts their personal thermal offset
   and gets added to the city's shared review feed.

## Stack

- **FastAPI** — web server and REST API
- **SQLAlchemy + Alembic** — storage for users, profiles and reviews, migrations
- **SQLite** — database
- **LangChain + langchain-groq** — LLM-generated advice text
- **OpenWeather API** — weather data
- **pytest / pytest-asyncio** — tests
- **Docker / docker-compose** — containerization

## API

| Method | Path                | Description                                              |
|--------|----------------------|------------------------------------------------------------|
| GET    | `/`                  | Serves the static app page                                  |
| GET    | `/whoami`            | Returns the current user resolved from `X-Device-ID`        |
| POST   | `/onboarding`        | Saves onboarding answers and the personal thermal offset     |
| GET    | `/weather/{city}`    | Quick weather advice without personalization                 |
| POST   | `/advice/{city}`     | Personalized advice using profile and city reviews            |
| POST   | `/checkin`           | Post-walk check-in: adjusts profile, records a review          |
| GET    | `/feed?city=...`     | Recent user reviews for a city                                 |

All endpoints except `/`, `/weather/{city}` and `/feed` require the
`X-Device-ID` header to identify the user.

## Running locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Create a `.env` file in the project root:

```
GROQ_API_KEY=...
OPENWEATHER_API_KEY=...
```

### With Docker

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8000`.

## Tests

```bash
pytest
```