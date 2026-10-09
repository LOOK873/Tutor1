/* ธีมร่วมสำหรับหน้าเนื้อหา: ตั้งโหมดมืด/สว่าง + แถบบนสุด (กลับหน้าแรก, นับถอยหลัง, สลับโหมด) */
(function () {
  var r = document.documentElement, key = 'exam-theme', d = 'dark';
  try { d = localStorage.getItem(key) || 'dark'; } catch (e) {}
  r.setAttribute('data-theme', d);
  r.setAttribute('data-subject', /\/phy\//.test(location.pathname) ? 'phy' : 'math');
  var sun = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>';
  var moon = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  document.addEventListener('DOMContentLoaded', function () {
    var bar = document.createElement('header');
    bar.className = 'xt-bar';
    bar.innerHTML = '<div class="xt-in"><a class="xt-home" href="../index.html">← หน้าแรก</a>' +
      '<span class="xt-chip"><span class="xt-dot"></span><span id="xt-count"></span></span>' +
      '<button class="xt-toggle" type="button"></button></div>';
    document.body.insertBefore(bar, document.body.firstChild);
    var btn = bar.querySelector('.xt-toggle'), cnt = bar.querySelector('#xt-count');
    function paint() {
      btn.innerHTML = d === 'dark' ? sun : moon;
      btn.setAttribute('aria-label', d === 'dark' ? 'โหมดสว่าง' : 'โหมดมืด');
    }
    btn.addEventListener('click', function () {
      d = d === 'dark' ? 'light' : 'dark';
      r.setAttribute('data-theme', d);
      try { localStorage.setItem(key, d); } catch (e) {}
      paint();
    });
    paint();
    if (window.examChipText) cnt.textContent = examChipText();
  });
})();
