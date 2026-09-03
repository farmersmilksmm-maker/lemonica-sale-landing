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
- `app.js` — переключение языка + форма запроса (открывает почтовое приложение
  с готовым письмом, ничего не хранит).
- `assets/` — видео (исходник, 1080 и web-версия 720), фото, шрифты.
- `qa/` — скриншоты QA (desktop-full, desktop-hero, mobile-full, mobile-hero).
- `ASSETS.md` — реестр медиа, источники, статус прав, внешние ссылки.

## Факты на странице (проверено 02.09.2026)

- Google: 4.8★, 2,466 отзывов; сегмент чека $30–80
- Instagram @lemonica_miami: 28K+ подписчиков
- Адрес: 1817 N Young Circle, Hollywood, FL 33020 (ArtsPark)
- Основан в 2024; доставка DoorDash/Uber Eats; бронирования OpenTable

## TODO перед публикацией

1. **Заменить email получателя** формы — сейчас `sale@lemonica.rest` (заглушка),
   см. `CONTACT_EMAIL` в `app.js`. Можно заменить на WhatsApp/Telegram-ссылку.
2. Подтвердить права на фото/видео (см. ASSETS.md).
3. По желанию: подключить бекенд формы вместо mailto, добавить Google Analytics.
4. Хостинг: любой статический (GitHub Pages / Netlify / S3).
