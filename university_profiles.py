"""Standalone university profiles blueprint; does not change existing Explorer logic."""
from flask import Blueprint, abort, render_template, request
from university_profiles_data import CATALOG

profiles_bp = Blueprint('university_profiles', __name__)

@profiles_bp.get('/university-profiles')
def index():
    return render_template('university_profiles.html', schools=sorted(CATALOG.values(), key=lambda x: x['name']), compare=False)

@profiles_bp.get('/university-profiles/compare')
def compare():
    slugs = list(dict.fromkeys(request.args.getlist('school')))
    if len(slugs) > 3:
        abort(400, 'Select no more than three universities.')
    selected = [CATALOG[slug] for slug in slugs if slug in CATALOG]
    return render_template('university_profiles.html', schools=selected, compare=True)

@profiles_bp.get('/university-profiles/<slug>')
def profile(slug):
    university = CATALOG.get(slug)
    if university is None:
        abort(404)
    return render_template('university_profile.html', university=university)
