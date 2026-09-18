#!/usr/bin/env node

/**
 * Local HTML Editor
 * 
 * Usage: node edit-html.js <path-to-html-file>
 * 
 * Opens your HTML file in the browser with editable text regions.
 * Click any text to edit it, then click "Save" to write changes back to the file.
 * 
 * By default, all <p>, <h1>-<h6>, <li>, <td>, <th>, <span>, and <div> elements
 * become editable. You can customize this by modifying EDITABLE_SELECTORS.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

// Configuration
const PORT = 3456;
const EDITABLE_SELECTORS = 'p, h1, h2, h3, h4, h5, h6, li, td, th, span:not(.edit-toolbar *), div:not(.edit-toolbar):not([contenteditable="false"])';

// Get the HTML file from command line args
const htmlFile = process.argv[2];

if (!htmlFile) {
  console.error('Usage: node edit-html.js <path-to-html-file>');
  console.error('Example: node edit-html.js index.html');
  process.exit(1);
}

const htmlFilePath = path.resolve(htmlFile);

if (!fs.existsSync(htmlFilePath)) {
  console.error(`File not found: ${htmlFilePath}`);
  process.exit(1);
}

// The editor script that gets injected into the HTML
const editorScript = `
<style>
  .edit-toolbar {
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 999999;
    background: #333;
    padding: 10px 15px;
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    display: flex;
    gap: 10px;
    align-items: center;
  }
  .edit-toolbar button {
    background: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
  }
  .edit-toolbar button:hover {
    background: #45a049;
  }
  .edit-toolbar button.secondary {
    background: #666;
  }
  .edit-toolbar button.secondary:hover {
    background: #555;
  }
  .edit-toolbar .status {
    color: #fff;
    font-size: 13px;
    margin-left: 10px;
  }
  .edit-toast {
    position: fixed;
    bottom: 30px;
    left: 50%;
    transform: translateX(-50%);
    background: #333;
    color: #fff;
    padding: 12px 24px;
    border-radius: 8px;
    font-size: 14px;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    z-index: 9999999;
    opacity: 0;
    transition: opacity 0.3s;
    pointer-events: none;
  }
  .edit-toast.error {
    background: #d32f2f;
  }
  .edit-toast.visible {
    opacity: 1;
  }
  [contenteditable="true"] {
    outline: 2px dashed transparent;
    transition: outline-color 0.2s;
  }
  [contenteditable="true"]:hover {
    outline-color: #4CAF5066;
  }
  [contenteditable="true"]:focus {
    outline-color: #4CAF50;
    outline-style: solid;
  }
</style>

<div class="edit-toast" id="editToast"></div>
<div class="edit-toolbar">
  <button onclick="saveChanges()">💾 Save</button>
  <button class="secondary" onclick="location.reload()">↻ Reload</button>
  <span class="status" id="editStatus">Click any text to edit</span>
</div>

<script>
  function showToast(msg, isError) {
    const toast = document.getElementById('editToast');
    toast.textContent = msg;
    toast.className = 'edit-toast visible' + (isError ? ' error' : '');
    setTimeout(() => { toast.className = 'edit-toast'; }, 2000);
  }

  // Show toast on reload after save
  const params = new URLSearchParams(location.search);
  if (params.has('saved')) { showToast('Saved successfully'); history.replaceState(null, '', '/'); }
  if (params.has('error')) { showToast('Error: ' + params.get('error'), true); history.replaceState(null, '', '/'); }

  // Make elements editable
  document.querySelectorAll('${EDITABLE_SELECTORS}').forEach(el => {
    // Skip if inside toolbar or already has contenteditable set to false
    if (el.closest('.edit-toolbar') || el.getAttribute('contenteditable') === 'false') return;

    // Skip elements that only contain other editable elements (to avoid nested editing)
    const hasOnlyElementChildren = el.children.length > 0 &&
      Array.from(el.childNodes).every(n => n.nodeType !== 3 || !n.textContent.trim());
    if (hasOnlyElementChildren && el.tagName !== 'LI') return;

    el.setAttribute('contenteditable', 'true');
  });

  // Escape to exit edit mode (blur the active element)
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && document.activeElement.getAttribute('contenteditable') === 'true') {
      document.activeElement.blur();
    }
  });

  // Track changes
  let hasChanges = false;
  document.addEventListener('input', (e) => {
    if (e.target.getAttribute('contenteditable') === 'true') {
      hasChanges = true;
      document.getElementById('editStatus').textContent = 'Unsaved changes';
    }
  });

  // Save function
  async function saveChanges() {
    // Clone the document and strip editor UI from the clone (leave live DOM intact)
    const clone = document.documentElement.cloneNode(true);
    clone.querySelectorAll('.edit-toolbar, .edit-toast').forEach(el => el.remove());
    clone.querySelectorAll('[contenteditable]').forEach(el => el.removeAttribute('contenteditable'));
    clone.querySelectorAll('style, script').forEach(el => {
      if (el.textContent.includes('edit-toolbar') || el.textContent.includes('saveChanges')) el.remove();
    });
    const html = '<!DOCTYPE html>\\n' + clone.outerHTML;
    
    try {
      const response = await fetch('/save', {
        method: 'POST',
        headers: { 'Content-Type': 'text/html' },
        body: html
      });
      
      if (response.ok) {
        hasChanges = false;
        location.href = '/?saved=1' + location.hash;
      } else {
        throw new Error('Save failed');
      }
    } catch (err) {
      location.href = '/?error=' + encodeURIComponent(err.message) + location.hash;
    }
  }

  // Warn before leaving with unsaved changes
  window.addEventListener('beforeunload', (e) => {
    if (hasChanges) {
      e.preventDefault();
      e.returnValue = '';
    }
  });
</script>
`;

// Create the server
const server = http.createServer((req, res) => {
  // Handle save request
  if (req.method === 'POST' && req.url === '/save') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        fs.writeFileSync(htmlFilePath, body, 'utf8');
        console.log(`✓ Saved changes to ${htmlFilePath}`);
        res.writeHead(200);
        res.end('OK');
      } catch (err) {
        console.error('Error saving:', err);
        res.writeHead(500);
        res.end('Error saving file');
      }
    });
    return;
  }

  // Serve the HTML file with editor injected
  const reqPath = req.url.split('?')[0];
  if (req.method === 'GET' && (reqPath === '/' || reqPath === '/index.html')) {
    try {
      let html = fs.readFileSync(htmlFilePath, 'utf8');
      
      // Inject the editor before </body> or at the end
      if (html.includes('</body>')) {
        html = html.replace('</body>', editorScript + '</body>');
      } else {
        html += editorScript;
      }
      
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(html);
    } catch (err) {
      res.writeHead(500);
      res.end('Error reading file');
    }
    return;
  }

  // Serve other static files (css, js, images) from the same directory
  const baseDir = path.dirname(htmlFilePath);
  const filePath = path.join(baseDir, req.url);
  if (!filePath.startsWith(baseDir)) { res.writeHead(403); res.end('Forbidden'); return; }
  if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
    const ext = path.extname(filePath).toLowerCase();
    const mimeTypes = {
      '.css': 'text/css',
      '.js': 'application/javascript',
      '.json': 'application/json',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.jpeg': 'image/jpeg',
      '.gif': 'image/gif',
      '.svg': 'image/svg+xml',
      '.ico': 'image/x-icon',
      '.woff': 'font/woff',
      '.woff2': 'font/woff2',
    };
    res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
    res.end(fs.readFileSync(filePath));
    return;
  }

  res.writeHead(404);
  res.end('Not found');
});

server.listen(PORT, () => {
  const url = `http://localhost:${PORT}`;
  console.log(`\n🖊️  HTML Editor running at ${url}`);
  console.log(`   Editing: ${htmlFilePath}\n`);
  console.log('   Click any text to edit, press Escape to deselect, then click Save.\n');
  console.log('   Press Ctrl+C to stop the server.\n');

  // Try to open browser
  const openCmd = process.platform === 'darwin' ? 'open' :
                  process.platform === 'win32' ? 'start' : 'xdg-open';
  exec(`${openCmd} ${url}`);
});