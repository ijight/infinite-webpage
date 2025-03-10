# [Infinite Wiki](https://infinite-wiki.up.railway.app)

An endless wiki-style page generator powered by Google's Gemini Pro AI. Each article generates links to new topics, creating an infinite web of connected nonsense.

## Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create API key
3. Add to `.env` for local development
4. Add to Railway environment variables for deployment

## Deploy to Railway

1. Push to GitHub
2. Create new project on [Railway](https://railway.app)
3. Select "Deploy from GitHub repo"
4. Add environment variable:
   - `GEMINI_API_KEY`: Your Gemini API key
5. To make the app public, click "Unexposed Service," generate a domain and set the port to 8080.

You can see mine at [infinite-wiki.up.railway.app](https://infinite-wiki.up.railway.app).

## Local Dev

You can run the app locally by installing the dependencies and running the app.py file. 