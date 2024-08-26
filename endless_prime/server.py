import json
import math
import os
from flask import Flask, render_template_string, Response
import matplotlib

matplotlib.use("Agg")  # Use a non-interactive backend
import matplotlib.pyplot as plt
import io
import base64
import time
from threading import Thread

from endless_prime.calc import get_next_prime


app = Flask(__name__)

x_values = []
y_values = []
prime_value = 0


def generate_new_point():
    global x_values, y_values, prime_value
    while True:
        prime_value = get_next_prime(prime_value)
        x = prime_value * math.cos(prime_value)
        y = prime_value * math.sin(prime_value)

        x_values.append(x)
        y_values.append(y)

        time.sleep(0.2)  # Wait 1 second before generating the next point
        prime_value += 1


def update_plot(x, y):
    plt.figure(figsize=(10, 10))  # Set figure size to ensure it's squared
    plt.plot(x, y, "bo")

    # Make the plot square by setting the aspect ratio to 'equal'
    minimal = min(min(x_values), min(y_values))
    maximal = max(max(x_values), max(y_values))
    limit = max(abs(minimal), maximal)
    plt.axis([-limit, limit, -limit, limit])
    plt.gca().set_aspect("equal", adjustable="box")

    # Remove axis ticks and labels
    plt.xticks([])
    plt.yticks([])
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().set_facecolor("#222222")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", facecolor="#222222")
    buf.seek(0)

    plot_url = base64.b64encode(buf.getvalue()).decode("ascii")
    plt.close()
    return plot_url


@app.route("/")
def index():
    return render_template_string(
        """
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
                font-family: Arial, sans-serif;
            }
            h1 {
                text-align: center;
                color: #ffffff;
            }
            #plot-container {
                display: flex;
                justify-content: center;
                flex-direction: column;
                align-items: center;
            }
            img {
                border: 1px solid #444444;
            }
            #given-number {
                margin-top: 15px;
                font-size: 20px;
                color: #cccccc;
            }
        </style>
        <h1>Endless Prime</h1>
        <div id="plot-container">
            <img id="plot" src="{{ url_for('plot') }}">
            <div id="given-number">Prime: <span id="number">{{ number }}</span></div>
        </div>
        <script>
            var source = new EventSource("{{ url_for('stream') }}");
            source.onmessage = function(event) {
                var data = JSON.parse(event.data);
                document.getElementById("plot").src = "data:image/png;base64," + data.plot;
                document.getElementById("number").innerText = data.number;
            };
        </script>
    """,
        number=prime_value,
    )


@app.route("/plot")
def plot():
    plot_url = update_plot(x_values, y_values)
    return plot_url


@app.route("/stream")
def stream():
    def event_stream():
        global prime_value
        while True:
            plot_url = update_plot(x_values, y_values)
            data = {"plot": plot_url, "number": prime_value}
            yield f"data: {json.dumps(data)}\n\n"
            time.sleep(1)  # Send updates every second

    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":
    # Start the point generation in a separate thread
    point_generator_thread = Thread(target=generate_new_point)
    point_generator_thread.start()

    # Start the Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True, threaded=True)
