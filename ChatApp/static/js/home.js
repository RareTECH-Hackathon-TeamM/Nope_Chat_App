'use strict';

{
  const open = document.getElementById('go-message-view-btn');
  const close = document.getElementById('room-delete-btn');

  const manager = new Hammer.Manager(open);
  const hammertime = new Hammer.Press({
    time: 500
  });

  manager.add(hammertime);

  manager.on('press', () => {
    open.classList.add('active');
  });

  manager.on('press', () => {
    open.classList.remove('active');
  });

  open.addEventListener('mouseout', () => {
    open.classList.add('active');
  });

  close.addEventListener('click', () => {
    open.classList.remove('active');
  });
}
