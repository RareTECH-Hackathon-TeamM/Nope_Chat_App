'use strict';

//各ルームに対してスワイプの処理を付与
document.addEventListener('DOMContentLoaded', () => {
  const buttons = document.getElementsByClassName('go-message-view-btn');
  if (!buttons.length) return;

  Array.from(buttons).forEach(button => {

    const hammertime = new Hammer(button);

    hammertime.get('pan').set({
      direction: Hammer.DIRECTION_HORIZONTAL
    });

    hammertime.on('panleft', () => {
      button.classList.add('active');
    });

    hammertime.on('panright', () => {
      button.classList.remove('active');
    });
  });
});
