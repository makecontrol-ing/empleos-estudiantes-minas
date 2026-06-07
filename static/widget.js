/* Widget de empleos para estudiantes — Bienestar, Facultad de Minas (UNAL).
 * Incrustar con:
 *   <div class="empleos-estudiantes"></div>
 *   <script src="https://makecontrol-ing.github.io/empleos-estudiantes-minas/widget.js" defer></script>
 *
 * Lee 'empleos.json' (junto a este script) y, si no lo encuentra, intenta la
 * API Flask local (/api/empleos). Incluye buscador y filtros (todo en el cliente).
 * Hereda la tipografía Ancízar de la página y combina con sus colores.
 */
(function () {
  var self = document.currentScript ||
             document.querySelector('script[src*="widget.js"]');
  var scriptUrl = self ? self.src : '';
  var jsonUrl = scriptUrl.replace(/[^\/?#]*([?#].*)?$/, 'empleos.json');
  var apiUrl = (scriptUrl ? new URL(scriptUrl).origin : '') + '/api/empleos?limite=200';

  var mount = document.querySelector('.empleos-estudiantes') ||
              document.querySelector('[data-empleos-estudiantes]');
  if (!mount) {
    mount = document.createElement('div');
    if (self && self.parentNode) self.parentNode.insertBefore(mount, self);
    else document.body.appendChild(mount);
  }

  inyectarEstilos();
  mount.innerHTML = '<p class="ee-vacio">Cargando empleos…</p>';

  cargar(jsonUrl)
    .catch(function () { return cargar(apiUrl); })
    .then(function (data) { construir(mount, (data && data.empleos) || []); })
    .catch(function () {
      mount.innerHTML =
        '<p class="ee-vacio" style="color:#b94a48">No se pudieron cargar los empleos.</p>';
    });

  function cargar(u) {
    return fetch(u).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.json();
    });
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  var DIACRITICOS = new RegExp('[\\u0300-\\u036f]', 'g');
  function norm(s) {
    // minúsculas e ignora acentos (á -> a) para buscar mejor en español
    return String(s == null ? '' : s).toLowerCase().normalize('NFD').replace(DIACRITICOS, '');
  }

  function fuenteLabel(s) {
    return { unal_minas: 'UNAL', jooble: 'Jooble', arbeitnow: 'Remoto' }[s] || s;
  }

  // Filtros por TIPO de oportunidad (chips)
  var FILTROS = [
    { key: 'all', label: 'Todas' },
    { key: 'practicas', label: 'Prácticas' },
    { key: 'aprendiz', label: 'Aprendiz' },
    { key: 'medio', label: 'Medio tiempo' },
    { key: 'unal', label: 'UNAL' },
  ];

  function pasaFiltro(e, key) {
    if (key === 'all') return true;
    if (key === 'unal') return e.source === 'unal_minas';
    var t = norm((e.title || '') + ' ' + (e.employment_type || ''));
    if (key === 'practicas') return /practic|pasant/.test(t);
    if (key === 'aprendiz') return /aprendiz/.test(t);
    if (key === 'medio') return /medio tiempo|parcial|part.?time/.test(t);
    return true;
  }

  function itemHtml(e) {
    var tags = fuenteLabel(e.source);
    if (e.employment_type) tags += ' · ' + e.employment_type;
    return '<div class="ee-item">' +
      '<a href="' + esc(e.url) + '" target="_blank" rel="noopener">' +
      esc(e.title || 'Sin título') + '</a>' +
      '<div class="ee-meta">' + esc(e.company || '') +
      (e.location ? ' · ' + esc(e.location) : '') + '</div>' +
      '<div class="ee-tags">' + esc(tags) + '</div></div>';
  }

  function construir(el, empleos) {
    if (!empleos.length) {
      el.innerHTML = '<p class="ee-vacio">No hay empleos disponibles ahora.</p>';
      return;
    }
    el.innerHTML =
      '<div class="ee-wrap">' +
        '<h3 class="ee-h">Oportunidades para estudiantes</h3>' +
        '<div class="ee-sub">Facultad de Minas · <span class="ee-contador"></span></div>' +
        '<div class="ee-controls">' +
          '<input class="ee-buscar" type="text" aria-label="Buscar" ' +
          'placeholder="Buscar cargo, empresa o palabra…">' +
          FILTROS.map(function (f, i) {
            return '<button class="ee-chip' + (i === 0 ? ' activo' : '') +
              '" data-f="' + f.key + '">' + f.label + '</button>';
          }).join('') +
        '</div>' +
        '<div class="ee-lista"></div>' +
      '</div>';

    var lista = el.querySelector('.ee-lista');
    var contador = el.querySelector('.ee-contador');
    var buscar = el.querySelector('.ee-buscar');
    var chips = el.querySelectorAll('.ee-chip');
    var estado = { q: '', filtro: 'all' };

    function aplicar() {
      var q = norm(estado.q);
      var res = empleos.filter(function (e) {
        if (!pasaFiltro(e, estado.filtro)) return false;
        if (!q) return true;
        return norm((e.title || '') + ' ' + (e.company || '') + ' ' +
          (e.location || '') + ' ' + (e.employment_type || '')).indexOf(q) !== -1;
      });
      contador.textContent = res.length + (res.length === 1 ? ' resultado' : ' resultados');
      lista.innerHTML = res.length
        ? res.map(itemHtml).join('')
        : '<p class="ee-vacio">Sin resultados para tu búsqueda.</p>';
    }

    buscar.addEventListener('input', function () { estado.q = buscar.value; aplicar(); });
    Array.prototype.forEach.call(chips, function (c) {
      c.addEventListener('click', function () {
        estado.filtro = c.getAttribute('data-f');
        Array.prototype.forEach.call(chips, function (x) { x.classList.remove('activo'); });
        c.classList.add('activo');
        aplicar();
      });
    });

    aplicar();
  }

  function inyectarEstilos() {
    if (document.getElementById('ee-estilos')) return;
    var css =
      ".ee-wrap{font-family:'Ancizar sans',Tahoma,Geneva,sans-serif;color:#3d3d3d;max-width:780px}" +
      ".ee-h{color:#b07d0a;font-size:18px;font-weight:700;margin:0;border-bottom:3px solid #f2a900;padding-bottom:6px}" +
      ".ee-sub{font-size:12px;color:#777;margin:6px 0 12px}" +
      ".ee-controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:12px}" +
      ".ee-buscar{flex:1;min-width:190px;padding:8px 10px;border:1px solid #d9d4c7;border-radius:6px;font-family:inherit;font-size:14px;color:#3d3d3d;background:#fff}" +
      ".ee-buscar:focus{outline:none;border-color:#f2a900;box-shadow:0 0 0 2px rgba(242,169,0,.25)}" +
      ".ee-chip{border:1px solid #d9d4c7;background:#fff;color:#666;font-family:inherit;font-weight:600;font-size:12px;padding:6px 12px;border-radius:999px;cursor:pointer}" +
      ".ee-chip:hover{border-color:#f2a900}" +
      ".ee-chip.activo{background:#f2a900;border-color:#f2a900;color:#3d3d3d}" +
      ".ee-item{padding:12px 0;border-bottom:1px solid #ebebeb}" +
      ".ee-item a{color:#135cae;text-decoration:none;font-weight:600;font-size:15px}" +
      ".ee-item a:hover{text-decoration:underline}" +
      ".ee-meta{color:#666;font-size:13px;margin-top:3px}" +
      ".ee-tags{margin-top:5px;font-size:11px;color:#b07d0a;font-weight:700;text-transform:uppercase;letter-spacing:.4px}" +
      ".ee-vacio{color:#777;font-size:14px;padding:16px 0}";
    var st = document.createElement('style');
    st.id = 'ee-estilos';
    st.textContent = css;
    (document.head || document.documentElement).appendChild(st);
  }
})();
