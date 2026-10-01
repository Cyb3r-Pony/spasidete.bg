МЯСТО ЗА ВИДЕОТО НА ПЛАТФОРМАТА / SLOT FOR THE PLATFORM VIDEO
=============================================================

Вариант 1 — YouTube (препоръчан)
  1. Качете видеото в YouTube.
  2. Вземете идентификатора от адреса: youtube.com/watch?v=XXXXXXXXXXX
  3. В campaigns.html намерете блока <div class="videoslot"> и заменете
     <div class="videoslot__ph">…</div> с кода от коментара точно над него.

Вариант 2 — файл на сайта
  Файлът spasidete.mp4 в тази папка вече е готов за ползване.
  В campaigns.html заменете <div class="videoslot__ph">…</div> с:

  <video controls preload="metadata" width="100%" poster="assets/img/photos/hero.jpg">
    <source src="assets/video/spasidete.mp4" type="video/mp4">
  </video>

Забележка: видеото е 568x320 пиксела. На голям екран ще изглежда меко —
ако имате версия с по-висока резолюция, заменете файла със същото име.
