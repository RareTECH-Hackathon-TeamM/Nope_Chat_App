'use strict';

{
  const open = document.getElementById('modal-open');
  const container = document.getElementById('modal-container');
  const modalBg = document.getElementById('modal-background');
  const search = document.getElementById('search-container');

  open.addEventListener('click', () => {
    container.classList.add('active');
    modalBg.classList.add('active');
    search.classList.add('active');
  });

  modalBg.addEventListener('click', () => {
    container.classList.remove('active');
    modalBg.classList.remove('active');
    search.classList.remove('active');
  });
}
