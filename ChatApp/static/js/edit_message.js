'use strict';

{
  const open = document.getElementById('modal-open');
  const container = document.getElementById('modal-container');
  const close = document.getElementById('modal-close');
  const conversationCompose = document.getElementById('conversation-compose');

  const manager = new Hammer.Manager(open);
  const hammertime = new Hammer.Press({
    time: 500
  });

  manager.add(hammertime);

  manager.on('press', () => {
    container.classList.add('active');
    conversationCompose.classList.add('deactive');
  });

  close.addEventListener('click', () => {
    container.classList.remove('active');
    conversationCompose.classList.remove('deactive');
  });
}

function openKeybord() {
  document.getElementById('message-input').focus();

}
