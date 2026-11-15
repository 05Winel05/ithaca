
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

The university planning feature includes:

- University preparation checklists.
- Official admission and financial aid links.
- Reference information for Stanford, MIT, and Rice University.
- International and U.S. domestic financial aid summaries.
- Guidance for researching universities outside the reference catalog.

Students can open **Compare university paths** from the journey dashboard or select one of the five islands.

University information is provided as a planning reference. Ithaca does not automatically verify admission eligibility or calculate admission probabilities.

### 4. Academic Practice

The Exams area includes an eight-question academic skills check.

Practice sets A and B cover:

- Numbers and proportions
- Algebra and functions
- Reading comprehension
- Evidence-based reasoning

After completing a practice set, students can view:

- Total score
- Performance by topic
- Correct answers
- Answer explanations
- Suggested study areas

Results are saved locally in the browser and can optionally be backed up through MongoDB Atlas.

The My Progress page displays previous assessment attempts and learning history.

These questions are original to Ithaca and are not official SAT, ACT, IELTS, TOEFL, or Duolingo English Test questions.

Practice scores are intended for learning feedback, not standardized proficiency measurement or admission predictions.

### 5. Athena — Gemini-Powered AI Planning

Athena is an AI-powered academic planning assistant that uses Google's Gemini API.

Students can open Athena from the dashboard or visit:

http://127.0.0.1:5000/athena

Athena uses selected student information to generate personalized preparation plans.

Features include:

- AI-generated study milestones
- Personalized academic recommendations
- Four actionable study quests
- Planning based on selected universities and goals
- Consideration of recent academic practice performance
- Plan adjustment through Poseidon's Storm

**Poseidon's Storm — I missed a week**

This feature helps students adjust their preparation plan after falling behind.

Athena requests user consent before sending selected planning information to Gemini.

Generated recommendations are suggestions, not verified university policies.

### 6. Gamification and XP

Ithaca uses a quest and XP system to encourage students to stay consistent.

Features include:

- Daily quests
- XP rewards for completing quests
- Student levels
- Personalized Athena quests
- Progress tracking
- Completed quest history

Personalized Athena quests award 10 XP each, with a maximum of 30 AI quest XP per day.

The same completed quest cannot repeatedly award XP.

XP is a motivational feature and does not represent academic proficiency or university admission readiness.

### 7. Progress Tracking

The My Progress area helps students monitor their activities.

It includes:

- Completed quests
- XP and level progress
- Academic practice history
- Recent practice performance
- Personalized Athena plan progress

The browser uses local storage to preserve learning history.

When MongoDB Atlas is configured, the application can additionally synchronize and back up supported progress information.

There is no full user account authentication system in this version.

### 8. MongoDB Atlas Synchronization

Ithaca supports optional MongoDB Atlas integration.

The application uses MongoDB to back up learning progress while keeping the browser as the working copy.

Features include:

- Optional cloud progress backup
- Synchronization of supported quest and assessment data
- Preservation of completed quests
- Saved practice attempts
- Saved Athena plan state
- Browser-only operation when MongoDB is unavailable

MongoDB uses two collections:

- `profiles`
- `progress`

The `progress` collection stores a state object containing supported learning history.

Database integration is designed for local demonstration rather than production student accounts.

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

```text
ithaca/
├── app.py
├── assessment_data.py
├── athena.py
├── database.py
├── database_status.py
├── university_data.py
├── requirements.txt
├── README.md
├── QUICK_START.md
├── .env.example
├── .gitignore
├── static/
│   ├── style.css
│   └── sync.js
└── templates/
    ├── index.html
    ├── journey.html
    ├── requirements.html
    ├── assessment.html
    ├── progress.html
    └── athena.html
```

## Running on Windows

### Step 1 — Clone the Repository

```powershell
git clone https://github.com/05Winel05/ithaca.git
cd ithaca
```

Alternatively, open an existing copy of the `ithaca` folder in Visual Studio Code.

### Step 2 — Create a Virtual Environment

```powershell
py -m venv .venv
```

### Step 3 — Install Dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### Step 4 — Configure Environment Variables

Create a `.env` file using the example:

```powershell
Copy-Item .env.example .env
```

Open `.env` in VS Code and configure:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GEMINI_MODEL=YOUR_MODEL_NAME

MONGODB_URI=YOUR_MONGODB_CONNECTION_STRING
MONGODB_DB=ithaca
```

Replace the placeholder values with your actual configuration.

Never share the real `.env` file or commit it to GitHub.

Gemini requires an API key and internet connection. MongoDB Atlas synchronization is optional.

### Step 5 — Start Flask

```powershell
.\.venv\Scripts\python.exe app.py
```

### Step 6 — Open the Application

Visit:

http://127.0.0.1:5000

### Step 7 — Stop the Application

Press **Ctrl+C** in the terminal.

## Configuring Gemini AI

1. Visit https://aistudio.google.com/apikey
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
- Latest topic-level practice results, when available

The application does not intentionally send names, email addresses, individual question responses, or the complete assessment history to Gemini.

Generated plans are saved in browser local storage and may be included in MongoDB progress backups when enabled.

New plans replace the current active plan.

## Configuring MongoDB Atlas

### Step 1 — Create a MongoDB Account

Visit:

https://www.mongodb.com/cloud/atlas/register

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

```env
MONGODB_URI=mongodb+srv://YOUR_DATABASE_USER:YOUR_DATABASE_PASSWORD@YOUR-CLUSTER.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB=ithaca
```

Replace all placeholders with the appropriate values.

If the password contains reserved URL characters, it must be URL-encoded.

Keep the Gemini configuration in the same `.env` file.

### Step 6 — Test MongoDB

Install the project dependencies if needed:

```powershell
python -m pip install -r requirements.txt
```

Run:

```powershell
python database_status.py
```

A successful test confirms connectivity and database read, write, and delete access.

### Step 7 — Test Synchronization

1. Start the Flask application.
2. Open http://127.0.0.1:5000.
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

### Athena AI

1. Open Athena.
2. Select a planning situation.
3. Give consent to share selected planning information.
4. Generate a study plan.
5. Review personalized milestones.
6. Complete an AI-generated quest.
7. Test Poseidon's Storm to adjust the plan.

### MongoDB Synchronization

1. Confirm MongoDB connectivity.
2. Complete a quest or practice set.
3. Check the synchronization status.
4. Verify records in Atlas Data Explorer.
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

https://admission.stanford.edu/apply/first-year/

Undergraduate financial aid:

https://financialaid.stanford.edu/undergrad/apply/index.html

### Massachusetts Institute of Technology (MIT)

First-year admission:

https://mitadmissions.org/apply/firstyear/deadlines-requirements/

Undergraduate financial aid:

https://sfs.mit.edu/undergraduate-students/apply-for-aid/deadlines-process/

### Rice University

International admission:

https://admission.rice.edu/apply/first-year-international-applicants

Domestic admission:

https://admission.rice.edu/apply/first-year-domestic-applicants

International financial aid:

https://financialaid.rice.edu/apply-aid/international-students

Financial aid:

https://financialaid.rice.edu/

Students should verify all deadlines, admission requirements, and financial aid policies directly through official university websites.

## Credits and Disclosures

Ithaca was developed with assistance from ChatGPT, including application scaffolding and code suggestions.

The project uses Google's Gemini API for AI-powered academic planning and MongoDB Atlas for optional progress backup.

Third-party libraries, assets, and reused code should be credited according to their applicable licenses.

AI assistance and third-party components should also be disclosed in the HackUTA submission according to organizer requirements.

## GitHub Repository

https://github.com/05Winel05/ithaca

## Project Purpose

Ithaca aims to make university preparation more organized, interactive, and motivating.

By combining university planning, academic practice, personalized AI suggestions, daily quests, and progress tracking, the project demonstrates how technology can support students as they prepare for their educational goals.

The current version is a functional local prototype intended for demonstration and further development.
