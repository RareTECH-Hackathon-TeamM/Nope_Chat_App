document.getElementById('copyButton').addEventListener('click', function() {
  const linkToCopy = document.getElementById('myLink').href; // コピーしたいリンクのURLを取得

  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(linkToCopy)
      .then(() => {
        alert('リンクがクリップボードにコピーされました！'); // コピー成功時のメッセージ
      })
      .catch(err => {
        console.error('コピーに失敗しました: ', err);
        alert('リンクのコピーに失敗しました。'); // コピー失敗時のメッセージ
      });
  } else {
    // 古いブラウザでの代替処理（オプション）
    alert('クリップボード機能が利用できません。');
  }
});
