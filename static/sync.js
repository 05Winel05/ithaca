/* Keeps local progress available and backs it up to the selected database. */
(() => {
  'use strict';
  const commonKeys = [
    'ithaca-quests', 'ithaca-assessments-v1', 'ithaca-exam-practice-v1',
    'ithaca-athena-current-v1', 'ithaca-athena-xp-v1'
  ];
  let connected = false;
  let timer = null;
  let writing = Promise.resolve();

  function parse(value, fallback) {
    try { return JSON.parse(value); } catch (_) { return fallback; }
  }

  function collect() {
    const data = {};
    for (const key of commonKeys) {
      const value = localStorage.getItem(key);
      if (value !== null) data[key] = parse(value, null);
    }
    for (let i = 0; i < localStorage.length; i++) {
      const key = localStorage.key(i);
      if (key && key.startsWith('ithaca-preparation:')) {
        data[key] = parse(localStorage.getItem(key), {});
      }
    }
    return data;
  }

  function merge(local, remote) {
    const all = {...remote, ...local};
    for (const key of Object.keys(all)) {
      const a = local[key], b = remote[key];
      if (a === undefined) { all[key] = b; continue; }
      if (b === undefined) { all[key] = a; continue; }
      if (key === 'ithaca-quests') {
        const result = {};
        for (const id of new Set([...Object.keys(b || {}), ...Object.keys(a || {})])) {
          result[id] = Boolean(a?.[id] || b?.[id]);
        }
        all[key] = result;
      } else if (key === 'ithaca-assessments-v1') {
        const map = new Map();
        for (const entry of [...(Array.isArray(b) ? b : []), ...(Array.isArray(a) ? a : [])]) {
          if (!entry || typeof entry.date !== 'string') continue;
          const id = [entry.date, entry.form, entry.score, entry.total].join('|');
          map.set(id, entry);
        }
        all[key] = [...map.values()].sort((x, y) => x.date.localeCompare(y.date)).slice(-30);
      } else if (key === 'ithaca-exam-practice-v1') {
        // Merge existing browser results with MongoDB results, retaining original timestamps.
        const entries = [...(Array.isArray(b) ? b : []), ...(Array.isArray(a) ? a : [])];
        const unique = new Map();
        for (const attempt of entries) {
          if (!attempt || typeof attempt.date !== 'string' || typeof attempt.exam !== 'string') continue;
          if (!['SAT','ACT','TOEFL','IELTS','DET'].includes(attempt.exam)) continue;
          const identity = [attempt.date, attempt.exam, attempt.score, attempt.total].join('|');
          unique.set(identity, attempt);
        }
        all[key] = [...unique.values()].sort((x,y) => x.date.localeCompare(y.date)).slice(-40);
      } else if (key === 'ithaca-athena-xp-v1') {
        const ledger = {};
        for (const day of new Set([...Object.keys(a || {}), ...Object.keys(b || {})])) {
          ledger[day] = Math.min(3, Math.max(Number(a?.[day]) || 0, Number(b?.[day]) || 0));
        }
        all[key] = ledger;
      } else if (key === 'ithaca-athena-current-v1') {
        const latest = (Date.parse(a?.savedAt) || 0) >= (Date.parse(b?.savedAt) || 0) ? a : b;
        const previous = latest === a ? b : a;
        all[key] = latest;
        if (latest?.id && latest.id === previous?.id) {
          all[key] = {...latest, completed: [...new Set([...(latest.completed || []), ...(previous.completed || [])])]};
        }
      } else if (key.startsWith('ithaca-preparation:')) {
        all[key] = {...(b || {}), ...(a || {})};
      }
    }
    return all;
  }

  function indicator(text) {
    const element = document.getElementById('storage-status');
    if (element) element.textContent = text;
  }

  async function upload() {
    const response = await fetch('/api/sync', {
      method: 'POST', credentials: 'same-origin',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({state: collect()})
    });
    if (!response.ok) throw new Error('Cloud save failed');
    connected = true;
    indicator('Saved in browser and MongoDB Atlas');
    return true;
  }

  function save() {
    if (!connected) return;
    clearTimeout(timer);
    timer = setTimeout(() => {
      writing = writing.catch(() => {}).then(upload).catch(() => {
        connected = false;
        indicator('Saved in this browser · Cloud temporarily unavailable');
      });
    }, 250);
  }

  async function initialize() {
    indicator('Saved in this browser');
    try {
      const response = await fetch('/api/sync', {credentials: 'same-origin'});
      if (!response.ok) return false;
      const data = await response.json();
      if (!data.connected) return false;
      const combined = merge(collect(), data.state || {});
      for (const [key, value] of Object.entries(combined)) {
        if (value !== undefined && value !== null) localStorage.setItem(key, JSON.stringify(value));
      }
      connected = true;
      try { await upload(); } catch (_) {
        connected = false;
        indicator('Saved in this browser · Cloud temporarily unavailable');
      }
      return connected;
    } catch (_) { return false; }
  }

  window.IthacaSync = {ready: initialize(), save, isConnected: () => connected};
})();
