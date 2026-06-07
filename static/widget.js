/* Widget de empleos para estudiantes — Bienestar, Facultad de Minas (UNAL).
 * Incrustar en cualquier página con:
 *   <div class="empleos-estudiantes"></div>
 *   <script src="https://TU-USUARIO.github.io/TU-REPO/widget.js" defer></script>
 *
 * Lee 'empleos.json' (publicado en GitHub Pages, junto a este script) y, si no
 * lo encuentra, intenta la API Flask local (/api/empleos) para desarrollo.
 * Hereda la tipografía Ancízar de la página y combina con sus colores.
 */
(function () {
  var FONT = "'Ancizar sans', Tahoma, Geneva, sans-serif";

  var self = document.currentScript ||
             document.querySelector('script[src*="widget.js"]');
  var scriptUrl = self ? self.src : '';
  var jsonUrl = scriptUrl.replace(/[^\/?#]*([?#].*)?$/, 'empleos.json');
  var apiUrl = (scriptUrl ? new URL(scriptUrl).origin : '') + '/api/empleos?limite=80';

  var mount = document.querySelector('.empleos-estudiantes') ||
              document.querySelector('[data-empleos-estudiantes]');
  if (!mount) {
    mount = document.createElement('div');
    if (self && self.parentNode) self.parentNode.insertBefore(mount, self);
    else document.body.appendChild(mount);
  }

  mount.innerHTML = msg('Cargando empleos…', '#777');

  cargar(jsonUrl)
    .catch(function () { return cargar(apiUrl); })
    .then(function (data) { render(mount, (data && data.empleos) || []); })
    .catch(function () {
      mount.innerHTML = msg('No se pudieron cargar los empleos.', '#b94a48');
    });

  function cargar(u) {
    return fetch(u).then(function (r) {
      if (!r.ok) throw new Error('http ' + r.status);
      return r.json();
    });
  }

  function msg(t, color) {
    return '<p style="font:14px ' + FONT + ';color:' + color + '">' + t + '</p>';
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function fuenteLabel(s) {
    return { unal_minas: 'UNAL', jooble: 'Jooble', arbeitnow: 'Remoto' }[s] || s;
  }

  function render(el, empleos) {
    if (!empleos.length) {
      el.innerHTML = msg('No hay empleos disponibles ahora.', '#777');
      return;
    }
    var html =
      '<div style="font-family:' + FONT + ';color:#3d3d3d;max-width:780px">' +
      '<h3 style="font-family:' + FONT + ';color:#b07d0a;font-size:18px;' +
      'font-weight:700;margin:0;border-bottom:3px solid #f2a900;padding-bottom:6px">' +
      'Oportunidades para estudiantes</h3>' +
      '<p style="font-size:12px;color:#777;margin:6px 0 14px">Facultad de Minas · ' +
      empleos.length + ' vigentes</p>';
    empleos.forEach(function (e) {
      var tags = fuenteLabel(e.source);
      if (e.employment_type) tags += ' · ' + e.employment_type;
      html +=
        '<div style="padding:12px 0;border-bottom:1px solid #ebebeb">' +
        '<a href="' + esc(e.url) + '" target="_blank" rel="noopener" ' +
        'style="color:#135cae;text-decoration:none;font-weight:600;font-size:15px;' +
        'font-family:' + FONT + '">' + esc(e.title || 'Sin título') + '</a>' +
        '<div style="color:#666;font-size:13px;margin-top:3px">' +
        esc(e.company || '') + (e.location ? ' · ' + esc(e.location) : '') + '</div>' +
        '<div style="margin-top:5px;font-size:11px;color:#b07d0a;font-weight:700;' +
        'text-transform:uppercase;letter-spacing:.4px">' + esc(tags) + '</div>' +
        '</div>';
    });
    html += '</div>';
    el.innerHTML = html;
  }
})();
