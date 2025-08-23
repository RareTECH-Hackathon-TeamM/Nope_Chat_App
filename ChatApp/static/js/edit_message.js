var elm = document.querySelector('#edit_message');
var manager = new Hammer.Manager(elm);
var hammertime = new Hammer.Press({
  time: 500
});

manager.add(hammertime);

manager.on('press', function(e) {
  alert('press');
});
