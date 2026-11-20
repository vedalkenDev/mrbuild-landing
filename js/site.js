/* Mr Build site script. Shared by every page. Pages work without it; this only adds polish. */
(function(){
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var root = document.documentElement;
  if(!reduce) root.classList.add('motion');
  function $$(sel, ctx){ return [].slice.call((ctx || document).querySelectorAll(sel)); }

  // Sticky nav shadow
  var nav = document.querySelector('.nav');
  if(nav){
    var onScroll = function(){ nav.classList.toggle('scrolled', window.scrollY > 8); };
    window.addEventListener('scroll', onScroll, {passive:true}); onScroll();
  }

  // Mobile drawer
  var btn = document.getElementById('menu-btn'), drawer = document.getElementById('drawer');
  if(btn && drawer){
    var setMenu = function(open){ btn.setAttribute('aria-expanded', open); drawer.classList.toggle('open', open); };
    btn.addEventListener('click', function(){ setMenu(btn.getAttribute('aria-expanded') !== 'true'); });
    drawer.addEventListener('click', function(e){ if(e.target.closest('a')) setMenu(false); });
    document.addEventListener('keydown', function(e){ if(e.key === 'Escape') setMenu(false); });
    document.addEventListener('click', function(e){
      if(btn.getAttribute('aria-expanded') !== 'true') return;
      if(drawer.contains(e.target) || btn.contains(e.target)) return;
      setMenu(false);
    });
  }

  // Count-up for [data-count]. Decorative, rare, so it can take about 1s.
  function countUp(el){
    var end = +el.getAttribute('data-count');
    if(reduce || !end) return;
    var start = performance.now(), dur = 1100;
    el.textContent = '1';
    function tick(t){
      var p = Math.min(1, (t - start) / dur);
      var e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.max(1, Math.round(e * end));
      if(p < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  // Branch open/closed status, in South African time.
  // Mon–Fri 07:30–13:30 and 14:00–16:30, Sat 07:30–12:30, Sun closed.
  function branchStatus(){
    var els = $$('[data-status]');
    if(!els.length) return;
    var parts;
    try {
      parts = new Intl.DateTimeFormat('en-ZA', {timeZone:'Africa/Johannesburg', weekday:'short', hour:'2-digit', minute:'2-digit', hourCycle:'h23'}).formatToParts(new Date());
    } catch(e){ return; }
    var get = function(t){ for(var i=0;i<parts.length;i++) if(parts[i].type===t) return parts[i].value; };
    var day = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'].indexOf(get('weekday').slice(0,3));
    var m = (+get('hour')) * 60 + (+get('minute'));
    var weekday = [[450,810],[840,990]], sat = [[450,750]];
    var slots = day === 0 ? [] : day === 6 ? sat : weekday;
    var txt, open = false;
    for(var i=0;i<slots.length;i++){ if(m >= slots[i][0] && m < slots[i][1]){ open = true; break; } }
    if(open){
      var closeAt = slots[i][1];
      txt = (closeAt - m <= 30) ? 'Closing soon' : 'Open now';
    } else if(day >= 1 && day <= 5 && m >= 810 && m < 840){
      txt = 'Lunch, back at 14:00';
    } else if(day >= 1 && day <= 5 && m < 450){
      txt = 'Opens 07:30';
    } else if(day === 6 && m < 450){
      txt = 'Opens 07:30';
    } else if(day === 5 || day === 6){
      txt = 'Closed, opens Mon';
    } else {
      txt = 'Closed, opens 07:30';
    }
    els.forEach(function(el){
      el.textContent = txt;
      el.classList.toggle('open', open);
      el.classList.toggle('shut', !open);
      el.hidden = false;
    });
  }
  branchStatus();

  // Branch filter. Exit is faster than entry (140ms out, 200ms in).
  var chips = $$('.chip[data-filter]');
  if(chips.length){
    var cards = $$('.bcard[data-district]');
    var busy = null;
    chips.forEach(function(chip){
      chip.addEventListener('click', function(){
        var f = chip.getAttribute('data-filter');
        chips.forEach(function(c){ c.setAttribute('aria-pressed', c === chip); });
        clearTimeout(busy);
        var show = function(c){ return f === 'all' || c.getAttribute('data-district') === f; };
        if(reduce){ cards.forEach(function(c){ c.hidden = !show(c); }); return; }
        cards.forEach(function(c){ if(!c.hidden && !show(c)) c.classList.add('is-out'); });
        busy = setTimeout(function(){
          cards.forEach(function(c){
            if(show(c)){
              if(c.hidden){ c.hidden = false; c.classList.add('is-out'); c.getBoundingClientRect(); }
              c.classList.remove('is-out');
            } else { c.hidden = true; c.classList.remove('is-out'); }
            c.classList.remove('pending'); c.classList.add('in');
          });
        }, 140);
      });
    });
  }

  // Contact form: inline checks, then a sent state. In concept mode nothing is sent.
  var form = document.getElementById('contact-form');
  if(form){
    var wrap = form.closest('.form-wrap');
    var setBad = function(field, msg){
      var box = field.closest('.field');
      box.classList.toggle('bad', !!msg);
      box.querySelector('.err').textContent = msg || '';
      field.setAttribute('aria-invalid', msg ? 'true' : 'false');
    };
    var check = function(field){
      var v = field.value.trim(), msg = '';
      if(field.name === 'name' && !v) msg = 'Tell us your name.';
      if(field.name === 'phone' && v && !/^[+\d][\d\s()-]{8,}$/.test(v)) msg = 'That number looks too short.';
      if(field.name === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = 'Check the email address.';
      if(field.name === 'message' && v.length < 5) msg = 'Add a short message.';
      setBad(field, msg);
      return !msg;
    };
    $$('input,select,textarea', form).forEach(function(f){
      f.addEventListener('blur', function(){ if(f.value) check(f); });
      f.addEventListener('input', function(){ if(f.closest('.field').classList.contains('bad')) check(f); });
    });
    form.addEventListener('submit', function(e){
      e.preventDefault();
      var ok = true, first = null;
      $$('input,select,textarea', form).forEach(function(f){ if(!check(f)){ ok = false; first = first || f; } });
      var phone = form.elements.phone, email = form.elements.email;
      if(!phone.value.trim() && !email.value.trim()){
        setBad(phone, 'Give us a phone number or an email so we can reply.');
        ok = false; first = first || phone;
      }
      var submit = form.querySelector('[type=submit]');
      if(!ok){
        first.focus();
        if(!reduce){ submit.classList.remove('shake'); submit.getBoundingClientRect(); submit.classList.add('shake'); }
        return;
      }
      submit.setAttribute('aria-busy', 'true');
      submit.firstChild.textContent = 'Sending… ';
      var done = function(){
        wrap.classList.add('is-sent');
        var sent = wrap.querySelector('.sent'); sent.setAttribute('tabindex', '-1'); sent.focus();
      };
      if(form.getAttribute('data-concept') === 'true'){ setTimeout(done, 500); return; }
      fetch(form.action, {method:'POST', body:new FormData(form), headers:{'Accept':'application/json'}})
        .then(function(r){ if(!r.ok) throw 0; done(); })
        .catch(function(){
          submit.removeAttribute('aria-busy'); submit.firstChild.textContent = 'Send message ';
          setBad(form.elements.message, 'That did not send. Please call the branch instead.');
        });
    });
  }

  // Store map (Leaflet + OpenStreetMap). The list beside it works without JS.
  var mapEl = document.getElementById('map'), dataEl = document.getElementById('store-data');
  if(mapEl && dataEl && window.L){
    var stores = JSON.parse(dataEl.textContent);
    mapEl.innerHTML = '';
    var map = L.map(mapEl, {scrollWheelZoom:false, zoomControl:true, attributionControl:true});
    L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {maxZoom:18, attribution:'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'}).addTo(map);
    var markers = {}, btns = $$('.stores button[data-store]');
    var setOn = function(id){
      btns.forEach(function(b){ b.setAttribute('aria-pressed', b.getAttribute('data-store') === id); });
      Object.keys(markers).forEach(function(k){ var el = markers[k].getElement(); if(el) el.classList.toggle('on', k === id); });
    };
    stores.forEach(function(s){
      var icon = L.divIcon({className:'bpin ' + s.k, html:'<span><img src="img/' + (s.k === 'tb' ? 'bob-pin.png' : 'buddy.svg') + '" alt=""></span>', iconSize:[46,58], iconAnchor:[23,58], popupAnchor:[0,-56]});
      var m = L.marker(s.ll, {icon:icon, title:s.n, keyboard:true, zIndexOffset:s.k === 'tb' ? 500 : 0}).addTo(map);
      m.bindPopup('<strong>' + s.n + '</strong>' + (s.a ? s.a + '<br>' : '') + '<a href="tel:' + s.e + '">' + s.t + '</a> · <a href="' + s.d + '" target="_blank" rel="noopener">Directions</a>');
      m.on('click', function(){ setOn(s.id); });
      markers[s.id] = m;
    });
    var all = L.featureGroup(Object.keys(markers).map(function(k){ return markers[k]; }));
    map.fitBounds(all.getBounds(), {padding:[40,40]});
    btns.forEach(function(b){
      b.addEventListener('click', function(e){
        if(e.target.closest('a')) return;
        var id = b.getAttribute('data-store'), m = markers[id];
        setOn(id);
        map.flyTo(m.getLatLng(), 14, {duration: reduce ? 0 : .8});
        m.openPopup();
      });
    });
  }

  // Scroll reveal: only hide what starts below the fold, so the first frame is complete.
  var items = $$('.rv');
  if(!('IntersectionObserver' in window)) return;
  var vh = window.innerHeight;
  // Stagger cards in a grid 60ms apart
  $$('.pylon,.bgrid,.panels,.yards').forEach(function(g){
    $$(':scope > .rv', g).forEach(function(c,i){ c.style.setProperty("--d", (Math.min(i,8)*60)+"ms"); });
  });
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if(!en.isIntersecting) return;
      var el = en.target;
      el.classList.remove('pending'); el.classList.add('in');
      io.unobserve(el);
      $$('[data-count]', el).forEach(countUp);
    });
  }, {rootMargin:'0px 0px -12% 0px', threshold:0.01});
  items.forEach(function(el){
    if(el.getBoundingClientRect().top > vh * 0.92){ el.classList.add('pending'); io.observe(el); }
    else { el.classList.add('in'); $$('[data-count]', el).forEach(countUp); }
  });
  // Count-ups that sit outside any .rv (e.g. a hero) run on load
  $$('[data-count]').forEach(function(el){ if(!el.closest('.rv')) countUp(el); });
})();
