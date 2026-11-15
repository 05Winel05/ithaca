"""Original practice questions and scoring for academic skill checks."""

TOPICS = {
    "numeracy": {"title": "Numbers & proportions", "area": "Mathematics",
                 "advice": "Practice percentages, fractions, and ratio problems. Explain each calculation before checking your answer."},
    "algebra": {"title": "Algebra & functions", "area": "Mathematics",
                "advice": "Work through equations and function rules step by step. Check your solution by substituting it back."},
    "reading": {"title": "Reading comprehension", "area": "Reading & reasoning",
                "advice": "Read short passages and summarize their main claim. Highlight what the passage does and does not prove."},
    "evidence": {"title": "Evidence & reasoning", "area": "Reading & reasoning",
                 "advice": "Distinguish observations from conclusions. Ask what additional evidence would strengthen or weaken a claim."},
}

FORMS = {
    "A": [
        {"id": "a01", "topic": "numeracy", "text": "What is three-fourths of 28?", "options": ["18", "21", "24", "25"], "correct": 1, "explanation": "28 ÷ 4 = 7, and 7 × 3 = 21."},
        {"id": "a02", "topic": "numeracy", "text": "18 students make up 30% of a group. How many students are in the full group?", "options": ["36", "48", "54", "60"], "correct": 3, "explanation": "30% of the total is 18, so the total is 18 ÷ 0.30 = 60."},
        {"id": "a03", "topic": "algebra", "text": "Solve for x: 3x + 7 = 22.", "options": ["3", "5", "7", "9"], "correct": 1, "explanation": "Subtract 7 from each side, then divide 15 by 3: x = 5."},
        {"id": "a04", "topic": "algebra", "text": "If f(x) = 2x² − 3, what is f(3)?", "options": ["9", "12", "15", "33"], "correct": 2, "explanation": "Substitute 3: 2 × 3² − 3 = 18 − 3 = 15."},
        {"id": "a05", "topic": "reading", "passage": "A school garden team counted butterflies each morning. Visits increased after the team planted more flowers. The team also noticed that the weather became warmer during the same period.", "text": "Which conclusion best fits the passage?", "options": ["Flowers definitely caused all of the increase.", "The butterfly count increased, but the cause is uncertain.", "Warm weather prevented butterflies from visiting.", "The team did not collect any observations."], "correct": 1, "explanation": "Counts increased, but both flowers and weather changed. The passage does not isolate one cause."},
        {"id": "a06", "topic": "reading", "passage": "A school garden team counted butterflies each morning. Visits increased after the team planted more flowers. The team also noticed that the weather became warmer during the same period.", "text": "Why did the writer mention warmer weather?", "options": ["To introduce another possible explanation", "To prove flowers have no effect", "To describe the team's schedule", "To explain how butterflies are counted"], "correct": 0, "explanation": "Warmer weather is a possible alternative explanation for the changing counts."},
        {"id": "a07", "topic": "evidence", "text": "After a library extended its hours, 15 of 20 surveyed visitors said the change helped them. Which statement is supported?", "options": ["All students prefer later hours.", "The library doubled its visitors.", "15 of the 20 people surveyed found the change helpful.", "Later hours increased exam grades."], "correct": 2, "explanation": "The survey supports a statement about those 20 respondents, not everyone at the school."},
        {"id": "a08", "topic": "evidence", "text": "A report says students who attend tutoring often earn higher grades. What would best help test whether tutoring caused the difference?", "options": ["The tutoring center's logo", "The number of pages in the report", "Whether the comparison accounted for prior grades and study habits", "The color of the students' notebooks"], "correct": 2, "explanation": "Prior grades and study habits may explain part of the relationship, so a fair comparison must consider them."},
    ],
    "B": [
        {"id": "b01", "topic": "numeracy", "text": "What is two-thirds of 36?", "options": ["18", "20", "24", "27"], "correct": 2, "explanation": "36 ÷ 3 = 12, then 12 × 2 = 24."},
        {"id": "b02", "topic": "numeracy", "text": "A group of 12 students represents 25% of a club. How many students are in the club?", "options": ["36", "48", "50", "60"], "correct": 1, "explanation": "25% is one quarter. Multiply 12 by 4 to get 48."},
        {"id": "b03", "topic": "algebra", "text": "Solve for y: 4y − 6 = 18.", "options": ["3", "5", "6", "8"], "correct": 2, "explanation": "Add 6 to both sides, then divide 24 by 4: y = 6."},
        {"id": "b04", "topic": "algebra", "text": "If g(x) = x² + 2x, what is g(4)?", "options": ["12", "16", "20", "24"], "correct": 3, "explanation": "Substitute 4: 4² + 2 × 4 = 16 + 8 = 24."},
        {"id": "b05", "topic": "reading", "passage": "A student club began posting reminders before its meetings. Attendance increased over three weeks, but the club also changed the meeting time to a later hour.", "text": "What is the most reasonable interpretation?", "options": ["Reminders were the only cause of higher attendance.", "Attendance grew, but more than one change might explain it.", "Changing the meeting time reduced attendance.", "The club stopped holding meetings."], "correct": 1, "explanation": "Attendance increased while both reminders and meeting times changed. A single cause has not been established."},
        {"id": "b06", "topic": "reading", "passage": "A student club began posting reminders before its meetings. Attendance increased over three weeks, but the club also changed the meeting time to a later hour.", "text": "What role does the later meeting time play in the passage?", "options": ["It is an alternative explanation for the attendance change.", "It proves reminders were ineffective.", "It shows the club had no members.", "It tells us how many reminders were posted."], "correct": 0, "explanation": "The later meeting time is another factor that could have influenced attendance."},
        {"id": "b07", "topic": "evidence", "text": "In a poll of 40 club members, 26 preferred online meetings. Which claim is justified?", "options": ["Everyone prefers online meetings.", "26 of the 40 surveyed club members preferred online meetings.", "Online meetings improve grades.", "The school must switch all classes online."], "correct": 1, "explanation": "The poll describes the sample of 40 members. It does not establish a preference for everyone."},
        {"id": "b08", "topic": "evidence", "text": "Students who use flashcards often get higher quiz scores. What would help determine whether the flashcards improved scores?", "options": ["Whether the cards have colorful borders", "Whether the school has a cafeteria", "Whether the comparison accounts for prior knowledge and study time", "Whether the flashcards fit in a pocket"], "correct": 2, "explanation": "Prior knowledge and study time can affect scores; they should be considered in a fair comparison."},
    ],
}


def public_questions(form):
    """Return questions without exposing the answer key."""
    return [{key: q[key] for key in ("id", "topic", "text", "options", "passage") if key in q} for q in FORMS[form]]


def grade_form(form, answers):
    if not isinstance(form, str) or form not in FORMS or not isinstance(answers, dict):
        raise ValueError("Invalid assessment submission.")
    questions = FORMS[form]
    expected_ids = {q["id"] for q in questions}
    if set(answers) != expected_ids:
        raise ValueError("Answer every question before submitting.")
    summary = {slug: {"title": topic["title"], "area": topic["area"], "correct": 0, "total": 0,
                      "advice": topic["advice"]} for slug, topic in TOPICS.items()}
    review = []
    total_correct = 0
    for q in questions:
        selected = answers[q["id"]]
        if type(selected) is not int or not 0 <= selected < len(q["options"]):
            raise ValueError("One or more answers are invalid.")
        correct = selected == q["correct"]
        total_correct += int(correct)
        summary[q["topic"]]["total"] += 1
        summary[q["topic"]]["correct"] += int(correct)
        review.append({"id": q["id"], "text": q["text"], "topic": TOPICS[q["topic"]]["title"],
                       "correct": correct, "your_answer": q["options"][selected],
                       "correct_answer": q["options"][q["correct"]], "explanation": q["explanation"]})
    weak = [slug for slug, result in summary.items() if result["correct"] < result["total"]]
    return {"form": form, "score": total_correct, "total": len(questions), "percentage": round(total_correct * 100 / len(questions)),
            "topics": summary, "review": review, "focus_topics": weak,
            "next_steps": [summary[slug]["advice"] for slug in weak[:3]] or ["Strong work. Try another set and review any questions you found challenging."]}
