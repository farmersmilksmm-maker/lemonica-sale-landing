// LEMONICA sale landing — language switch + inquiry form (mailto compose)
(function () {
  "use strict";

  var CONTACT_EMAIL = "farmersmilksmm@gmail.com";
  var FORM_EMAIL = "farmersmilksmm+lemonica@gmail.com"; // FormSubmit endpoint (plus-alias → separate form, same inbox)

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
        message: message || (t["form.message.ph"] || ""),
        _subject: "LEMONICA acquisition inquiry — " + name,
        _template: "table",
        _captcha: "false",
        _replyto: email
      };

      var btn = form.querySelector("button[type=submit]");
      if (btn) btn.disabled = true;
      fetch("https://formsubmit.co/ajax/" + FORM_EMAIL, {
        method: "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify(payload)
      }).then(function (r) {
        if (!r.ok) throw new Error("http " + r.status);
        return r.json();
      }).then(function () {
        status.className = "form-status ok";
        status.textContent = t["form.ok"] || "Sent.";
        form.reset();
      }).catch(function () {
        status.className = "form-status err";
        status.textContent = (t["form.err.send"] || "Sending failed.") + " " + CONTACT_EMAIL;
      }).finally(function () {
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
})();
