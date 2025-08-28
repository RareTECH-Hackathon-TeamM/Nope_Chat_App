'use strict';

{
  // モーダルの制御
  const modal = document.getElementById('hamburger-modal');
  const btn = document.getElementById('hamburger-btn');
  const closeBtn = document.querySelector('.modal-close');

  btn.addEventListener('click', () => {
    modal.style.display = 'flex';
  });

  closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
  });

  window.addEventListener('click', (e) => {
    if (e.target === modal) {
      modal.style.display = 'none';
    }
  });

  // 既存のHammer.jsコード
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

  manager.on('pressup', () => {
    open.classList.remove('active');
  });

  open.addEventListener('mouseout', () => {
    open.classList.remove('active');
  });

  close.addEventListener('click', () => {
    open.classList.remove('active');
  });
}