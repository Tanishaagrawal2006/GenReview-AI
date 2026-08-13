# ReviewFlow AI

ReviewFlow AI is a review management and tenant onboarding platform. It allows businesses to capture feedback, generate AI-driven response drafts, and securely route alerts for unhappy customers.

## Deployment on Render

1. Fork or clone this repository to your GitHub account.
2. Go to [Render](https://render.com/) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the **Build Command** to:
   ```bash
   pip install -r requirements.txt
   ```
5. Set the **Start Command** to:
   ```bash
   gunicorn app:app
   ```
6. Under **Environment Variables**, add the keys specified in `.env.example`:
   - `FLASK_SECRET_KEY` (Generate a secure random string)
   - `GROQ_API_KEY` (Your Groq API key)
   - `SMTP_SERVER` (e.g., smtp.gmail.com)
   - `SMTP_PORT` (e.g., 587)
   - `SMTP_SENDER_EMAIL` (Your sender email)
   - `SMTP_SENDER_PASSWORD` (Your app password for the email)
   - `BASE_URL` (Set this to your Render URL, e.g., `https://your-app-name.onrender.com`)
   - `FLASK_ENV` (Set to `production`)

## Local Development

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your values.
4. Run the application:
   ```bash
   python app.py
   ```
