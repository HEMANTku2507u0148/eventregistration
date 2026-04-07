"""
app_cloud.py — Cloud-native version using Google Cloud Firestore.
Deployable to Cloud Run (serverless).

Routes:
  GET  /                   → Registration form
  POST /register           → Submit registration
  GET  /admin              → Admin panel (password protected)
  POST /admin/login        → Admin login
  GET  /admin/logout       → Admin logout
  POST /admin/delete/<id>  → Delete a registration (Firestore doc ID)
"""

import os
from datetime import datetime, timezone, date
from collections import Counter
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, get_flashed_messages, session
)
from google.cloud import firestore

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "change-this-in-production")

ADMIN_PWD  = os.environ.get("ADMIN_PASSWORD", "admin123")   # override via env var
COLLECTION = "registrations"

# Firestore client (uses ADC / Cloud Run service account automatically)
db = firestore.Client()


# ── FIRESTORE HELPERS ────────────────────────────────────────────────────────

def get_registration_count():
    try:
        result = db.collection(COLLECTION).count().get()
        return result[0][0].value
    except Exception:
        return sum(1 for _ in db.collection(COLLECTION).stream())


def get_all_registrations():
    docs = db.collection(COLLECTION).order_by(
        "created_at", direction=firestore.Query.DESCENDING
    ).stream()

    result = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id   # Firestore document ID (used for delete)

        # Format timestamp
        ts = d.get("created_at")
        if ts:
            try:
                if hasattr(ts, "astimezone"):
                    d["created_at"] = ts.astimezone().strftime("%d %b %Y, %I:%M %p")
                else:
                    d["created_at"] = str(ts)
            except Exception:
                d["created_at"] = str(ts)

        result.append(d)
    return result


def build_stats(registrations):
    total        = len(registrations)
    today_str    = date.today().strftime("%d %b %Y")
    today_count  = sum(1 for r in registrations if today_str in str(r.get("created_at", "")))
    events       = list({r["event_name"] for r in registrations if r.get("event_name")})
    event_counts = Counter(r["event_name"] for r in registrations if r.get("event_name"))
    top_event    = event_counts.most_common(1)[0][0] if event_counts else None

    return {
        "total":      total,
        "today":      today_count,
        "events":     len(events),
        "event_list": sorted(events),
        "top_event":  top_event,
    }


# ── STUDENT ROUTES ───────────────────────────────────────────────────────────

@app.route("/")
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        "index.html",
        messages=messages,
        version_label="Google Cloud · Cloud Run + Firestore",
        reg_count=get_registration_count(),
    )


@app.route("/register", methods=["POST"])
def register():
    full_name  = request.form.get("full_name", "").strip()
    email      = request.form.get("email", "").strip()
    phone      = request.form.get("phone", "").strip()
    event_name = request.form.get("event_name", "").strip()
    year       = request.form.get("year", "").strip()
    department = request.form.get("department", "").strip()

    if not full_name or not email or not event_name:
        flash("Please fill in all required fields.", "error")
        return redirect(url_for("index"))

    try:
        db.collection(COLLECTION).add({
            "full_name":  full_name,
            "email":      email,
            "phone":      phone,
            "event_name": event_name,
            "year":       year,
            "department": department,
            "created_at": datetime.now(timezone.utc),
        })
        flash(
            f"🎉 You're registered for {event_name}, {full_name.split()[0]}! See you there.",
            "success",
        )
    except Exception as e:
        flash(f"Registration failed: {str(e)}", "error")

    return redirect(url_for("index"))


# ── ADMIN ROUTES ─────────────────────────────────────────────────────────────

@app.route("/admin")
def admin():
    logged_in = session.get("admin_logged_in", False)
    messages  = get_flashed_messages(with_categories=True)

    if logged_in:
        registrations = get_all_registrations()
        stats         = build_stats(registrations)
    else:
        registrations = []
        stats         = {}

    return render_template(
        "admin.html",
        logged_in=logged_in,
        messages=messages,
        registrations=registrations,
        stats=stats,
        version_label="Google Cloud · Cloud Run + Firestore",
    )


@app.route("/admin/login", methods=["POST"])
def admin_login():
    password = request.form.get("password", "")
    if password == ADMIN_PWD:
        session["admin_logged_in"] = True
        flash("Welcome back, Admin!", "success")
    else:
        flash("Incorrect password. Please try again.", "error")
    return redirect(url_for("admin"))


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_logged_in", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("admin"))


@app.route("/admin/delete/<doc_id>", methods=["POST"])
def admin_delete(doc_id):
    if not session.get("admin_logged_in"):
        flash("Unauthorised.", "error")
        return redirect(url_for("admin"))
    try:
        db.collection(COLLECTION).document(doc_id).delete()
        flash("Registration deleted successfully.", "success")
    except Exception as e:
        flash(f"Delete failed: {str(e)}", "error")
    return redirect(url_for("admin"))


# ── ENTRY POINT ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"🔑 Admin password : {ADMIN_PWD}  (set ADMIN_PASSWORD env var to change)")
    print(f"🌐 Registration   : http://localhost:{port}/")
    print(f"🛡️  Admin panel    : http://localhost:{port}/admin")
    app.run(debug=False, host="0.0.0.0", port=port)
