# LEMONICA — Sale Landing

Лендинг продажи действующего прибыльного ресторана LEMONICA (Голливуд, Флорида).
Образец структуры — проект G-Class Buyout Website («Мерседес»): тёмный hero с
видео, секции с индексами, editorial-типографика (Source Serif 4 + Source Sans 3),
двуязычие.

**Live:** https://farmersmilksmm-maker.github.io/lemonica-sale-landing/
(репозиторий: `farmersmilksmm-maker/lemonica-sale-landing`, GitHub Pages, ветка main)

## Запуск

Открыть `index.html` в браузере или поднять статический сервер:

```bash
cd ~/Documents/Limonika_Sale_Landing_2026-09-02
python3 -m http.server 8791   # http://127.0.0.1:8791/
```

## Структура

- `index.html` — одностраничный лендинг: hero (видео) → история → «почему это
  работает» → отзывы (ссылка на Google) → галерея → «о нас говорят» (блогеры,
  Yelp, OpenTable, сайт) → форма запроса → футер со ссылками.
- `styles.css` — айдентика: крем/чернила/лимонный акцент, адаптив 1100/640 px.
- `translations.js` — EN/RU тексты (EN по умолчанию, автодетект ru, выбор
  сохраняется в localStorage).
- `app.js` — переключение языка + форма запроса: отправка на FormSubmit
  (`farmersmilksmm+lemonica@gmail.com`, домен активирован 03.09.2026) → письмо
  с заявкой приходит на farmersmilksmm@gmail.com.
- `contacts.html` — отдельная страница контактов (Марк + почта + форма).
- `scripts/collect_inquiries.py` — watchdog-сборщик заявок: раз в 30 мин
  (cron `70b965813b6b`) проверяет ящик, пишет новые в `inquiries/Lemonica_Inquiries.csv`
  (локально, не в Git) и дублирует в Telegram. Повторы не считает.
- `assets/` — видео (исходник, 1080 и web-версия 720), фото, шрифты.
- `qa/` — скриншоты QA (desktop-full, desktop-hero, mobile-full, mobile-hero).
- `ASSETS.md` — реестр медиа, источники, статус прав, внешние ссылки.

## Факты на странице (проверено 02.09.2026)

- Google: 4.8★, 2,466 отзывов; сегмент чека $30–80
- Instagram @lemonica_miami: 28K+ подписчиков
- Адрес: 1817 N Young Circle, Hollywood, FL 33020 (ArtsPark)
- Основан в 2024; доставка DoorDash/Uber Eats; бронирования OpenTable

## TODO перед публикацией

1. Подтвердить права на фото/видео (см. ASSETS.md).
2. Секция «Голливуд — район, который растёт»: ждём статистику с платного
   сервиса от владельца (трафик US-1, доходы, радиусы 1/5 км, стройка).
3. По желанию: Google Analytics, кастомный домен.
