"""Ithaca University Explorer: curated official links, not admissions policy claims."""
from flask import Blueprint, render_template
from university_data import UNIVERSITIES

explorer_bp = Blueprint('explorer', __name__)

EXTRA = [
    ('harvard', 'Harvard University', 'Cambridge', 'Massachusetts', 'https://college.harvard.edu/admissions/apply/first-year-applicants'),
    ('yale', 'Yale University', 'New Haven', 'Connecticut', 'https://admissions.yale.edu/apply'),
    ('gatech', 'Georgia Institute of Technology', 'Atlanta', 'Georgia', 'https://admission.gatech.edu/first-year/deadlines'),
    ('berkeley', 'University of California, Berkeley', 'Berkeley', 'California', 'https://www.admissions.berkeley.edu/'),
]

@explorer_bp.get('/explore')
def explore():
    schools = []
    for slug, school in UNIVERSITIES.items():
        place = school.get('location', '')
        parts = [p.strip() for p in place.split(',')]
        schools.append({
            'id': slug, 'name': school['name'], 'city': parts[0],
            'region': parts[-1] if len(parts) > 1 else '',
            'admissions': school['admission_url'], 'details': True,
            'testing': school.get('testing', 'Check official source'),
            'application': school.get('application', 'Check official source'),
            'aid': school.get('aid_international', 'Check official source'),
            'date_note': 'Recheck current admission year and applicant category',
        })
    for slug, name, city, region, url in EXTRA:
        schools.append({
            'id': slug, 'name': name, 'city': city, 'region': region,
            'admissions': url, 'details': False,
            'testing': 'Not yet reviewed in Ithaca',
            'application': 'Not yet reviewed in Ithaca',
            'aid': 'Not yet reviewed in Ithaca',
            'date_note': 'Official admissions link only — verify requirements yourself',
        })
    schools.sort(key=lambda s: s['name'].casefold())
    return render_template('explorer.html', schools=schools)
