(function () {
  // header shadow + mobile menu
  var hdr = document.querySelector('.hdr');
  var onScroll = function () { if (hdr) hdr.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var burger = document.querySelector('.burger'), nav = document.querySelector('.nav');
  if (burger && nav) burger.addEventListener('click', function () {
    var open = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  // reveal on scroll
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: 0.12 });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // count-up numbers
  document.querySelectorAll('[data-count]').forEach(function (el) {
    var target = parseFloat(el.getAttribute('data-count')), done = false;
    var run = function () {
      if (done) return; done = true; var t0 = null, dur = 1400;
      var step = function (t) { if (!t0) t0 = t; var p = Math.min(1, (t - t0) / dur);
        el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(step); };
      requestAnimationFrame(step);
    };
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es, o) { if (es[0].isIntersecting) { run(); o.disconnect(); } }).observe(el);
    } else { el.textContent = target; }
  });

  // flow video tabs
  document.querySelectorAll('[data-flows]').forEach(function (box) {
    var vid = box.querySelector('video'), cap = box.querySelector('[data-cap]'), title = box.querySelector('[data-title]');
    box.querySelectorAll('.flow-tabs button').forEach(function (b) {
      b.addEventListener('click', function () {
        box.querySelectorAll('.flow-tabs button').forEach(function (x) { x.classList.remove('on'); });
        b.classList.add('on');
        vid.poster = b.dataset.poster; vid.src = b.dataset.src; vid.play && vid.play().catch(function () {});
        if (cap) cap.textContent = b.dataset.cap; if (title) title.textContent = b.dataset.title;
      });
    });
  });

  // live run console
  var con = document.querySelector('[data-console]');
  if (con) {
    var runs = JSON.parse(con.getAttribute('data-console'));
    var list = con.querySelector('.steps-live'), bar = con.querySelector('.bar i'),
        nm = con.querySelector('.name'), role = con.querySelector('.role'), av = con.querySelector('.av'),
        tabs = con.querySelector('.tabs');
    var cur = 0, i = 0, timer = null;
    runs.forEach(function (r, k) {
      var b = document.createElement('button'); b.type = 'button'; b.textContent = r.short;
      b.addEventListener('click', function () { show(k); }); tabs.appendChild(b);
    });
    function show(k) {
      cur = k; i = 0; var r = runs[k];
      nm.textContent = r.name; role.textContent = r.role; av.textContent = r.av;
      [].forEach.call(tabs.children, function (b, j) { b.classList.toggle('on', j === k); });
      list.innerHTML = r.steps.map(function (s) {
        return '<li><span class="dot"></span><div><div class="t">' + s[0] + '</div><div class="d">' + s[1] + '</div>' +
          (s[2] ? '<span class="gate">' + s[2] + '</span>' : '') + '</div></li>';
      }).join('');
      tick(); clearInterval(timer); timer = setInterval(tick, 1900);
    }
    function tick() {
      var r = runs[cur], lis = list.children;
      for (var j = 0; j < lis.length; j++) { lis[j].className = j < i ? 'done' : (j === i ? 'now' : ''); }
      bar.style.width = Math.min(100, (i / r.steps.length) * 100) + '%';
      i++;
      if (i > r.steps.length + 1) { show((cur + 1) % runs.length); }
    }
    show(0);
  }

  // contact form -> opens the visitor's email app (no data is sent to any server)
  var f = document.querySelector('[data-mailto]');
  if (f) f.addEventListener('submit', function (e) {
    e.preventDefault();
    var v = function (n) { return (f.elements[n] && f.elements[n].value || '').trim(); };
    var body = 'Name: ' + v('name') + '\nCompany: ' + v('company') + '\nInterested in: ' + v('topic') + '\n\n' + v('message');
    location.href = 'mailto:' + f.getAttribute('data-mailto') + '?subject=' + encodeURIComponent('Digital workers: ' + v('topic')) +
      '&body=' + encodeURIComponent(body);
  });
})();
