const resizer = document.querySelector('.resizer');
const leftPanel = document.querySelector('.course-content');
const rightPanel = document.querySelector('.code-editor');
const container = document.querySelector('.course-editor');

let isResizing = false;

resizer.addEventListener('mousedown', (e) => {
  isResizing = true;
  document.addEventListener('mousemove', resize);
  document.addEventListener('mouseup', stopResize);
});

function resize(e) {
  if (!isResizing) return;

  const containerOffsetLeft = container.getBoundingClientRect().left;
  const containerWidth = container.getBoundingClientRect().width;
  let newLeftWidth = ((e.clientX - containerOffsetLeft) / containerWidth) * 100;

  if (newLeftWidth < 10) newLeftWidth = 10;
  if (newLeftWidth > 90) newLeftWidth = 90;

  leftPanel.style.width = `${newLeftWidth}%`;
  rightPanel.style.width = `${100 - newLeftWidth}%`;
}

function stopResize() {
  isResizing = false;
  document.removeEventListener('mousemove', resize);
  document.removeEventListener('mouseup', stopResize);
}
