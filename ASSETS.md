# LEMONICA Sale Landing — Asset Registry

Дата регистрации: 2026-09-02

> Важно: фото и видео взяты с публичных источников (официальный сайт LEMONICA,
> Vimeo-ссылка, предоставленная владельцем). Перед публикацией лендинга
> публично необходимо подтвердить права на все медиа у правообладателя.

## Видео

| Файл | Источник | Технические данные | Назначение | Права |
|---|---|---|---|---|
| `assets/video/lemonica_vimeo_source.mp4` | https://vimeo.com/1158311461/c82cdc9eee (ссылка от владельца) | 1296×2304, 24 fps, H.264+AAC, 38.5 s, 49.7 MB | Исходник | Подтвердить у владельца |
| `assets/video/lemonica_hero_1080.mp4` | Производный из исходника | 1080×1920, H.264, без звука, 25.7 MB | Промежуточная версия | Наследует права |
| `assets/video/lemonica_hero.mp4` | Производная web-версия | 720×1280, H.264 High, yuv420p, Fast Start, без звука, 8.8 MB | Hero-фон сайта | Наследует права |

## Фото (официальный сайт lemonica.rest)

Интерьер и атмосфера: `main.jpg`, `IMG_8868-1.jpg`, `IMG_8373.jpg`, `IMG_7934.jpg`,
`IMG_0984.jpg`, `IMG_8375-1.jpg`, `DSC02810.jpg`, `DSC02892.jpg`, `DSC02894.jpg`,
`DSC02919-1.jpg`, `DSC02934.jpg`.
Блюда: `IMG_2613.jpg` – `IMG_2618.jpg`.

Кадры из Vimeo-видео (галерея и постер): `hero-poster.jpg` (кадр ~0 с),
`gallery-frame-1.jpg` (~16 с), `gallery-frame-2.jpg` (~22 с), `gallery-frame-3.jpg` (~35 с).

Все фото оптимизированы: max сторона 1600 px, JPEG q≈82.

## Проверка

- `lemonica_vimeo_source.mp4` полностью декодирован FFmpeg без ошибок (`-xerror`);
- web-версия: H.264 + yuv420p + Fast Start — совместимость с автовоспроизведением
  (autoplay) в Safari/Chrome подтверждена контейнером; в headless-окружении
  браузерная песочница не отдаёт локальные медиа — на постере (кадр f01) страница
  выглядит корректно, что подтверждает fallback;
- все ресурсы отдаются с HTTP 200; JS-синтаксис проверен; RU/EN-переключение
  проверено кликом; мобильная вёрстка 390 px — без горизонтального скролла
  (scrollWidth == innerWidth).

## Внешние ссылки на лендинге

- Google Maps / отзывы: https://www.google.com/maps/place/LEMONICA/@26.0127406,-80.1438862,17z (4.8★, 2,466 отзывов — данные на 02.09.2026)
- Instagram: https://www.instagram.com/lemonica_miami
- Сайт: https://www.lemonica.rest
- OpenTable: https://www.opentable.com/r/lemonica-hollywood
- Yelp: https://www.yelp.com/biz/lemonica-hollywood
- Facebook-группа Let's Eat South Florida (обзор)
