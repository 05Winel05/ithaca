"""Ithaca University Explorer: curated official admissions starting points.

Only universities in university_data.UNIVERSITIES have reviewed Ithaca summaries.
All other schools are official-link-only: never infer their requirements.
"""

from flask import Blueprint, render_template
from university_data import UNIVERSITIES

explorer_bp = Blueprint('explorer', __name__)

# id, official name, city, state, official first-year/undergraduate admissions page
EXTRA = [
    ('harvard', 'Harvard University', 'Cambridge', 'Massachusetts', 'https://college.harvard.edu/admissions/apply/first-year-applicants'),
    ('yale', 'Yale University', 'New Haven', 'Connecticut', 'https://admissions.yale.edu/apply'),
    ('gatech', 'Georgia Institute of Technology', 'Atlanta', 'Georgia', 'https://admission.gatech.edu/first-year/deadlines'),
    ('berkeley', 'University of California, Berkeley', 'Berkeley', 'California', 'https://www.admissions.berkeley.edu/'),
    ('utaustin', 'University of Texas at Austin', 'Austin', 'Texas', 'https://admissions.utexas.edu/apply/freshman/'),
    ('tamu', 'Texas A&M University', 'College Station', 'Texas', 'https://admissions.tamu.edu/apply/freshman/index.html'),
    ('utdallas', 'University of Texas at Dallas', 'Richardson', 'Texas', 'https://enroll.utdallas.edu/freshman/'),
    ('utarlington', 'University of Texas at Arlington', 'Arlington', 'Texas', 'https://www.uta.edu/admissions/apply/freshmen'),
    ('houston', 'University of Houston', 'Houston', 'Texas', 'https://www.uh.edu/undergraduate-admissions/'),
    ('baylor', 'Baylor University', 'Waco', 'Texas', 'https://admissions.web.baylor.edu/'),
    ('smu', 'Southern Methodist University', 'Dallas', 'Texas', 'https://www.smu.edu/admission'),
    ('texastech', 'Texas Tech University', 'Lubbock', 'Texas', 'https://www.depts.ttu.edu/admissions/'),
    ('unt', 'University of North Texas', 'Denton', 'Texas', 'https://admissions.unt.edu/'),
    ('txstate', 'Texas State University', 'San Marcos', 'Texas', 'https://www.admissions.txst.edu/'),
    ('princeton', 'Princeton University', 'Princeton', 'New Jersey', 'https://admission.princeton.edu/'),
    ('duke', 'Duke University', 'Durham', 'North Carolina', 'https://admissions.duke.edu/'),
    ('purdue', 'Purdue University', 'West Lafayette', 'Indiana', 'https://admissions.purdue.edu/'),
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
