(function(){
  var V = window.CLEVR_UNIVERSE_DATA || [];
  var pad = function(n){ return (n<10?'0':'')+n; };
  var esc = function(s){ return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); };

  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var mobileQuery = window.matchMedia && window.matchMedia('(max-width: 760px)');
  var isMobile = function(){ return !!(mobileQuery && mobileQuery.matches); };
  var stage = document.getElementById('uni-stage');
  var cvs = document.getElementById('uni-sky');
  var ctx = cvs.getContext('2d');
  var panel = document.getElementById('uni-panel');
  var hint = document.getElementById('uni-hint');

  var sel = null, selM = null, hover = false;

  // nodes
  var core = document.createElement('button');
  core.type = 'button'; core.className = 'uni-node uni-core'; core.setAttribute('aria-label','Clevr, ver todas las soluciones');
  core.innerHTML = '<span class="w">clev<em>r</em></span><span class="c">SOLUCIONES</span>';
  core.addEventListener('click', function(){ select(null,null); });
  stage.appendChild(core);

  V.forEach(function(v, i){
    v.base = -Math.PI/2 + i*Math.PI/2;
    v.sat = Math.random()*Math.PI*2;
    v.satSpeed = 1;
    var p = document.createElement('button');
    p.type = 'button'; p.className = 'uni-node uni-planet';
    p.setAttribute('aria-label','Área '+v.name);
    p.setAttribute('aria-controls','uni-panel');
    p.innerHTML = '<span class="n">'+esc(v.short)+'</span>';
    p.addEventListener('click', function(){ select(i,null); });
    v.el = p;
    v.modEls = v.mods.map(function(m, j){
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'uni-node uni-mod';
      b.setAttribute('aria-label','Solución '+m[0]+', '+v.name);
      b.setAttribute('aria-controls','uni-panel');
      b.innerHTML = '<i></i><span class="lbl">'+esc(m[0])+'</span>';
      b.addEventListener('click', function(){ select(i,j); });
      stage.appendChild(b);
      return b;
    });
    stage.appendChild(p);
  });

  stage.addEventListener('mouseenter', function(){ hover = true; });
  stage.addEventListener('mouseleave', function(){ hover = false; });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && sel !== null) select(null,null); });

  // background stars
  var stars = [];
  for (var k=0;k<140;k++) stars.push({ x:Math.random(), y:Math.random(), r:Math.random()<.85?.7:1.3, ph:Math.random()*6.28, sp:.4+Math.random()*1.2 });

  var S = 0, dpr = 1;
  function resize(){
    S = stage.clientWidth;
    dpr = Math.min(window.devicePixelRatio || 1, 2);
    cvs.width = Math.round(S*dpr); cvs.height = Math.round(S*dpr);
    var coreD = Math.max(76, S*.19);
    core.style.width = coreD+'px'; core.style.height = coreD+'px';
    core.querySelector('.w').style.fontSize = Math.max(18, S*.04)+'px';
    core.querySelector('.c').style.fontSize = (S < 400 ? Math.max(5.5, S*.02) : Math.max(8, S*.012))+'px';
    var P = Math.max(64, Math.min(132, S*.16));
    V.forEach(function(v){
      v.el.style.width = P+'px'; v.el.style.height = P+'px';
      v.el.querySelector('.n').style.fontSize = Math.max(11, P*.12)+'px';
      v.el.querySelector('.k').style.fontSize = (P < 80 ? Math.max(5.5, P*.09) : Math.max(8, P*.075))+'px';
    });
  }
  if (window.ResizeObserver) new ResizeObserver(resize).observe(stage); else window.addEventListener('resize', resize);
  resize();

  var main = 0, mainSpeed = 1, last = performance.now(), t = 0;
  var pos = [];
  var inView = false;
  var rafId = 0;

  function frame(now){
    var dt = Math.min(.05, (now-last)/1000); last = now; t += dt;
    var targetMain = reduce ? 0 : ((hover || sel !== null) ? 0 : 1);
    mainSpeed += (targetMain - mainSpeed) * Math.min(1, dt*3);
    main += dt * (Math.PI*2/110) * mainSpeed;

    var c = S/2, R1 = S*.32, R2 = S*.15, coreD = core.offsetWidth, P = V[0].el.offsetWidth;
    core.style.transform = 'translate('+(c-coreD/2)+'px,'+(c-coreD/2)+'px)';
    pos = V.map(function(v, i){
      var tS = reduce ? 0 : (hover ? 0 : (sel === null ? 1 : (sel === i ? .35 : 0)));
      v.satSpeed += (tS - v.satSpeed) * Math.min(1, dt*3);
      v.sat += dt * (Math.PI*2/v.dur) * v.satSpeed;
      var a = v.base + main, px = c + R1*Math.cos(a), py = c + R1*Math.sin(a);
      v.el.style.transform = 'translate('+(px-P/2)+'px,'+(py-P/2)+'px)';
      var ms = v.mods.map(function(m, j){
        var b = v.sat + j*Math.PI*2/v.mods.length, mx = px + R2*Math.cos(b), my = py + R2*Math.sin(b);
        v.modEls[j].style.transform = 'translate('+(mx-15)+'px,'+(my-15)+'px)';
        var label = v.modEls[j].querySelector('.lbl');
        label.classList.toggle('uni-label-left', mx < S*.28);
        label.classList.toggle('uni-label-right', mx > S*.72);
        return [mx,my];
      });
      return { x:px, y:py, ms:ms };
    });
    draw(c, R1, R2, coreD);
    if (inView && !reduce) rafId = requestAnimationFrame(frame);
  }

  function draw(c, R1, R2, coreD){
    ctx.setTransform(dpr,0,0,dpr,0,0);
    ctx.clearRect(0,0,S,S);
    // stars
    stars.forEach(function(s){
      var a = reduce ? .45 : .12 + .6*(.5+.5*Math.sin(t*s.sp + s.ph));
      ctx.fillStyle = 'rgba(255,255,255,'+a.toFixed(3)+')';
      ctx.beginPath(); ctx.arc(s.x*S, s.y*S, s.r, 0, 6.283); ctx.fill();
    });
    // nebula glow
    var g = ctx.createRadialGradient(c,c,0,c,c,S*.36);
    g.addColorStop(0,'rgba(231,106,58,.20)'); g.addColorStop(.5,'rgba(231,106,58,.06)'); g.addColorStop(1,'rgba(231,106,58,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(c,c,S*.36,0,6.283); ctx.fill();
    // outer + main orbits
    ctx.lineWidth = 1;
    ctx.strokeStyle = 'rgba(223,229,236,.05)'; ctx.beginPath(); ctx.arc(c,c,S*.47,0,6.283); ctx.stroke();
    ctx.setLineDash([3,7]); ctx.strokeStyle = 'rgba(255,170,132,.25)'; ctx.beginPath(); ctx.arc(c,c,R1,0,6.283); ctx.stroke(); ctx.setLineDash([]);
    // core pulses
    if (!reduce) for (var q=0;q<2;q++){
      var f = ((t/3.6) + q*.5) % 1, rr = coreD/2*(1+f*1.3);
      ctx.strokeStyle = 'rgba(255,170,132,'+(.5*(1-f)).toFixed(3)+')';
      ctx.beginPath(); ctx.arc(c,c,rr,0,6.283); ctx.stroke();
    }
    pos.forEach(function(p, i){
      var on = sel === i, dim = sel !== null && !on;
      // spoke
      ctx.strokeStyle = on ? 'rgba(255,170,132,.6)' : (dim ? 'rgba(223,229,236,.04)' : 'rgba(223,229,236,.13)');
      ctx.beginPath(); ctx.moveTo(c,c); ctx.lineTo(p.x,p.y); ctx.stroke();
      if (!reduce && !dim){
        var f = ((t/2.6) + i*.25) % 1, x = c + (p.x-c)*f, y = c + (p.y-c)*f;
        ctx.fillStyle = 'rgba(255,170,132,'+(Math.sin(f*Math.PI)).toFixed(3)+')';
        ctx.beginPath(); ctx.arc(x,y,2.4,0,6.283); ctx.fill();
      }
      // satellite ring
      ctx.strokeStyle = on ? 'rgba(255,170,132,.45)' : (dim ? 'rgba(223,229,236,.03)' : 'rgba(223,229,236,.09)');
      ctx.beginPath(); ctx.arc(p.x,p.y,R2,0,6.283); ctx.stroke();
      // constellation lines for selected vertical
      if (on && !isMobile()){
        ctx.strokeStyle = 'rgba(255,170,132,.16)';
        p.ms.forEach(function(m, j){
          ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(m[0],m[1]); ctx.stroke();
          var n = p.ms[(j+1)%p.ms.length];
          ctx.strokeStyle = 'rgba(223,229,236,.10)'; ctx.beginPath(); ctx.moveTo(m[0],m[1]); ctx.lineTo(n[0],n[1]); ctx.stroke();
          ctx.strokeStyle = 'rgba(255,170,132,.16)';
        });
        if (selM !== null){
          var m = p.ms[selM];
          ctx.strokeStyle = 'rgba(231,106,58,.85)'; ctx.lineWidth = 1.5;
          ctx.beginPath(); ctx.moveTo(p.x,p.y); ctx.lineTo(m[0],m[1]); ctx.stroke(); ctx.lineWidth = 1;
        }
      }
    });
  }

  function select(i, j){
    sel = i; selM = (i === null) ? null : j;
    V.forEach(function(v, k){
      var on = sel === k, dim = sel !== null && !on;
      v.el.classList.toggle('uni-on', on); v.el.classList.toggle('uni-dim', dim);
      v.el.setAttribute('aria-pressed', on ? 'true' : 'false');
      v.el.setAttribute('aria-expanded', on ? 'true' : 'false');
      v.modEls.forEach(function(b, n){
        b.classList.toggle('uni-show', on); b.classList.toggle('uni-dim', dim);
        b.classList.toggle('uni-on', on && selM === n);
      });
    });
    hint.textContent = sel === null ? 'CADA ESTRELLA ES UNA SOLUCIÓN · PASA EL CURSOR PARA PAUSAR' : 'TOCA UNA ESTRELLA PARA VER SU SOLUCIÓN · TOCA CLEVR PARA VOLVER';
    renderPanel();
    if (sel !== null && isMobile()) requestAnimationFrame(function(){ panel.scrollIntoView({behavior:reduce?'auto':'smooth',block:'start'}); });
  }

  function renderPanel(){
    var h;
    if (sel === null){
      h = '<div class="uni-card"><div class="uni-kicker">CLEVR · SOLUCIONES</div><h2>Elige un área y explora sus soluciones.</h2>'+
          '<p>Agentes, automatizaciones y herramientas conectadas a los sistemas que ya usa tu equipo.</p><div class="uni-list">'+
          V.map(function(v, i){ return '<button type="button" class="uni-row" data-v="'+i+'">Soluciones para '+esc(v.name)+'<span class="m">→</span></button>'; }).join('')+
          '</div></div>';
    } else {
      var v = V[sel];
      h = '<div class="uni-card"><button type="button" class="uni-back" data-core="1">← TODAS LAS SOLUCIONES</button>'+
          '<div class="uni-kicker" style="margin-top:6px">ÁREA · '+esc(v.name)+'</div><h2>Soluciones para '+esc(v.name)+'</h2><p>'+esc(v.desc)+'</p><div class="uni-list">'+
          v.mods.map(function(m, j){ return '<button type="button" class="uni-row uni-mrow'+(selM===j?' uni-on':'')+'" aria-pressed="'+(selM===j)+'" data-m="'+j+'"><span class="m">'+pad(j+1)+'</span>'+esc(m[0])+'</button>'; }).join('')+
          '</div>'+(selM !== null ? '<div class="uni-detail"><b>'+esc(v.mods[selM][0])+'</b><span>'+esc(v.mods[selM][1])+'</span></div>' : '')+
          '<a class="uni-cta" href="#agendar">Conversemos →</a></div>';
    }
    panel.innerHTML = h;
  }
  panel.addEventListener('click', function(e){
    var b = e.target.closest('button'); if (!b) return;
    if (b.dataset.core) select(null,null);
    else if (b.dataset.v !== undefined) select(+b.dataset.v, null);
    else if (b.dataset.m !== undefined) select(sel, +b.dataset.m);
  });

  renderPanel();
  if ('IntersectionObserver' in window) {
    var visibilityObserver = new IntersectionObserver(function(entries){
      var visible = entries.some(function(entry){ return entry.isIntersecting; });
      if (visible && !inView) {
        inView = true;
        last = performance.now();
        frame(last);
      } else if (!visible && inView) {
        inView = false;
        cancelAnimationFrame(rafId);
      }
    }, { threshold: 0.01 });
    visibilityObserver.observe(document.getElementById('universo-clevr'));
  } else {
    inView = true;
    frame(performance.now());
  }
  window.addEventListener('resize', function(){ if (reduce && inView) frame(performance.now()); });
})();
