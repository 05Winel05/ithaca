"""Small, transparent Athena context builder for Ithaca (no API requests)."""
import re
from university_profiles_data import CATALOG

ALIASES = {
    'mit': 'mit', 'massachusetts institute of technology': 'mit',
    'uta': 'uta', 'ut arlington': 'uta', 'university of texas arlington': 'uta',
    'utd': 'utd', 'ut dallas': 'utd', 'university of texas dallas': 'utd',
    'ut austin': 'ut', 'university of texas austin': 'ut',
    'tamu': 'tamu', 'texas a&m': 'tamu', 'texas a and m university': 'tamu',
    'uc berkeley': 'berkeley', 'university of california berkeley': 'berkeley',
    'georgia tech': 'gatech', 'rice': 'rice', 'stanford': 'stanford',
    'harvard': 'harvard', 'yale': 'yale', 'duke': 'duke',
    'purdue': 'purdue', 'princeton': 'princeton', 'smu': 'smu',
    'unt': 'unt', 'ttu': 'ttu', 'uh': 'uh', 'txst': 'txst',
}


def _normalize(value):
    return re.sub(r'[^a-z0-9]+', ' ', str(value or '').casefold()).strip()


def _school_by_name(value):
    query = _normalize(value)
    if not query:
        return None
    slug = ALIASES.get(query)
    if slug in CATALOG:
        return CATALOG[slug]
    for record in CATALOG.values():
        if query in {_normalize(record.get('name')), _normalize(record.get('slug'))}:
            return record
    return None  # Never guess which university was intended


def _practice_focus(assessment):
    if not isinstance(assessment, dict):
        return {'status': 'No completed practice check shared', 'focus_topics': []}
    scores = []
    for topic, value in (assessment.get('topic_results') or {}).items():
        match = re.fullmatch(r'\s*(\d+)\s*/\s*(\d+)\s+correct\s*', str(value))
        if not match:
            continue
        correct, total = map(int, match.groups())
        if total and 0 <= correct <= total:
            scores.append((correct / total, topic[:60], correct, total))
    scores.sort(key=lambda item: (item[0], item[1]))
    return {
        'status': 'Original short practice check; not a validated standardized exam',
        'focus_topics': [
            {'topic': topic, 'correct': correct, 'total': total}
            for ratio, topic, correct, total in scores if ratio < 1.0
        ][:2],
        'caution': 'Two questions per topic: small sample; do not infer ability or exam readiness.',
    }


def build_athena_context(profile, assessment):
    """Return limited source-linked context; no user secrets, networking, or requests."""
    schools = []
    unmatched = []
    for name in (profile.get('universities') or [])[:3]:
        item = _school_by_name(name)
        if not item:
            unmatched.append(str(name)[:80])
            continue
        if any(s['name'] == item['name'] for s in schools):
            continue
        schools.append({
            'name': item['name'],
            'official_admissions_url': item['admissions_url'],
            'source_reviewed': item.get('review_date'),
            'testing_reference': item.get('testing') or 'Not verified',
            'application_documents_reference': item.get('documents') or 'Not verified',
            # Dates become obsolete quickly. Require the student to check the official page.
            'deadlines': 'Check official admissions page for the intended entry year and round',
            'english_proficiency': 'Check the official international applicant requirements',
            'financial_aid': 'Check official financial aid rules for applicant status',
        })
    return {
        'university_references': schools,
        'universities_not_in_curated_catalog': unmatched,
        'practice_priorities': _practice_focus(assessment),
        'reference_notice': (
            'Planning references only; no live verification. Policies may have changed. '
            'Do not infer eligibility, acceptance, deadlines, costs, or standardized scores.'
        ),
    }
