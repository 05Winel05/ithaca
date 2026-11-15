/* Ithaca Upgrade 6: unified, local-first exam history display. */
(() => {
  'use strict';
  const key = 'ithaca-exam-practice-v1';
  const known = new Set(['SAT','ACT','TOEFL','IELTS','DET']);
  const examNames = {SAT:'SAT',ACT:'ACT',TOEFL:'TOEFL',IELTS:'IELTS',DET:'Duolingo English Test'};
  const el = id => document.getElementById(id);
  const make = (tag, text, cls) => {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  };
  function loadHistory() {
    try {
      const values = JSON.parse(localStorage.getItem(key) || '[]');
      return Array.isArray(values) ? values.filter(x => x && known.has(x.exam) &&
        Number.isInteger(x.score) && Number.isInteger(x.total) && x.total > 0 &&
        x.total <= 8 && x.score >= 0 && x.score <= x.total && typeof x.date === 'string') : [];
    } catch (_) { return []; }
  }
  function render() {
    const examHistory = loadHistory();
    const generalRaw = (() => { try { return JSON.parse(localStorage.getItem('ithaca-assessments-v1') || '[]'); } catch (_) { return []; }})();
    const general = Array.isArray(generalRaw) ? generalRaw.filter(x => x && typeof x.date === 'string' && Number.isInteger(x.score) && Number.isInteger(x.total) && x.total > 0) : [];
    const combined = [
      ...general.map(x => ({...x, label:'General Skills · Set ' + (x.form || '?')})),
      ...examHistory.map(x => ({...x, label:examNames[x.exam] + ' practice'}))
    ].sort((a, b) => Date.parse(b.date) - Date.parse(a.date));
    if (el('unified-attempt-count')) el('unified-attempt-count').textContent = String(combined.length);
    if (el('unified-category-count')) el('unified-category-count').textContent = String(new Set(combined.map(x => x.exam || 'GENERAL')).size);
    if (el('unified-latest-score')) el('unified-latest-score').textContent = combined.length ? `${combined[0].score}/${combined[0].total}` : '—';
    const history = el('unified-exam-history');
    if (!history) return;
    history.replaceChildren();
    if (!combined.length) {
      history.append(make('p','No practice attempts yet. Complete a general skill check or choose an exam to begin.','hint'));
    } else {
      for (const item of combined.slice(0, 15)) {
        const date = new Date(item.date);
        const dateText = Number.isNaN(date.valueOf()) ? 'Previous attempt' : date.toLocaleDateString();
        const row = make('div',undefined,'unified-attempt');
        const details = make('div',undefined,'unified-attempt-detail');
        details.append(make('strong',item.label),make('span',`${dateText} · ${item.score} of ${item.total} correct`));
        const ratio = Math.round(item.score/item.total*100);
        const meter = make('div',undefined,'unified-meter');
        const bar = make('div',undefined,'unified-fill');
        bar.style.width = ratio + '%';
        meter.append(bar);
        row.append(details,meter,make('strong',ratio + '%','unified-percent'));
        history.append(row);
      }
    }
    const breakdown = el('unified-topic-breakdown');
    if (!breakdown) return;
    breakdown.replaceChildren();
    const summary = {};
    for (const entry of examHistory.slice(-20)) {
      for (const [topic, result] of Object.entries(entry.topics || {})) {
        if (!result || !Number.isInteger(result.correct) || !Number.isInteger(result.total) || result.total < 1) continue;
        const id = `${entry.exam} — ${topic}`;
        if (!summary[id]) summary[id] = {correct:0,total:0};
        summary[id].correct += result.correct;
        summary[id].total += result.total;
      }
    }
    const ranked = Object.entries(summary).filter(([,s]) => s.total).sort((a,b)=> a[1].correct/a[1].total - b[1].correct/b[1].total);
    if (!ranked.length) breakdown.append(make('p','Complete an exam-category practice set to see focused study suggestions.','hint'));
    else for (const [topic,s] of ranked.slice(0,8)) {
      const row = make('div',undefined,'unified-topic');
      row.append(make('strong',topic),make('span',`${s.correct}/${s.total} correct`));
      const track = make('div',undefined,'unified-meter');
      const fill = make('div',undefined,'unified-fill');
      fill.style.width = Math.round(s.correct/s.total*100) + '%';
      track.append(fill);
      row.append(track);
      breakdown.append(row);
    }
    const focus = el('unified-focus-link');
    if (focus && ranked.length) {
      const worst = ranked[0][0].split(' — ');
      focus.textContent = `Practice ${worst[0]} again ↗`;
      focus.href = '/exam-center/' + encodeURIComponent(worst[0]);
    }
  }
  if (window.IthacaSync && window.IthacaSync.ready) {
    window.IthacaSync.ready.then(render, render);
  } else {
    render();
  }
})();
