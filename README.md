# Ithaca — Your Journey to Your Dream University

Ithaca is a Flask web application designed to help high school students organize their journey toward university admission.

Students can set academic goals, explore university preparation requirements, complete academic practice questions, track progress, and earn XP through daily quests.

Ithaca also includes Athena, a Gemini-powered AI study planning assistant, and optional MongoDB Atlas synchronization to save learning progress.

## Features

### 1. Personalized University Journey

- Choose your current grade from Grades 9–12.
- Select a general preparation route or up to three university goals.
- Set academic interests and weekly study time.
- Enter optional GPA, intended university entry year, and scholarship priority.
- Edit your profile without rebuilding your journey.
- Explore preparation areas through an interactive journey.

### 2. Five Preparation Areas

Ithaca organizes university preparation into five areas:

1. Academics
2. Exams
3. Achievements
4. Applications
5. Scholarships

Students can explore each area and complete preparation activities.

### 3. University Planning and Comparison

The university planning features include:

- A University Explorer with a curated catalog of 20 U.S. universities.
- University profiles and side-by-side comparison of selected universities.
- Preparation checklists and official admission and financial aid links where available.
- Reference information about application documents, testing, costs, and financial aid; details vary by university and applicant type.
- Guidance for U.S. domestic and international applicants and for researching schools outside the curated catalog.

Students can open **Explore Universities** or **Compare university paths** from My Odyssey. More detailed profiles and comparisons are available through the University Explorer.

University information is a planning reference, not a live admissions database. Ithaca does not automatically verify current requirements, determine admission eligibility, calculate admission probabilities, or guarantee scholarships. Always check the university's official website.

### 4. Academic Practice and Exam Preparation

**General Skills:** The original eight-question academic check remains available as practice Sets A and B. These cover:

- Numbers and proportions
- Algebra and functions
- Reading comprehension
- Evidence-based reasoning

**Exam Preparation Center:** A separate practice area is available for:

- Digital SAT
- ACT
- TOEFL iBT
- IELTS Academic
- Duolingo English Test (DET)

The final local prototype includes **100 original exam-category questions (20 per exam)**, in addition to the General Skills questions. Practice is organized by topic and difficulty (**Foundation**, **Intermediate**, **Advanced**, and **Mixed**), with eight-question sets. The app prioritizes questions not previously seen in that browser where possible, but can reuse questions as the bank is exhausted.

Students can open the Exam Center at:

[http://127.0.0.1:5000/exam-center](http://127.0.0.1:5000/exam-center)

After answering, students can review their score, performance by topic, correct answers, explanations, and suggested areas for further practice. The Exam Center links to official exam-provider preparation resources, including College Board and Khan Academy for SAT preparation.

These are **original Ithaca short-form exercises**, not copied official test questions. They do not simulate every exam section or question type (for example, speaking or listening), and results are **not** official scores, score predictions, or admission-readiness measures.

General Skills and exam-category attempts are saved in browser storage and can be included in optional MongoDB Atlas progress synchronization. My Progress displays both kinds of history.

### 5. Athena — Gemini-Powered AI Planning

Athena is an AI-powered academic planning assistant using Google's Gemini API. Students can open Athena from My Odyssey or visit:

[http://127.0.0.1:5000/athena](http://127.0.0.1:5000/athena)

With the student's consent, Athena uses selected profile and academic practice information to suggest:

- AI-generated study milestones and academic recommendations.
- Four actionable study quests in each generated plan.
- University preparation steps aligned with selected goals and study time.
- Study priorities informed by the latest General Skills check and up to five recent exam-category practice summaries when available.
- Adjusted plans for situations such as **Poseidon's Storm — I missed a week**.

Athena quests appear in My Odyssey and can be marked completed there. Generating a new plan uses a Gemini API request; **daily route suggestions reuse existing saved data without an additional Gemini request**.

Athena requests consent before sending selected planning information to Gemini. AI-generated recommendations are suggestions, not verified university policies, and students must verify official requirements independently.

### 6. Gamification, XP, and My Odyssey

Ithaca uses daily activities and Athena quests to motivate consistent study:

- **My Odyssey** displays the journey, universities, academic practice, Athena's current quests, level, and XP progress.
- **Three daily quests** can be completed once per local calendar day; their completion status resets on the next day the app is opened or refreshed.
- A **personalized daily route** recommends study activities using saved weak exam topics and unfinished Athena quests. Suggestions are selected locally and can link to focused practice.
- **Athena quests** award **10 XP per eligible completion**, up to **30 Athena XP per day**. The interface explains when the daily limit is reached or a completion is not rewarded.
- An XP event ledger records awarded rewards and guards against duplicate XP for the same task instance.
- Levels increase every **50 total XP**: Level 1 begins at 0 XP, Level 2 at 50 XP, and so on.
- Completion history and XP are shown in My Progress and can be included in optional MongoDB synchronization.

The daily route is selected once per device-local day so it stays stable during the day. Daily quest completion is self-reported, and the date-based reset uses the device's clock. Athena does **not** automatically call Gemini or generate a new AI plan at midnight.

XP is a motivational feature and does not represent academic proficiency or university admission readiness. The app protects against duplicate rewards, but it is not designed as an anti-cheat or verified study-time system.

### 7. Progress Tracking

**My Progress** combines the original General Skills assessments with SAT, ACT, TOEFL, IELTS, and DET practice history. It includes:

- Saved attempts and recent scores by exam category.
- Topic performance, accuracy, and areas to strengthen.
- Daily and Athena quest completion records.
- Total XP, current level, and activity-related progress.
- The currently saved Athena study plan and completed quest state.

Browser localStorage is the primary working copy. Supported records can synchronize to MongoDB Atlas when connected. No full user account authentication system is included in this version.

### 8. MongoDB Atlas Synchronization

Ithaca supports optional MongoDB Atlas integration to back up selected learning progress while continuing to work locally when MongoDB is unavailable.

Supported synced information includes:

- General Skills and exam-category practice attempts.
- Quest completion and the XP event ledger.
- Saved Athena plan and quest state.
- Other supported journey progress fields.

The main application collections include `profiles` and `progress`; the database may also contain diagnostic collections such as `connection_checks` from connection testing. The `progress` collection stores a state object containing supported browser history.

Data is associated with a session identifier, **not a verified user account**. This is intended for a local demonstration, not production multi-user storage.

## Technology Stack

**Backend**

- Python
- Flask

**Frontend**

- HTML
- CSS
- JavaScript

**Artificial Intelligence**

- Google Gemini API
- Google GenAI Python SDK

**Database**

- MongoDB Atlas
- PyMongo

**Other Technologies**

- Browser localStorage
- Flask sessions
- Git
- GitHub

## Project Structure

Selected files and directories in the final local prototype (not an exhaustive listing):

```text
ithaca/
├── app.py
├── assessment_data.py
├── athena.py
├── athena_context.py
├── database.py
├── database_status.py
├── exam_practice.py
├── exam_practice_data.py
├── exam_practice_more.py
├── university_data.py
├── university_explorer.py
├── university_profiles.py
├── university_profiles_data.py
├── requirements.txt
├── README.md
├── QUICK_START.md
├── .env.example
├── .gitignore
├── static/
│   ├── style.css
│   ├── sync.js
│   ├── gamification.js
│   ├── gamification.css
│   ├── exam_center.css
│   ├── unified_progress.js
│   ├── unified_progress.css
│   ├── final_release.js
│   └── final_release.css
└── templates/
    ├── index.html
    ├── journey.html
    ├── requirements.html
    ├── assessment.html
    ├── exam_center.html
    ├── exam_quiz.html
    ├── progress.html
    ├── athena.html
    ├── explorer.html
    ├── university_profile.html
    └── university_profiles.html
```

## Running on Windows

### Step 1 — Clone the Repository

```
git clone https://github.com/05Winel05/ithaca.git
cd ithaca
```

Alternatively, open an existing copy of the `ithaca` folder in Visual Studio Code.

### Step 2 — Create a Virtual Environment

```
py -m venv .venv
```

### Step 3 — Install Dependencies

```
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Create a `.env` file using the example:

```
Copy-Item .env.example .env
```

Open `.env` in VS Code and configure:

```
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=YOUR_MODEL_NAME

MONGODB_URI=YOUR_MONGODB_CONNECTION_STRING
MONGODB_DB=ithaca
```

Replace the placeholder values with your actual configuration.

Never share the real `.env` file or commit it to GitHub.

Gemini requires an API key and internet connection. MongoDB Atlas synchronization is optional.

### Step 5 — Start Flask

```
.\.venv\Scripts\python.exe app.py
```

### Step 6 — Open the Application

Visit:

[http://127.0.0.1:5000](http://127.0.0.1:5000/)

### Step 7 — Stop the Application

Press **Ctrl+C** in the terminal.

## Configuring Gemini AI

1. Visit [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Create a Gemini API key.
3. Add the key to your `.env` file.
4. Configure `GEMINI_MODEL` for a model available to your API key.
5. Install dependencies and restart Flask.
6. Open Athena from the application dashboard.
7. Choose a planning situation.
8. Review and accept the data-sharing consent.
9. Click **Build my journey**.

Athena generates a personalized study plan and quests.

The API may have usage limits or associated costs.

### How Athena Works

The Flask backend communicates with Gemini through the Google GenAI Python SDK.

With consent, Athena can send:

- Selected universities
- Current grade
- Study time
- Academic interests
- Scholarship priority
- Latest General Skills topic-level results, when available
- Up to five recent exam-category practice summaries, when available

The application does not intentionally send names, email addresses, individual question responses, or the complete assessment history to Gemini. Only selected recent practice summaries are included with consent.

Generated plans are saved in browser local storage and may be included in MongoDB progress backups when enabled.

New plans replace the current active plan.

## Configuring MongoDB Atlas

### Step 1 — Create a MongoDB Account

Visit:

[https://www.mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)

Create an Atlas account and database cluster.

### Step 2 — Create a Database User

Under **Database Access**, create a database user with a strong password.

Use database-specific read/write permissions where supported.

### Step 3 — Configure Network Access

Open **Network Access** and add your current IP address.

Avoid allowing unrestricted access from every IP address.

### Step 4 — Copy the Connection String

Open your cluster and select:

**Connect → Drivers → Python**

Copy the connection string provided by MongoDB Atlas.

### Step 5 — Configure `.env`

Add:

```
MONGODB_URI=mongodb+srv://YOUR_DATABASE_USER:YOUR_DATABASE_PASSWORD@YOUR-CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=ithaca
```

Replace all placeholders with the appropriate values.

If the password contains reserved URL characters, it must be URL-encoded.

Keep the Gemini configuration in the same `.env` file.

### Step 6 — Test MongoDB

Install the project dependencies if needed:

```
python -m pip install -r requirements.txt
```

Run:

```
python database_status.py
```

A successful test confirms connectivity and database read, write, and delete access.

### Step 7 — Test Synchronization

1. Start the Flask application.
2. Open [http://127.0.0.1:5000](http://127.0.0.1:5000/).
3. Create a fictional student profile.
4. Complete a quest or academic practice set.
5. Open My Progress.
6. Check the storage synchronization status.
7. Open MongoDB Atlas Data Explorer.
8. Check the `profiles` and `progress` collections.
9. Refresh the application and confirm progress is preserved.

The application remains usable with browser storage if MongoDB is not configured or temporarily unavailable.

## Testing the Application

### Student Journey

1. Open Ithaca.
2. Select a grade.
3. Choose university goals.
4. Enter academic interests and study time.
5. Create the student journey.
6. Explore the five preparation areas.

### Academic Practice

1. Open the Exams area.
2. Start practice set A.
3. Complete all eight questions.
4. Submit answers.
5. Review the score and explanations.
6. Open My Progress.
7. Complete practice set B.
8. Confirm that both attempts are saved.
9. Open `/exam-center` and select SAT, ACT, TOEFL, IELTS, or DET.
10. Try an Advanced eight-question set, check explanations, and verify the new attempt in My Progress.

### Athena AI

1. Open Athena.
2. Select a planning situation.
3. Give consent to share selected planning information.
4. Generate a study plan.
5. Review personalized milestones.
6. Complete an AI-generated quest.
7. Test Poseidon's Storm to adjust the plan.
8. Return to My Odyssey, mark a quest complete, and check XP and completion feedback.

### MongoDB Synchronization

1. Confirm MongoDB connectivity.
2. Complete a quest or practice set.
3. Check the synchronization status.
4. Verify records in Atlas Data Explorer, including exam history and the `ithaca-xp-ledger-v1` state when present.
5. Refresh the application.
6. Confirm progress remains available.

Use fictional and non-sensitive profile data during testing.

## Data Storage and Privacy

Ithaca uses several storage mechanisms.

**Flask Session**

Stores profile information in a signed browser session cookie.

**Browser Local Storage**

Stores progress such as quests, practice attempts, and current Athena plan information.

**MongoDB Atlas**

Optionally backs up supported application data.

The application currently does not provide full user registration, authentication, or production-grade access controls.

Records are associated with a random identifier in the signed Flask browser session.

This approach is intended only for a local demonstration.

Do not use real minors' personal information, sensitive educational records, or financial details.

## Current Limitations

- University information is not automatically retrieved or verified in real time.
- University admission probabilities are not calculated.
- Scholarship eligibility is not automatically determined.
- Academic practice questions are not official standardized examination questions.
- Practice sets have not been statistically equated or validated.
- The five exam categories use limited original short-form exercises and do not reproduce full standardized exams.
- Daily quest resets use the device-local calendar day, and completed activities are self-reported.
- AI recommendations may contain inaccurate or outdated information.
- MongoDB synchronization does not provide authenticated multi-user accounts.
- Browser data can be lost if local storage is cleared.
- Production-level privacy, security, and account management are not implemented.
- The built-in Flask development server is not intended for public production deployment.

Before a public deployment, the application would require appropriate authentication, privacy protection, HTTPS, rate limiting, secure secret management, database access controls, and production server configuration.

Debug mode should be disabled in production.

## Official University References

The reference university information was reviewed on November 14, 2026. Policies and deadlines may change.

### Stanford University

First-year admission:

[https://admission.stanford.edu/apply/first-year/](https://admission.stanford.edu/apply/first-year/)

Undergraduate financial aid:

[https://financialaid.stanford.edu/undergrad/apply/index.html](https://financialaid.stanford.edu/undergrad/apply/index.html)

### Massachusetts Institute of Technology (MIT)

First-year admission:

[https://mitadmissions.org/apply/firstyear/deadlines-requirements/](https://mitadmissions.org/apply/firstyear/deadlines-requirements/)

Undergraduate financial aid:

[https://sfs.mit.edu/undergraduate-students/apply-for-aid/deadlines-process/](https://sfs.mit.edu/undergraduate-students/apply-for-aid/deadlines-process/)

### Rice University

International admission:

[https://admission.rice.edu/apply/first-year-international-applicants](https://admission.rice.edu/apply/first-year-international-applicants)

Domestic admission:

[https://admission.rice.edu/apply/first-year-domestic-applicants](https://admission.rice.edu/apply/first-year-domestic-applicants)

International financial aid:

[https://financialaid.rice.edu/apply-aid/international-students](https://financialaid.rice.edu/apply-aid/international-students)

Financial aid:

[https://financialaid.rice.edu/](https://financialaid.rice.edu/)

Students should verify all deadlines, admission requirements, and financial aid policies directly through official university websites.

## Credits and Disclosures

Ithaca was developed with assistance from ChatGPT, including application scaffolding, code suggestions, and iterative feature upgrades.

The project uses Google's Gemini API for AI-powered academic planning and MongoDB Atlas for optional progress backup.

Third-party libraries, assets, and reused code should be credited according to their applicable licenses.

AI assistance and third-party components should also be disclosed in the HackUTA submission according to organizer requirements.

## GitHub Repository

[https://github.com/05Winel05/ithaca](https://github.com/05Winel05/ithaca)

## Project Purpose

Ithaca aims to make university preparation more organized, interactive, and motivating.

By combining university planning, academic practice, personalized AI suggestions, daily quests, and progress tracking, the project demonstrates how technology can support students as they prepare for their educational goals.

The current version is a functional local prototype intended for demonstration and further development.