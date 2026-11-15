"""Admissions reference pages used by the university planning screen."""

UNIVERSITIES = {
    "stanford": {
        "name": "Stanford University",
        "short_name": "Stanford",
        "aliases": ("stanford", "stanford university"),
        "location": "Stanford, California",
        "application": "Common Application + Stanford Questions",
        "testing": "SAT or ACT required",
        "testing_kind": "required",
        "testing_detail": "Stanford lists SAT or ACT scores as a required component of its first-year application.",
        "materials": ["High school transcript / academic results", "School report and counselor recommendation", "Two teacher recommendations", "Application essays and Stanford Questions"],
        "deadlines": "Nov 1 (Restrictive Early Action); Jan 5 (Regular Decision)",
        "aid_domestic": "Need-based financial aid. Use Stanford's checklist for U.S. citizens and eligible noncitizens; requirements depend on your situation.",
        "aid_international": "Need-based financial aid is available. International applicants must follow Stanford's international aid checklist; need for aid can be considered in international admission decisions.",
        "additional": "The optional arts portfolio has separate earlier submission dates.",
        "admission_url": "https://admission.stanford.edu/apply/first-year/",
        "aid_url": "https://financialaid.stanford.edu/undergrad/apply/index.html",
    },
    "mit": {
        "name": "Massachusetts Institute of Technology",
        "short_name": "MIT",
        "aliases": ("mit", "massachusetts institute of technology", "mit university"),
        "location": "Cambridge, Massachusetts",
        "application": "MIT application portal (not the Common App)",
        "testing": "SAT or ACT required",
        "testing_kind": "required",
        "testing_detail": "MIT requires SAT or ACT scores. English proficiency exams are strongly recommended for some non-native English speakers.",
        "materials": ["Secondary school report and transcript", "Two teacher recommendations", "MIT essays, activities, and academics", "SAT or ACT results"],
        "deadlines": "Nov 1 (Early Action); Jan 4 (Regular Action)",
        "aid_domestic": "Need-based aid. Prospective students submit the CSS Profile and requested family documents; domestic applicants also submit the FAFSA.",
        "aid_international": "Need-based aid is open to international applicants. Prospective students submit the CSS Profile and supporting family income documents.",
        "additional": "Optional maker, arts, and research portfolios may be submitted if relevant to the applicant.",
        "admission_url": "https://mitadmissions.org/apply/firstyear/deadlines-requirements/",
        "aid_url": "https://sfs.mit.edu/undergraduate-students/apply-for-aid/deadlines-process/",
    },
    "rice": {
        "name": "Rice University",
        "short_name": "Rice",
        "aliases": ("rice", "rice university"),
        "location": "Houston, Texas",
        "application": "Common Application + Rice writing supplement",
        "testing": "SAT or ACT recommended, not required",
        "testing_kind": "recommended",
        "testing_detail": "Rice recommends SAT or ACT scores if available, but students who do not submit scores still receive full admission consideration.",
        "materials": ["High school transcript", "Counselor and two teacher recommendations", "Common App and Rice writing supplement", "English proficiency evidence if applicable"],
        "deadlines": "Nov 1 (Early Decision I); Jan 4 (Early Decision II / Regular Decision)",
        "aid_domestic": "Need-based aid is available to domestic applicants. Rice also automatically considers admitted first-year applicants for merit scholarships.",
        "aid_international": "Rice is need-aware for international admissions and offers limited need-based aid to international first-year students. The international financial statement is required; merit consideration is automatic.",
        "additional": "Some programs, including Architecture and Music, require additional materials.",
        "admission_url": "https://admission.rice.edu/apply/first-year-international-applicants",
        "domestic_admission_url": "https://admission.rice.edu/apply/first-year-domestic-applicants",
        "aid_url": "https://financialaid.rice.edu/apply-aid/international-students",
        "domestic_aid_url": "https://financialaid.rice.edu/",
    },
}


def match_university(name):
    normalized = " ".join(name.casefold().split())
    for slug, school in UNIVERSITIES.items():
        if normalized in school["aliases"]:
            return {"slug": slug, **school, "recognized": True, "requested_name": name}
    return {"slug": None, "name": name, "short_name": name, "recognized": False, "requested_name": name}


def build_preparation_steps(profile, schools):
    """Create general planning actions, without claiming admission eligibility."""
    grade = int(profile.get("grade", 11))
    steps = [
        {
            "id": "coursework",
            "title": "Review your academic foundation",
            "detail": "Identify your strongest courses and one subject you want to improve.",
            "island": "academics",
        },
        {
            "id": "university-sources",
            "title": "Check official admissions pages",
            "detail": "Confirm requirements for your intended entry year and applicant category.",
            "island": "applications",
        },
    ]
    if any(s.get("testing_kind") == "required" for s in schools):
        steps.append({
            "id": "test-plan",
            "title": "Create a SAT or ACT preparation plan",
            "detail": "At least one selected university requires testing; start with practice questions and track your weakest areas.",
            "island": "exams",
        })
    else:
        steps.append({
            "id": "test-research",
            "title": "Review testing choices",
            "detail": "Check whether standardized tests could support your application goals.",
            "island": "exams",
        })
    if grade <= 10:
        steps.append({
            "id": "activities",
            "title": "Build a meaningful activity",
            "detail": "Choose a project, community activity, or competition you can work on consistently.",
            "island": "achievements",
        })
    else:
        steps.append({
            "id": "activities",
            "title": "Document your achievements",
            "detail": "Record your projects, responsibilities, impact, and what you learned.",
            "island": "achievements",
        })
    steps.append({
        "id": "application-story",
        "title": "Start an application story journal" if grade < 12 else "Outline application essays",
        "detail": "Capture concrete experiences that show your interests and growth.",
        "island": "applications",
    })
    if profile.get("scholarships"):
        steps.append({
            "id": "financial-aid",
            "title": "Research financial aid requirements",
            "detail": "Identify need-based aid, merit scholarships, and documents needed for your applicant category.",
            "island": "scholarships",
        })
    return steps
