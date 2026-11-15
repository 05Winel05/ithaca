"""Curated planning references; not live admissions verification. Updated 2026-11-15."""
REVIEW_DATE = '2026-11-15'
# Each record contains an official entry point. Unverified values are intentionally not guessed.
SCHOOLS = [
('stanford','Stanford University','Stanford','California','Private','https://admission.stanford.edu/apply/first-year/','SAT or ACT required','Common Application, transcript, school report, two teacher recommendations','REA Nov 1; RD Jan 5','Stanford first-year admissions page'),
('mit','Massachusetts Institute of Technology (MIT)','Cambridge','Massachusetts','Private','https://mitadmissions.org/apply/firstyear/deadlines-requirements/','SAT or ACT required','MIT application, transcripts, two teacher letters','EA Nov 1; RA Jan 4','MIT deadlines and requirements'),
('rice','Rice University','Houston','Texas','Private','https://admission.rice.edu/apply/first-year-domestic-applicants','Review current official first-year testing policy','Application, school transcript, recommendation letters','ED I Nov 1; ED II/RD Jan 4','Rice first-year domestic admissions'),
('harvard','Harvard University','Cambridge','Massachusetts','Private','https://college.harvard.edu/admissions/apply/first-year-applicants','SAT or ACT required; limited exceptions on official page','Common Application, supplements, school report, two teacher recommendations','REA Nov 1; RD Jan 1','Harvard first-year applicants'),
('yale','Yale University','New Haven','Connecticut','Private','https://admissions.yale.edu/apply','Standardized testing required; review test-flexible options','Application, school report, recommendations, testing','SCEA Nov 1; RD Jan 2','Yale apply'),
('gatech','Georgia Institute of Technology','Atlanta','Georgia','Public','https://admission.gatech.edu/first-year/deadlines',None,None,None,'Georgia Tech first-year admissions'),
('berkeley','University of California, Berkeley','Berkeley','California','Public','https://admissions.berkeley.edu/',None,None,None,'UC Berkeley admissions'),
('uta','University of Texas at Arlington','Arlington','Texas','Public','https://www.uta.edu/admissions/apply/freshmen','SAT/ACT optional but encouraged','Application, application fee/waiver, transcripts','Fall priority Feb 15; fall merit deadline Mar 1','UTA first-year admissions'),
('utd','University of Texas at Dallas','Richardson','Texas','Public','https://enroll.utdallas.edu/freshman/criteria/',None,'Holistic review of high school grades and coursework','Priority Dec 1; regular May 1','UT Dallas freshman criteria'),
('tamu','Texas A&M University','College Station','Texas','Public','https://admissions.tamu.edu/apply/freshman/index.html',None,'First-year admission application and supporting documents',None,'Texas A&M freshman admissions'),
('uh','University of Houston','Houston','Texas','Public','https://www.uh.edu/undergraduate-admissions/apply/freshman/',None,None,None,'University of Houston freshman admissions'),
('ut','University of Texas at Austin','Austin','Texas','Public','https://admissions.utexas.edu/apply/freshman/',None,'Application, supplemental materials and academic records','Fall early action Oct 15; regular Dec 1','UT Austin freshman admissions'),
('baylor','Baylor University','Waco','Texas','Private','https://admissions.web.baylor.edu/admission',None,None,None,'Baylor undergraduate admissions'),
('smu','Southern Methodist University','Dallas','Texas','Private','https://www.smu.edu/admission/apply',None,None,None,'SMU admissions'),
('ttu','Texas Tech University','Lubbock','Texas','Public','https://www.depts.ttu.edu/admissions/apply/status/first_freshmen/','Test-optional admission pathway offered','Common App or ApplyTexas, transcript, application fee','Check official entry-year timeline','Texas Tech first-time freshman'),
('unt','University of North Texas','Denton','Texas','Public','https://admissions.unt.edu/freshman',None,None,None,'UNT freshman admissions'),
('txst','Texas State University','San Marcos','Texas','Public','https://www.admissions.txst.edu/future-students/freshman/admission-requirements.html','Top 75% class rank: SAT/ACT generally not required; other rules apply','High-school curriculum and transcripts','Fall 2027 priority Dec 1, 2026; final dates vary by applicant category','Texas State freshman requirements'),
('princeton','Princeton University','Princeton','New Jersey','Private','https://admission.princeton.edu/apply/first-year-application-dates-deadlines',None,'Common Application, Princeton questions, graded written paper, school materials','SCEA Nov 1; RD Jan 1','Princeton application dates'),
('duke','Duke University','Durham','North Carolina','Private','https://admissions.duke.edu/first-year-applicants/','SAT/ACT optional for listed cycle','Common Application, transcript, counselor and two teacher recommendations','ED Nov 2; RD Jan 4 (listed cycle)','Duke first-year applicants'),
('purdue','Purdue University','West Lafayette','Indiana','Public','https://admissions.purdue.edu/become-student/apply/',None,'Common Application for West Lafayette/Indianapolis','Fall application available Aug 1–Jan 15; program priority dates may differ','Purdue apply'),
]
FIELDS = ('slug','name','city','state','type','admissions_url','testing','documents','deadlines','source_name')
CATALOG = {row[0]: dict(zip(FIELDS,row)) for row in SCHOOLS}
for obj in CATALOG.values():
    obj['review_date'] = REVIEW_DATE if any(obj.get(k) for k in ('testing','documents','deadlines')) else None
    obj['english'] = 'Check international admissions and English proficiency policy on official website'
    obj['tuition'] = 'Verify current cost of attendance for your residency and entry year'
    obj['aid'] = 'Check domestic/international financial aid and scholarship eligibility with university'
    obj['majors'] = 'Check university program catalog and program-specific admission rules'
    obj['applicant_note'] = 'First-year undergraduate planning reference; transfer and graduate admission may differ.'
CATALOG['uta']['english'] = 'International: TOEFL 79 (120-scale), IELTS 6.5, Duolingo 100 (non-engineering) / 105 (engineering), per official international-first-year page.'
CATALOG['uta']['international_url'] = 'https://www.uta.edu/admissions/apply/international-undergraduate/international-freshmen'
CATALOG['txst']['international_url'] = 'https://www.admissions.txst.edu/future-students/priority_dates.html'
CATALOG['rice']['international_url'] = 'https://admission.rice.edu/apply/first-year-international-applicants'
