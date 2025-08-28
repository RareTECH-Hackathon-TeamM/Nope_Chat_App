'use strict';

document.addEventListener('DOMContentLoaded', () => {
  const open = document.getElementById('go-message-view-btn');
  if (!open) return;

  const hammertime = new Hammer(open);

  hammertime.get('pan').set({
    direction: Hammer.DIRECTION_HORIZONTAL
  });

  hammertime.on('panleft', () => {
    open.classList.add('active');
  });

  hammertime.on('panright', () => {
    open.classList.remove('active');
  });
});
