import os
from flask import Flask, render_template, Response
from services.gemini_service import GeminiService

app = Flask(__name__)
app.config.update(
    ENV='production',
    DEBUG=False,
    PROPAGATE_EXCEPTIONS=True
)

gemini_service = GeminiService()

port = int(os.environ.get("PORT", 5000))

@app.route('/')
def index():
    print("Serving index page")
    return render_template('page.html')

@app.route('/generate')
def generate():
    print("Starting content generation")
    return Response(
        gemini_service.get_initial_page(),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

@app.route('/topic/<topic_name>')
def topic(topic_name):
    print(f"Generating content for topic: {topic_name}")
    topic = topic_name.replace('-', ' ')
    return Response(
        gemini_service.get_topic_page(topic),
        mimetype='text/event-stream',
        headers={
            'Cache-Control': 'no-cache',
            'X-Accel-Buffering': 'no'
        }
    )

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host='0.0.0.0', port=port) 