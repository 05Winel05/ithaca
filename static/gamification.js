/* Ithaca Upgrade 7: one idempotent XP event ledger, daily tasks, Athena quests. */
(() => {
  'use strict';
  const KEY = 'ithaca-xp-ledger-v1';
  const DAILY_KEY = 'ithaca-quests';
  const ATHENA_KEY = 'ithaca-athena-current-v1';
  const $ = id => document.getElementById(id);
  const read = (key, fallback) => { try { const v = JSON.parse(localStorage.getItem(key) || 'null'); return v === null ? fallback : v; } catch (_) { return fallback; } };
  const day = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`; };
  const validEvent = (id, e) => typeof id === 'string' && id.length <= 160 && e && Number.isInteger(e.xp) && e.xp >= 0 && e.xp <= 40 && typeof e.day === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(e.day) && typeof e.type === 'string' && e.type.length <= 24 && typeof e.title === 'string' && e.title.length <= 100;
  function load() {
    const raw = read(KEY, {version:1, events:{}});
    const events = {};
    if (raw && raw.events && typeof raw.events === 'object') {
      for (const [id, e] of Object.entries(raw.events).slice(0, 480)) if (validEvent(id, e)) events[id] = e;
    }
    return {version:1, events};
  }
  function save(ledger) {
    localStorage.setItem(KEY, JSON.stringify(ledger));
    if (window.IthacaSync) window.IthacaSync.save();
    window.dispatchEvent(new CustomEvent('ithaca-xp-changed'));
  }
  const total = ledger => Object.values(ledger.events).reduce((sum, e) => sum + e.xp, 0);
  const todayEvents = ledger => Object.entries(ledger.events).filter(([,e]) => e.day === day());
  function reward(ledger, id, xp, type, title, onDay=day()) {
    if (Object.prototype.hasOwnProperty.call(ledger.events, id)) return false;
    if (Object.keys(ledger.events).length >= 480) return false;
    const event = {xp, day:onDay, type, title:String(title).slice(0,100)};
    if (!validEvent(id,event)) return false;
    ledger.events[id] = event;
    save(ledger);
    return true;
  }
  function migrate(ledger) {
    let touched = false;
    // Legacy daily checkboxes were permanent. Credit them once, mark them completed for installation day.
    const prior = read(DAILY_KEY, {});
    if (prior && typeof prior === 'object') {
      for (const box of document.querySelectorAll('[data-quest-id]')) {
        const id = box.dataset.questId;
        if (prior[id] && !ledger.events[`legacy:daily:import:${id}`]) {
          const xp = Math.min(40, Math.max(0, Number(box.dataset.xp) || 0));
          ledger.events[`legacy:daily:import:${id}`] = {xp,day:day(),type:'daily',title:'Previous daily quest: '+id};
          touched = true;
        }
      }
    }
    // Preserve old Athena counters; do NOT count original quest completion a second time.
    const counts = read('ithaca-athena-xp-v1', {});
    if (counts && typeof counts === 'object') {
      for (const [d, val] of Object.entries(counts)) {
        if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) continue;
        const n = Math.min(3,Math.max(0,Math.floor(Number(val)||0)));
        for (let i=0; i<n; i++) {
          const id = `legacy:athena:${d}:${i}`;
          if (!ledger.events[id]) {ledger.events[id]={xp:10,day:d,type:'athena',title:'Previous Athena quest'};touched=true;}
        }
      }
    }
    if (touched) save(ledger);
  }
  function renderLevel(ledger) {
    const xp = total(ledger);
    const level = 1 + Math.floor(xp / 50);
    const progress = xp % 50;
    if ($('level-label')) $('level-label').textContent = `Level ${level}`;
    if ($('xp-count')) $('xp-count').textContent = `${xp} total XP`;
    if ($('level-meter')) $('level-meter').style.width = `${progress * 2}%`;
    if ($('xp-level-detail')) $('xp-level-detail').textContent = `${progress} / 50 XP to next level`;
    if ($('gamification-level')) $('gamification-level').textContent = `Level ${level}`;
    if ($('gamification-xp')) $('gamification-xp').textContent = `${xp} XP earned`;
    const earned = todayEvents(ledger).reduce((n,[,e])=>n+e.xp,0);
    if ($('gamification-today')) $('gamification-today').textContent = `${earned} XP earned today`;
    const days = new Set(Object.values(ledger.events).map(e=>e.day));
    let streak=0; const d = new Date(); d.setHours(12,0,0,0);
    for(let i=0;i<365;i++) {
      const ds=`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
      if (!days.has(ds) && i===0) { d.setDate(d.getDate()-1); continue; }
      if (!days.has(ds)) break;
      streak++;d.setDate(d.getDate()-1);
    }
    if ($('gamification-streak')) $('gamification-streak').textContent=`${streak} day${streak===1?'':'s'} active`;
  }
  function renderDaily(ledger) {
    const boxes=[...document.querySelectorAll('[data-quest-id]')];
    let completed=0;
    boxes.forEach(box=>{
      const id=`daily:${day()}:${box.dataset.questId}`;
      const legacyId=`legacy:daily:import:${box.dataset.questId}`;
      box.checked=Boolean(ledger.events[id] || (ledger.events[legacyId] && ledger.events[legacyId].day===day()));
      box.disabled=box.checked;
      if(box.checked) completed++;
      box.onchange=()=>{
        if (!box.checked) {box.checked=true;return;}
        const xp=Math.min(40,Math.max(0,Number(box.dataset.xp)||0));
        reward(ledger,id,xp,'daily',box.closest('label')?.querySelector('strong')?.textContent||'Daily quest');
        refresh();
      };
    });
    if ($('completion-label')) $('completion-label').textContent=`${completed} of ${boxes.length} daily quests completed today`;
    if ($('daily-reset-note')) $('daily-reset-note').textContent=`Daily quests refresh on the next local calendar day (${day()}).`;
  }
  function planData() {
    const saved=read(ATHENA_KEY,null);
    if(!saved || !saved.plan || !Array.isArray(saved.plan.quests)) return null;
    const p=$('ithaca-profile-data');
    if(p) {
      try {
        const profile=JSON.parse(p.textContent);
        const signature=JSON.stringify([profile.grade,profile.interest,profile.study_hours,profile.universities||[],profile.entry_year]);
        if(saved.signature !== signature) return null;
      } catch (_) {return null;}
    }
    return saved;
  }
  function renderAthena(ledger) {
    const list=$('athena-dash-quests');
    if(!list)return;
    const saved=planData();
    if(!saved){list.hidden=true;return;}
    list.hidden=false;
    if($('athena-dash-title')) $('athena-dash-title').textContent=saved.plan.heading||'Your Athena plan';
    if($('athena-dash-caption')) $('athena-dash-caption').textContent=saved.plan.summary||'';
    if($('athena-dash-foot')) $('athena-dash-foot').textContent='Earn 10 XP per Athena quest, up to 3 per day. Completed tasks remain checked.';
    list.replaceChildren();
    const planId=String(saved.id || saved.savedAt || 'previous-plan').slice(0,80).replace(/[^a-zA-Z0-9_.:-]/g,'_');
    const completed=Array.isArray(saved.completed)?saved.completed:[];
    saved.plan.quests.forEach((quest,i)=>{
      const label=document.createElement('label');label.className='athena-dash-quest';
      const box=document.createElement('input');box.type='checkbox';
      const id=`athena:${planId}:${i}`;
      box.checked=completed.includes(i)||Boolean(ledger.events[id]);box.disabled=box.checked;
      const info=document.createElement('span');info.className='athena-dash-quest-info';
      const heading=document.createElement('strong');heading.textContent=quest.title||`Quest ${i+1}`;
      const detail=document.createElement('small');detail.textContent=`${quest.island||'Study'} · ${quest.minutes||20} min · ${quest.detail||''}`;
      info.append(heading,detail);label.append(box,info);
      box.addEventListener('change',()=>{
        if(!box.checked)return;
        const current=read(ATHENA_KEY,null);
        if(!current || String(current.id||current.savedAt||'previous-plan').slice(0,80).replace(/[^a-zA-Z0-9_.:-]/g,'_')!==planId) return;
        const done=Array.isArray(current.completed)?current.completed:[];
        if(!done.includes(i)) {
          current.completed=[...done,i];
          localStorage.setItem(ATHENA_KEY,JSON.stringify(current));
          const todayCount=todayEvents(ledger).filter(([,e])=>e.type==='athena').length;
          if(todayCount<3) reward(ledger,id,10,'athena',quest.title||'Athena quest');
          if(window.IthacaSync)window.IthacaSync.save();
        }
        refresh();
      });
      list.append(label);
    });
  }
  let ledger;
  function refresh(){ledger=load();renderLevel(ledger);renderDaily(ledger);renderAthena(ledger);}
  function initialize(){
    ledger=load(); migrate(ledger); refresh();
    const history=read('ithaca-assessments-v1',[]);
    if($('recent-practice')&&Array.isArray(history)&&history.length){
      const last=history[history.length-1];
      $('recent-practice').textContent=`Latest practice: ${last.score} of ${last.total} correct · ${history.length} attempt(s) saved`;
    }
    window.addEventListener('storage',e=>{if([KEY,ATHENA_KEY].includes(e.key))refresh();});
  }
  if(window.IthacaSync?.ready)window.IthacaSync.ready.then(initialize,initialize);
  else initialize();
})();
