from flask import Flask, jsonify, render_template, request

from algorithm import (
    find_common_free_intervals,
    generate_meeting_slots
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/find-time", methods=["POST"])
def find_time():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No data received."
            }), 400

        schedules = data.get("schedules", {})

        work_start = data.get(
            "work_start",
            "09:00"
        )

        work_end = data.get(
            "work_end",
            "17:00"
        )

        duration = int(
            data.get(
                "duration",
                30
            )
        )

        if not schedules:
            return jsonify({
                "success": False,
                "error": "Please add at least one participant schedule."
            }), 400

        if duration <= 0:
            return jsonify({
                "success": False,
                "error": "Meeting duration must be greater than 0."
            }), 400

        # ------------------------------------------------
        # CALL THE DAA ALGORITHM
        # ------------------------------------------------

        common_intervals = find_common_free_intervals(
            schedules,
            work_start,
            work_end,
            duration
        )

        meeting_slots = generate_meeting_slots(
            common_intervals,
            duration
        )

        # ------------------------------------------------
        # CONVERT RESULTS TO JSON
        # ------------------------------------------------

        common_results = []

        for start, end, available_duration in common_intervals:

            common_results.append({
                "start": start,
                "end": end,
                "duration": available_duration
            })

        slot_results = []

        for start, end in meeting_slots:

            slot_results.append({
                "start": start,
                "end": end
            })

        return jsonify({
            "success": True,
            "common_intervals": common_results,
            "meeting_slots": slot_results
        })

    except ValueError as error:

        return jsonify({
            "success": False,
            "error": str(error)
        }), 400

    except Exception as error:

        return jsonify({
            "success": False,
            "error": f"Server error: {str(error)}"
        }), 500


if __name__ == "__main__":

    print("=" * 60)
    print("              SMARTMEET WEB APPLICATION")
    print("=" * 60)
    print()
    print("Starting Flask server...")
    print("Open your browser at:")
    print("http://127.0.0.1:5000")
    print()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )