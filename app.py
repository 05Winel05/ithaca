"""Ithaca web application: college journey planning and daily quests."""
import os
from datetime import timedelta, datetime, timezone
from secrets import token_hex
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, session, url_for, jsonify
from university_data import match_university, build_preparation_steps
from assessment_data import TOPICS, FORMS, public_questions, grade_form
from database import get_database

load_dotenv()
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 120 * 1024
app.permanent_session_lifetime = timedelta(days=90)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-local-secret-before-deployment")

ISLANDS = [
    {"symbol": "01", "title": "Academics", "detail": "Grades and academic growth", "icon": "✦"},
    {"symbol": "02", "title": "Exams", "detail": "Practice tests and improvement", "icon": "◇"},
    {"symbol": "03", "title": "Achievements", "detail": "Projects, competitions and skills", "icon": "★"},
    {"symbol": "04", "title": "Applications", "detail": "Essays and deadlines", "icon": "✧"},
    {"symbol": "05", "title": "Scholarships", "detail": "Funding and opportunities", "icon": "◈"},
]

QUESTS = [
    {"id": "plan", "title": "Plan your first study session", "detail": "Choose a subject and a specific study time", "xp": 20},
    {"id": "focus", "title": "Complete focused practice", "detail": "Study for 25 minutes using one clear goal", "xp": 30},
    {"id": "reflect", "title": "Reflect on one mistake", "detail": "Describe an error and how you would fix it", "xp": 25},
]



def get_owner_id():
    if "profile" not in session:
        return None
    if "guest_id" not in session:
        session["guest_id"] = token_hex(16)
    session.permanent = True
    return session["guest_id"]


def save_profile_to_atlas():
    """Keep a copy of the current session profile when Atlas is connected."""
    try:
        db = get_database()
        if db is not None and session.get("profile"):
            owner_id = get_owner_id()
            db["profiles"].update_one(
                {"_id": owner_id},
                {"$set": {"profile": session["profile"], "updated_at": datetime.now(timezone.utc)}},
                upsert=True,
            )
    except Exception as error:
        app.logger.warning("Profile backup skipped: %s", type(error).__name__)


@app.route("/api/sync", methods=["GET", "POST"])
def sync_progress():
    owner_id = get_owner_id()
    if not owner_id:
        return jsonify({"error": "Start your journey first."}), 403
    try:
        db = get_database()
        if db is None:
            return jsonify({"connected": False, "state": {}}) if request.method == "GET" else (jsonify({"error": "MongoDB is not configured."}), 503)
        collection = db["progress"]
        if request.method == "GET":
            document = collection.find_one({"_id": owner_id}, {"_id": 0, "state": 1})
            return jsonify({"connected": True, "state": (document or {}).get("state", {})})

        data = request.get_json(silent=True)
        if not isinstance(data, dict) or not isinstance(data.get("state"), dict):
            return jsonify({"error": "Invalid progress format."}), 400
        supplied = data["state"]
        if len(supplied) > 48:
            return jsonify({"error": "Too many progress sections."}), 400
        allowed = {
            "ithaca-quests", "ithaca-assessments-v1",
            "ithaca-athena-current-v1", "ithaca-athena-xp-v1",
        }
        state = {key: value for key, value in supplied.items()
                 if key in allowed or (key.startswith("ithaca-preparation:") and len(key) <= 220)}
        collection.update_one(
            {"_id": owner_id},
            {"$set": {"state": state, "updated_at": datetime.now(timezone.utc)}},
            upsert=True,
        )
        save_profile_to_atlas()
        return jsonify({"connected": True, "saved": True})
    except Exception as error:
        app.logger.warning("Atlas sync unavailable: %s", type(error).__name__)
        return jsonify({"error": "MongoDB could not be reached. Progress is still stored in your browser."}), 503


@app.get("/api/storage-status")
def storage_status():
    try:
        db = get_database()
        if db is None:
            return jsonify({"connected": False, "mode": "browser"})
        return jsonify({"connected": True, "mode": "mongodb", "database": db.name})
    except Exception:
        return jsonify({"connected": False, "mode": "browser"})


@app.get("/")
def home():
    return render_template("index.html", profile=session.get("profile", {}))


@app.post("/start")
def start():
    grade = request.form.get("grade", "").strip()
    if grade not in {"9", "10", "11", "12"}:
        return "Please select a grade between 9 and 12.", 400

    mode = request.form.get("mode", "general").strip()
    if mode not in {"general", "specific"}:
        return "Please select a preparation route.", 400

    interest = request.form.get("interest", "Undecided").strip()[:60] or "Undecided"
    study_hours = request.form.get("study_hours", "4-6").strip()
    if study_hours not in {"1-3", "4-6", "7-10", "11+"}:
        return "Please choose your weekly study time.", 400

    scholarships = request.form.get("scholarships") == "yes"

    gpa_value = request.form.get("gpa", "").strip()
    gpa_scale = request.form.get("gpa_scale", "4").strip()
    if gpa_scale not in {"4", "5", "100"}:
        return "Please select a GPA scale.", 400
    if gpa_value:
        try:
            score = float(gpa_value)
        except ValueError:
            return "Please enter a numeric GPA or leave it blank.", 400
        if not 0 <= score <= int(gpa_scale):
            return "The GPA must fit the selected scale.", 400
        gpa_value = f"{score:g}"

    universities = []
    if mode == "specific":
        for field in ("university", "university_2", "university_3"):
            name = request.form.get(field, "").strip()[:80]
            if name and name.casefold() not in {item.casefold() for item in universities}:
                universities.append(name)
        if not universities:
            return "Enter at least one university, or choose general preparation.", 400

    entry_year = request.form.get("entry_year", "").strip()
    if entry_year and (not entry_year.isdigit() or not 2027 <= int(entry_year) <= 2036):
        return "Choose an entry year between 2027 and 2036.", 400

    session["profile"] = {
        "grade": grade,
        "mode": mode,
        "destination": universities[0] if universities else "University readiness",
        "universities": universities,
        "interest": interest,
        "study_hours": study_hours,
        "scholarships": scholarships,
        "gpa": gpa_value,
        "gpa_scale": gpa_scale,
        "entry_year": entry_year,
    }
    get_owner_id()
    save_profile_to_atlas()
    return redirect(url_for("journey"))


@app.get("/journey")
def journey():
    profile = session.get("profile")
    if not profile:
        return redirect(url_for("home"))
    # Older sessions still have one destination rather than a universities list.
    if "universities" not in profile:
        profile = {**profile, "universities": [profile["destination"]] if profile.get("mode") == "specific" else []}
    return render_template("journey.html", profile=profile, islands=ISLANDS, quests=QUESTS)


@app.get("/requirements")
def requirements():
    profile = session.get("profile")
    if not profile:
        return redirect(url_for("home"))

    applicant_type = request.args.get("applicant", "international")
    if applicant_type not in {"international", "domestic"}:
        applicant_type = "international"

    selected_names = profile.get("universities", [])
    if not selected_names and profile.get("mode") == "specific" and profile.get("destination"):
        selected_names = [profile["destination"]]
    if not selected_names:
        selected_names = ["Stanford University", "MIT", "Rice University"]
    schools = [match_university(name) for name in selected_names]
    steps = build_preparation_steps(profile, schools)

    return render_template(
        "requirements.html", profile=profile, schools=schools,
        applicant_type=applicant_type, steps=steps,
        matched_count=sum(s["recognized"] for s in schools),
    )


@app.get("/assessment")
def assessment():
    profile = session.get("profile")
    if not profile:
        return redirect(url_for("home"))
    form = request.args.get("form", "A").upper()
    if form not in FORMS:
        form = "A"
    questions = public_questions(form)
    return render_template(
        "assessment.html", profile=profile, form=form, questions=questions,
        question_ids=[question["id"] for question in questions], topics=TOPICS,
    )


@app.post("/api/assessment/grade")
def grade_assessment():
    if "profile" not in session:
        return jsonify({"error": "Start your journey before taking an assessment."}), 403
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Send the assessment as JSON."}), 400
    try:
        result = grade_form(data.get("form"), data.get("answers"))
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(result)


@app.get("/progress")
def progress():
    profile = session.get("profile")
    if not profile:
        return redirect(url_for("home"))
    return render_template("progress.html", profile=profile, topics=TOPICS)


@app.get("/athena")
def athena():
    profile = session.get("profile")
    if not profile:
        return redirect(url_for("home"))
    return render_template("athena.html", profile=profile)


@app.post("/api/athena/plan")
def athena_plan():
    profile = session.get("profile")
    if not profile:
        return jsonify({"error": "Start your Ithaca journey before requesting a plan."}), 403
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid request."}), 400
    if data.get("consent") is not True:
        return jsonify({"error": "Please agree before sharing your study goals with Gemini."}), 400
    scenario = data.get("scenario", "steady")
    if scenario not in {"steady", "missed_week", "score_drop", "less_time"}:
        return jsonify({"error": "Choose a valid situation."}), 400

    assessment = None
    raw_assessment = data.get("assessment")
    if isinstance(raw_assessment, dict):
        form = raw_assessment.get("form")
        score, total = raw_assessment.get("score"), raw_assessment.get("total")
        if form in {"A", "B"} and type(score) is int and type(total) is int and total == 8 and 0 <= score <= total:
            topics = {}
            raw_topics = raw_assessment.get("topics")
            if isinstance(raw_topics, dict):
                for slug in TOPICS:
                    item = raw_topics.get(slug)
                    if isinstance(item, dict):
                        good, count = item.get("correct"), item.get("total")
                        if type(good) is int and type(count) is int and count == 2 and 0 <= good <= count:
                            topics[TOPICS[slug]["title"]] = f"{good}/{count} correct"
            assessment = {"form": form, "score": f"{score} of 8", "topic_results": topics}

    if not os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY") == "PASTE_YOUR_API_KEY_HERE":
        return jsonify({"error": "Gemini is not configured. Add GEMINI_API_KEY to your .env file, then restart Flask."}), 503
    try:
        from athena import generate_plan
        plan = generate_plan(profile, assessment, scenario)
    except ValueError as error:
        return jsonify({"error": str(error)}), 502
    except Exception as error:
        app.logger.warning("Gemini request did not complete (%s).", type(error).__name__)
        return jsonify({"error": "Gemini could not create a plan. Check your API key, model access, and network connection, then try again."}), 502
    return jsonify(plan)


from university_explorer import explorer_bp
app.register_blueprint(explorer_bp)

from university_profiles import profiles_bp
app.register_blueprint(profiles_bp)

if __name__ == "__main__":
    # Local development only; disable debug mode before deployment.
    app.run(debug=True)
