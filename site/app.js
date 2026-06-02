// Lightbox + gallery navigation
(function () {
  var tiles = Array.prototype.slice.call(document.querySelectorAll('.tile img'));
  var lb = document.getElementById('lightbox');
  var lbImg = document.getElementById('lb-img');
  var lbCap = document.getElementById('lb-caption');
  var idx = -1;

  function show(i) {
    if (i < 0) i = tiles.length - 1;
    if (i >= tiles.length) i = 0;
    idx = i;
    var img = tiles[idx];
    lbImg.src = img.src;
    lbImg.alt = img.alt;
    var cap = img.getAttribute('data-caption') || '';
    lbCap.textContent = cap;
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
  }
  function close() {
    lb.hidden = true;
    document.body.style.overflow = '';
  }

  tiles.forEach(function (img, i) {
    img.addEventListener('click', function () { show(i); });
  });
  lb.querySelector('.lb-close').addEventListener('click', close);
  lb.querySelector('.lb-next').addEventListener('click', function (e) { e.stopPropagation(); show(idx + 1); });
  lb.querySelector('.lb-prev').addEventListener('click', function (e) { e.stopPropagation(); show(idx - 1); });
  lb.addEventListener('click', function (e) { if (e.target === lb) close(); });
  document.addEventListener('keydown', function (e) {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') show(idx + 1);
    else if (e.key === 'ArrowLeft') show(idx - 1);
  });
})();
