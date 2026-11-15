"""Independent, locally graded exam-category practice for Ithaca."""
from flask import Blueprint, jsonify, render_template, request, session
from exam_practice_data import BANK, CATALOG

exam_practice_bp = Blueprint('exam_practice', __name__)

@exam_practice_bp.get('/exam-center')
def index():
    return render_template('exam_center.html', catalog=CATALOG)

@exam_practice_bp.get('/exam-center/<exam>')
def quiz(exam):
    exam = exam.upper()
    if exam not in CATALOG:
        return 'Exam category not found', 404
    return render_template('exam_quiz.html', exam=exam, info=CATALOG[exam])

@exam_practice_bp.post('/api/exam-center/questions')
def questions():
    payload = request.get_json(silent=True) or {}
    if not isinstance(payload, dict):
        return jsonify(error='Invalid request'), 400
    exam = str(payload.get('exam', '')).upper()
    if exam not in BANK:
        return jsonify(error='Choose an exam category'), 400
    focus = payload.get('focus')
    level = payload.get('level', 'mixed')
    if level not in ('mixed', 'foundation', 'intermediate'):
        return jsonify(error='Invalid difficulty'), 400
    all_questions = BANK[exam]
    topics = {q['topic'] for q in all_questions}
    if focus is not None and focus not in topics:
        return jsonify(error='Invalid topic'), 400
    filtered = [q for q in all_questions if (level == 'mixed' or q['difficulty'] == level)]
    # Balance topics by round-robin rather than showing only the first subject.
    # When a focus topic is chosen, allocate up to four of eight questions to it.
    selected = []
    if focus:
        selected.extend(q for q in filtered if q['topic'] == focus)
        selected = selected[:4]
    by_topic = {topic: [q for q in filtered if q['topic'] == topic and q not in selected] for topic in sorted(topics)}
    while len(selected) < 8 and any(by_topic.values()):
        for topic in sorted(by_topic):
            if by_topic[topic] and len(selected) < 8:
                selected.append(by_topic[topic].pop(0))
    return jsonify(exam=exam, questions=[{k:v for k,v in q.items() if k not in ('correct','explanation')} for q in selected], topics=sorted(topics), level=level)

@exam_practice_bp.post('/api/exam-center/grade')
def grade():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify(error='Invalid request'), 400
    exam = str(payload.get('exam', '')).upper()
    if exam not in BANK:
        return jsonify(error='Invalid exam'), 400
    answers = payload.get('answers')
    ids = payload.get('question_ids')
    if not isinstance(answers, dict) or not isinstance(ids, list) or not 1 <= len(ids) <= 8 or len(ids) != len(set(map(str, ids))):
        return jsonify(error='Invalid answers'), 400
    by_id = {q['id']:q for q in BANK[exam]}
    if any(qid not in by_id for qid in ids) or set(answers) != set(ids):
        return jsonify(error='Answer every question'), 400
    review = []
    topic_scores = {}
    score = 0
    for qid in ids:
        q = by_id[qid]
        choice = answers[qid]
        if type(choice) is not int or not 0 <= choice < 4:
            return jsonify(error='Invalid answer option'), 400
        correct = choice == q['correct']
        score += correct
        topic_scores.setdefault(q['topic'], {'correct':0,'total':0})
        topic_scores[q['topic']]['correct'] += int(correct)
        topic_scores[q['topic']]['total'] += 1
        review.append({'text':q['text'], 'correct':correct, 'selected':q['options'][choice], 'answer':q['options'][q['correct']], 'explanation':q['explanation']})
    return jsonify(exam=exam,score=score,total=len(ids), topics=topic_scores,review=review)
