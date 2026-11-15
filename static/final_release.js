/* Ithaca Final Local Release: daily roadmap & visible XP rewards. No extra AI calls. */
(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const read = (key, fallback) => {
    try { const x = JSON.parse(localStorage.getItem(key) || 'null'); return x === null ? fallback : x; }
    catch (_) { return fallback; }
  };
  const localDay = () => {
    const x = new Date();
    return `${x.getFullYear()}-${String(x.getMonth()+1).padStart(2,'0')}-${String(x.getDate()).padStart(2,'0')}`;
  };
  const examNames = {SAT:'SAT',ACT:'ACT',TOEFL:'TOEFL',IELTS:'IELTS Academic',DET:'Duolingo English Test'};
  function worstArea() {
    const attempts = read('ithaca-exam-practice-v1', []);
    if (!Array.isArray(attempts)) return null;
    const scores = {};
    for (const a of attempts.slice(-15)) {
      if (!a || !examNames[a.exam] || !a.topics || typeof a.topics !== 'object') continue;
      for (const [name,s] of Object.entries(a.topics)) {
        if (!s || !Number.isInteger(s.correct) || !Number.isInteger(s.total) || s.total < 1) continue;
        const key = JSON.stringify([a.exam,name]);
        if (!scores[key]) scores[key] = {exam:a.exam,topic:name, correct:0,total:0};
        scores[key].correct += s.correct; scores[key].total += s.total;
      }
    }
    return Object.values(scores).sort((a,b) => a.correct/a.total-b.correct/b.total || b.total-a.total)[0] || null;
  }
  function planQuest() {
    const p = read('ithaca-athena-current-v1', null);
    if (!p || !p.plan || !Array.isArray(p.plan.quests)) return null;
    const done = Array.isArray(p.completed) ? p.completed : [];
    return p.plan.quests.find((q,i) => !done.includes(i) && q && typeof q.title === 'string') || null;
  }
  function routeForToday() {
    const key = 'ithaca-final-daily-route-v1';
    const stored = read(key,null);
    if (stored && stored.day === localDay() && Array.isArray(stored.items) && stored.items.length === 3) return stored.items;
    const weak = worstArea(); const quest = planQuest();
    const items = [
      {title:'Plan today’s learning route', detail: weak ? `Schedule 15 minutes to improve ${weak.exam} — ${weak.topic}.` : 'Choose one subject and set a realistic study time.', href: weak ? `/exam-center/${encodeURIComponent(weak.exam)}?focus=${encodeURIComponent(weak.topic)}` : '/exam-center', link:'Open exam practice'},
      {title:'Complete focused practice', detail: weak ? `Practice ${weak.topic} in ${examNames[weak.exam]}; review each explanation.` : 'Complete a short General Skills or exam practice set.', href: weak ? `/exam-center/${encodeURIComponent(weak.exam)}?focus=${encodeURIComponent(weak.topic)}` : '/assessment', link:'Practice now'},
      {title:'Reflect and continue the journey', detail: quest ? `Work on Athena: ${quest.title}. Write down what you learned.` : 'Write down one mistake and one improvement; ask Athena for the next plan when ready.', href:'/athena', link:'Open Athena'}
    ];
    try { localStorage.setItem(key,JSON.stringify({day:localDay(),items})); } catch (_) { /* browser storage disabled */ }
    return items;
  }
  function build() {
    if (!$('final-route-panel')) return;
    const items=routeForToday();
    const list=$('final-route-list'); if (!list) return;
    list.replaceChildren();
    const labels=[...document.querySelectorAll('[data-quest-id]')];
    for (let i=0;i<items.length;i++) {
      const it=items[i];
      const card=document.createElement('div'); card.className='final-route-item';
      const header=document.createElement('strong');header.textContent=`${i+1}. ${it.title}`;
      const small=document.createElement('span');small.textContent=it.detail;
      const link=document.createElement('a');link.href=it.href;link.textContent=`${it.link} ↗`;
      card.append(header,small,link);list.append(card);
      if(labels[i]) {
        const strong=labels[i].closest('label')?.querySelector('.quest-info strong');
        const detail=labels[i].closest('label')?.querySelector('.quest-info small');
        if (strong) strong.textContent=it.title;
        if (detail) detail.textContent=it.detail;
      }
    }
    const area=worstArea();
    if ($('final-focus-note')) $('final-focus-note').textContent=area ? `Based on recent short practice: ${area.exam} — ${area.topic} (${area.correct}/${area.total} correct). This is not an official exam score.` : 'Complete an exam practice set to receive a personalized recommendation.';
    updateRewards();
    window.addEventListener('ithaca-xp-changed',updateRewards);
    window.addEventListener('storage',updateRewards);
    const athena=$('athena-dash-quests');
    if (athena) new MutationObserver(updateRewards).observe(athena,{childList:true});
  }
  function updateRewards() {
    const ledger=read('ithaca-xp-ledger-v1',{events:{}});
    const events=ledger && ledger.events && typeof ledger.events==='object' ? Object.values(ledger.events) : [];
    const today=events.filter(e=>e && e.day===localDay());
    const used=today.filter(e=>e.type==='athena').length;
    if ($('final-xp-rule')) $('final-xp-rule').textContent=`Athena XP today: ${Math.min(used,3)*10}/30. Each new quest completion rewards 10 XP until the daily cap. Completed quests never reward twice.`;
    if ($('final-day-summary')) $('final-day-summary').textContent=`${today.reduce((n,e)=>n+(Number(e.xp)||0),0)} XP earned today. XP is not awarded again by refreshing.`;
  }
  if (window.IthacaSync?.ready) window.IthacaSync.ready.then(build,build); else build();
})();
