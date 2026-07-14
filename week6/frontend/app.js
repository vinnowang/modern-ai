async function fetchJSON(url, options) {
  const res = await fetch(url, options);
  if (!res.ok) throw new Error(await res.text());
  if (res.status === 204) return null;
  return res.json();
}

let localNotes = [];

async function loadNotes() {
  try {
    localNotes = await fetchJSON('/notes/');
    renderNotes();
  } catch (err) {
    console.error("Failed to load notes", err);
  }
}

function renderNotes() {
  const list = document.getElementById('notes');
  list.innerHTML = '';
  
  for (const n of localNotes) {
    const li = document.createElement('li');
    li.style.display = 'flex';
    li.style.justifyContent = 'space-between';
    li.style.alignItems = 'center';
    li.style.marginBottom = '8px';
    
    const span = document.createElement('span');
    span.textContent = `${n.title}: ${n.content}`;
    
    const delBtn = document.createElement('button');
    delBtn.textContent = 'Delete';
    delBtn.style.marginLeft = '10px';
    delBtn.onclick = () => deleteNoteOptimistic(n.id);
    
    li.appendChild(span);
    li.appendChild(delBtn);
    list.appendChild(li);
  }
}

async function deleteNoteOptimistic(noteId) {
  const backupNotes = [...localNotes];
  localNotes = localNotes.filter(n => n.id !== noteId);
  renderNotes();
  
  try {
    await fetchJSON(`/notes/${noteId}`, { method: 'DELETE' });
  } catch (err) {
    alert('Failed to delete note. Rolling back change.');
    localNotes = backupNotes;
    renderNotes();
  }
}

async function loadActions() {
  const list = document.getElementById('actions');
  list.innerHTML = '';
  
  // Read current filter state
  const filterVal = document.getElementById('action-filter').value;
  let url = '/action-items/';
  if (filterVal === 'open') url += '?completed=false';
  if (filterVal === 'completed') url += '?completed=true';
  
  const items = await fetchJSON(url);
  for (const a of items) {
    const li = document.createElement('li');
    li.style.display = 'flex';
    li.style.alignItems = 'center';
    li.style.gap = '8px';
    li.style.marginBottom = '6px';
    
    // Checkbox for bulk select
    if (!a.completed) {
      const chk = document.createElement('input');
      chk.type = 'checkbox';
      chk.className = 'action-checkbox';
      chk.value = a.id;
      li.appendChild(chk);
    }
    
    const text = document.createElement('span');
    text.textContent = `${a.description} [${a.completed ? 'done' : 'open'}]`;
    li.appendChild(text);
    
    if (!a.completed) {
      const btn = document.createElement('button');
      btn.textContent = 'Complete';
      btn.style.marginLeft = 'auto';
      btn.onclick = async () => {
        await fetchJSON(`/action-items/${a.id}/complete`, { method: 'PUT' });
        loadActions();
      };
      li.appendChild(btn);
    }
    list.appendChild(li);
  }
}

async function bulkCompleteActions() {
  const checkboxes = document.querySelectorAll('.action-checkbox:checked');
  const ids = Array.from(checkboxes).map(cb => parseInt(cb.value));
  
  if (ids.length === 0) {
    alert('Please select at least one action item.');
    return;
  }
  
  try {
    await fetchJSON('/action-items/bulk-complete', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ ids })
    });
    loadActions();
  } catch (err) {
    alert('Failed to execute bulk completion.');
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('note-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const title = document.getElementById('note-title').value;
    const content = document.getElementById('note-content').value;
    await fetchJSON('/notes/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content }),
    });
    e.target.reset();
    loadNotes();
  });

  document.getElementById('action-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const description = document.getElementById('action-desc').value;
    await fetchJSON('/action-items/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ description }),
    });
    e.target.reset();
    loadActions();
  });

  loadNotes();
  loadActions();
});
