// LEMONICA sale landing — language switch + inquiry form (mailto compose)
(function () {
  "use strict";

  var CONTACT_EMAIL = "sale@lemonica.rest"; // TODO: replace with the broker/owner inbox before publishing

  var dict = window.I18N || { en: {}, ru: {} };
  var langs = ["en", "ru"];
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
    initial = nav === "ru" ? "ru" : "en";
  }
  applyLang(initial);

  // ---- inquiry form: compose a pre-filled email, store nothing ----
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

      var subject = "LEMONICA acquisition inquiry — " + name;
      var body = [
        "Name: " + name,
        "Email: " + email,
        phone ? "Phone / WhatsApp: " + phone : null,
        "",
        message || (t["form.message.ph"] || "")
      ].filter(function (l) { return l !== null; }).join("\n");

      window.location.href = "mailto:" + CONTACT_EMAIL +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(body);
    });
  }

  // ---- hero video: if autoplay is blocked, show poster via pause state ----
  var heroVideo = document.querySelector(".hero-video");
  if (heroVideo) {
    var p = heroVideo.play();
    if (p && p.catch) p.catch(function () { /* poster stays visible */ });
  }
})();
