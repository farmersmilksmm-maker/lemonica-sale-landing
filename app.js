// LEMONICA sale landing — language switch + inquiry form (mailto compose)
(function () {
  "use strict";

  var CONTACT_EMAIL = "farmersmilksmm@gmail.com";
  var FORM_EMAIL = "farmersmilksmm+lemonica@gmail.com"; // FormSubmit endpoint (plus-alias → separate form, same inbox)

  var dict = window.I18N || { en: {}, ru: {}, es: {}, uk: {}, el: {} };
  var langs = ["en", "ru", "es", "uk", "el"];
  var stored = null;
  try { stored = localStorage.getItem("lemonica-lang"); } catch (e) {}

  function applyLang(lang) {
    if (langs.indexOf(lang) === -1) lang = "en";
    var t = dict[lang];
    document.documentElement.setAttribute("lang", lang);

    document.querySelectorAll("[data-i18n]").forEach(function (el) {
      var key = el.getAttribute("data-i18n");
      if (t[key] != null) el.textContent = t[key];
    });
    document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-html");
      if (t[key] != null) el.innerHTML = t[key];
    });
    document.querySelectorAll("[data-i18n-ph]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-ph");
      if (t[key] != null) el.setAttribute("placeholder", t[key]);
    });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
      var key = el.getAttribute("data-i18n-aria");
      if (t[key] != null) el.setAttribute("aria-label", t[key]);
    });
    document.querySelectorAll(".language-switcher button").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.getAttribute("data-lang") === lang));
    });
    try { localStorage.setItem("lemonica-lang", lang); } catch (e) {}
  }

  document.querySelectorAll(".language-switcher button").forEach(function (b) {
    b.addEventListener("click", function () { applyLang(b.getAttribute("data-lang")); });
  });

  var initial = stored;
  if (!initial) {
    var nav = (navigator.language || "en").slice(0, 2).toLowerCase();
    initial = (nav === "ru" || nav === "es" || nav === "uk" || nav === "el") ? nav : "en";
  }
  applyLang(initial);

  // ---- inquiry form: send straight to the Farmer's Milk SMM mailbox ----
  var form = document.getElementById("inquiry-form");
  var status = document.getElementById("form-status");
  if (form) {
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      var t = dict[document.documentElement.getAttribute("lang")] || dict.en;
      var name = form.name.value.trim();
      var email = form.email.value.trim();
      var phone = form.phone.value.trim();
      var message = form.message.value.trim();
      var valid = name && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);

      status.className = "form-status " + (valid ? "ok" : "err");
      status.textContent = valid ? (t["form.ok"] || "") : (t["form.err.required"] || "");
      if (!valid) return;

      var payload = {
        name: name,
        email: email,
        phone: phone || "—",
        message: message || "",
        _subject: "LEMONICA acquisition inquiry — " + name,
        _template: "table",
        _captcha: "false",
        _replyto: email
      };

      var btn = form.querySelector("button[type=submit]");
      if (btn) btn.disabled = true;
      var sendOnce = function () {
        return fetch("https://formsubmit.co/ajax/" + FORM_EMAIL, {
          method: "POST",
          headers: { "Content-Type": "application/json", "Accept": "application/json" },
          body: JSON.stringify(payload)
        }).then(function (r) {
          if (!r.ok) throw new Error("http " + r.status);
          return r.json();
        }).then(function (j) {
          if (String(j && j.success) !== "true") throw new Error("rejected");
        });
      };
      sendOnce()
        .catch(sendOnce)
        .then(function () {
          status.className = "form-status ok";
          status.textContent = t["form.ok"] || "Sent.";
          form.reset();
        })
        .catch(function () {
          status.className = "form-status err";
          var subject = "LEMONICA acquisition inquiry — " + name;
          var body = ["Name: " + name, "Email: " + email,
                      phone ? "Phone / WhatsApp: " + phone : "", "", message || ""]
                      .filter(function (l) { return l !== ""; }).join("\n");
          status.textContent = "";
          status.appendChild(document.createTextNode((t["form.err.send"] || "Sending failed.") + " "));
          var a = document.createElement("a");
          a.href = "mailto:" + CONTACT_EMAIL +
            "?subject=" + encodeURIComponent(subject) +
            "&body=" + encodeURIComponent(body);
          a.textContent = CONTACT_EMAIL;
          a.setAttribute("style", "font-weight:700;text-decoration:underline;");
          status.appendChild(a);
        })
        .finally(function () {
          if (btn) btn.disabled = false;
        });
    });
  }

  // ---- hero video: if autoplay is blocked, show poster via pause state ----
  var heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    var p = heroVideo.play();
    if (p && p.catch) p.catch(function () { /* poster stays visible */ });
  }

  // ---- background music: browsers block sound autoplay, so we start on the
  // first user gesture; EVERY gesture retries (a rejected first attempt must
  // not lock music off), and the toggle always works ----
  var music = document.getElementById("bg-music");
  var musicBtn = document.getElementById("music-toggle");
  if (music && musicBtn) {
    music.volume = 0.35;
    var musicUserOff = false;
    try { musicUserOff = localStorage.getItem("lemonica-music") === "off"; } catch (e) {}

    var setBtn = function (playing) {
      musicBtn.setAttribute("aria-pressed", String(playing));
      musicBtn.classList.toggle("playing", playing);
    };
    var startMusic = function () {
      if (musicUserOff || !music.paused) return;
      var mp = music.play();
      if (mp && mp.then) {
        mp.then(function () { setBtn(true); }).catch(function () { setBtn(false); });
      } else {
        setBtn(true);
      }
    };

    // autoplay attempt (usually rejected until the first gesture — harmless)
    startMusic();
    // retry on every gesture — pointer, touch AND click
    ["pointerdown", "touchend", "click", "keydown"].forEach(function (evt) {
      document.addEventListener(evt, startMusic, { passive: true });
    });

    musicBtn.addEventListener("click", function () {
      if (music.paused) {
        musicUserOff = false;
        try { localStorage.setItem("lemonica-music", "on"); } catch (e) {}
        startMusic();
      } else {
        musicUserOff = true;
        try { localStorage.setItem("lemonica-music", "off"); } catch (e) {}
        music.pause();
        setBtn(false);
      }
    });
  }
})();
