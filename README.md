# Ithaca — Your Journey to Your Dream University

Ithaca is a Flask web application for students organizing their college preparation. Students can set academic goals, choose universities, follow five preparation areas, and complete daily quests that earn XP.

## Running on Windows

1. Open the `ithaca` folder in Visual Studio Code.
2. Open **Terminal → New Terminal**.
3. Create an environment if necessary: `py -m venv .venv`.
4. Install dependencies: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
5. Start the application: `.\.venv\Scripts\python.exe app.py`.
6. Visit `http://127.0.0.1:5000` in a browser.
7. Press **Ctrl+C** in the terminal to stop the application.

## Features

- Choose Grades 9–12 and a general preparation route or up to three university goals.
- Set an academic interest, weekly study time, optional GPA, intended entry year, and scholarship priority.
- Edit the student profile without rebuilding the journey.
- Explore academics, exams, achievements, applications, and scholarships as separate preparation areas.
- Complete daily quests to earn XP and level up.
- Keep quest progress in browser local storage. Progress from the original single-university format is carried over when available.

## Development notes

- University names are user-entered destinations. There is no live admissions verification or automatic requirements comparison yet.
- XP rewards task completion; it does not measure academic performance or admission chances.
- Profile details are stored in Flask's browser session cookie. Quest completion is stored in the same browser's local storage. This is suitable for local testing only, not for real student accounts or sensitive data.
- This app has no authentication or production security configuration. It should not be used with real minors' personal data or deployed publicly without appropriate privacy and security controls.
- The built-in Flask server and fallback secret key are only for local development. Configure a secure secret and disable debugging before deployment.

## Credits and disclosures

The initial application scaffolding and code suggestions were developed with assistance from ChatGPT. Additional libraries, assets, or reused code should be attributed according to their licenses. Disclose AI assistance and third-party components in the hackathon submission according to organizer requirements.

## University planning

Open **Compare university paths** from the journey dashboard, or select any of the five islands.
The comparison includes official admissions/financial-aid links for Stanford, MIT, and Rice, plus a preparation checklist. Students can switch between international and U.S. domestic financial-aid summaries. The preparation checklist saves separately in browser local storage and does not add XP. Universities outside the reference catalog are explicitly marked as needing research; the site does not invent their requirements.

The reference information was reviewed on November 14, 2026. Published policies may change. Deadlines and eligibility must be reconfirmed for the student's actual admission year and individual circumstances. The site does not calculate admission probabilities or determine eligibility. Selected universities are currently a planning aid; fully automated source retrieval is not implemented.

Official sources referenced:

- Stanford first-year admission: https://admission.stanford.edu/apply/first-year/
- Stanford undergraduate aid: https://financialaid.stanford.edu/undergrad/apply/index.html
- MIT first-year admission: https://mitadmissions.org/apply/firstyear/deadlines-requirements/
- MIT undergraduate aid: https://sfs.mit.edu/undergraduate-students/apply-for-aid/deadlines-process/
- Rice international first-year admission: https://admission.rice.edu/apply/first-year-international-applicants
- Rice domestic first-year admission: https://admission.rice.edu/apply/first-year-domestic-applicants
- Rice international aid: https://financialaid.rice.edu/apply-aid/international-students
- Rice financial aid: https://financialaid.rice.edu/

## Academic practice and progress

The **Exams** island now opens an eight-question skills check. Practice sets A and B each cover numbers and proportions, algebra and functions, reading comprehension, and evidence-based reasoning. The questions are original to Ithaca; they are not official SAT, ACT, IELTS, or TOEFL items.

After submitting a full set, students see their score, topic breakdown, correct answers, explanations, and suggested study areas. Results are saved in the browser's local storage, which also powers **My progress** and the journey dashboard's latest-practice summary. Scores are separate from quest XP.

Use the same browser and address (`http://127.0.0.1:5000`) to retain the existing quest completions, preparation checklist, and practice history. Clearing site data or switching browsers will erase local progress. There is no account synchronization or database in this version.

The two practice sets cover the same topic categories but have not been statistically equated for difficulty. Results are formative feedback, not standardized scores, validated proficiency measurements, admissions predictions, or evidence of scholarship eligibility.

To test: create a student profile; open **Academic practice**; complete all eight questions in set A; submit; review explanations; visit **My progress**; then complete set B and confirm both attempts appear after refreshing. The `/api/assessment/grade` route checks answers on the server. A local development server is sufficient for testing but should not be publicly deployed with debug enabled.

## Athena — Gemini-powered planning

Use **Open Athena** on the dashboard, or navigate to `http://127.0.0.1:5000/athena`.

1. Create a Gemini API key at https://aistudio.google.com/apikey.
2. In the same folder as `app.py`, make an `.env` file from `.env.example` using PowerShell: `Copy-Item .env.example .env`.
3. Open `.env` in VS Code and replace `PASTE_YOUR_API_KEY_HERE` with the real key. Do not add quotes or spaces around the equals sign. The model is configurable with `GEMINI_MODEL` (default `gemini-3.5-flash-lite`).
4. Install new dependencies in your existing virtual environment: `.\.venv\Scripts\python.exe -m pip install -r requirements.txt`.
5. Restart Flask: `.\.venv\Scripts\python.exe app.py`.
6. Open Athena, choose a situation, check the data-sharing consent box, and click **Build my journey**. You need an internet connection and a valid Gemini API key. Provider usage may incur cost or rate limits.
7. Use **Poseidon's Storm — I missed a week** to generate an adjusted plan. After generating, open the dashboard to complete the personalized quests.

Never paste the API key into ChatGPT, commit it to GitHub, or place it in HTML/JavaScript. `.env` is ignored by Git. If you accidentally publish a key, revoke it in Google AI Studio and create another.

### How Athena works

The Flask backend requests an AI-generated study plan using Google's `google-genai` Python SDK. The request includes the selected universities, grade, study time, academic interest, funding priority, and **the latest topic-level results of the short practice check** if available. It does not send question responses, names, email addresses, or an entire assessment history. The user must choose to send that context before each request.

Athena returns university preparation milestones and four concrete quests. The selected plan is saved in this browser's `localStorage`; new plans replace the old active plan. Completed personalized quests can earn 10 XP each, capped at 30 AI quest XP per day across plan changes. Previous standard quest XP and practice history are retained. The score is a motivational game mechanic, not evidence of verified learning or admission readiness.

Plans are *suggestions*, not verified university regulations. The Gemini API does not browse or independently verify current official admissions policies in this version. The app does not generate admission probabilities, claim scholarship eligibility, or treat original practice questions as official examinations. Review official admissions and aid links separately before using any university-specific advice.

This version still uses a local browser session and local storage, without accounts, server persistence, permission controls, or protections appropriate for real minors' records. **Only use fictional/non-sensitive student details.** For a public deployment, provide actual account security, privacy controls, secure secret management, HTTPS, rate limiting and database access controls.

## MongoDB Atlas — saved progress

This local version optionally backs up the browser's learning history to MongoDB Atlas. It continues to work when MongoDB is not configured or temporarily unavailable.

### Connect Atlas

1. Create an Atlas account at https://www.mongodb.com/cloud/atlas/register and create a free cluster if one is available to your account and region.
2. In **Database Access**, create a **database user** with a strong password. This is different from your Atlas login. For local development, grant the user read/write access to the project's database only where the console supports it.
3. In **Network Access**, choose **Add Current IP Address**. Avoid granting public access to all IP addresses.
4. On your cluster, select **Connect** → **Drivers** → **Python** to copy the connection string.
5. In the existing `.env` next to `app.py`, add:

   ```dotenv
   MONGODB_URI=mongodb+srv://YOUR_DATABASE_USER:YOUR_DATABASE_PASSWORD@YOUR-CLUSTER.mongodb.net/?retryWrites=true&w=majority
   MONGODB_DB=ithaca
   ```

   Keep your existing `GEMINI_API_KEY` and `GEMINI_MODEL` lines. **Do not replace the whole `.env` file or share it.** Replace the URI with the precise connection string Atlas supplies. If your password contains reserved URL characters (such as `@`, `:`, `/`, `#`, `%`), URL-encode it or create a strong password without those characters for this local setup.
6. Run `python -m pip install -r requirements.txt` inside your project's environment. Run `python database_status.py` to test Atlas connectivity and database write/read/delete access.
7. Restart Flask, open the site at `http://127.0.0.1:5000`, and visit **My Odyssey**. The storage status will show when both browser and Atlas saves are active.
8. Complete a quest or practice set, then open Atlas **Browse Collections** / **Data Explorer** and view the `ithaca` database. The `profiles` and `progress` collections are created automatically by the first writes. The `progress` collection contains a `state` object with assessment history, quest completion, and latest Athena plan. Database names and navigation may differ slightly depending on the Atlas UI version.

### Data handling and limitations

- Browser storage remains the working copy so the app is usable offline or if Atlas is unreachable. When the page loads and Atlas is connected, existing local entries are merged with the cloud backup and uploaded. In particular, saved assessment attempts and XP are preserved; a completed quest stays complete, even after refreshing.
- A completed quest is locked to avoid repeated XP awards. The old **Reset quests** button was removed. Atlas saves the latest state, including changes to the active Athena plan.
- This is an **individual, local demonstration** without a login or production account security. The database records are linked to a random identifier in a signed Flask browser session. This is **not** suitable for deployment with real minors' records, personally identifying student details, or sensitive financial information. Use fictional test profiles only.
- Server credentials remain in `.env`. MongoDB connection details must never be placed in browser scripts, screenshots, GitHub, or shared with other participants.
- If Atlas is not configured, the application still runs with browser-only storage. If Atlas becomes unavailable, browser progress is retained, but cloud backup will resume after the next successful page load. Use the same browser and local URL to preserve the existing profile and records.
- The generated plans are study suggestions, not authoritative admissions rules. Official admission and scholarship policies still need independent verification.

The project uses PyMongo, MongoDB's Python driver. Official resources: https://www.mongodb.com/docs/atlas/driver-connection/ and https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/.
