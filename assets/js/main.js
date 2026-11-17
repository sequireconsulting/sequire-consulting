/* Sequire Consulting — small progressive enhancements. The site works without JS. */
(function () {
  document.documentElement.classList.remove("no-js");

  // Mobile navigation
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      toggle.setAttribute("aria-expanded", String(!open));
      nav.classList.toggle("is-open", !open);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a")) {
        toggle.setAttribute("aria-expanded", "false");
        nav.classList.remove("is-open");
      }
    });
  }

  // "See our approach" cards
  document.querySelectorAll(".toggle").forEach(function (btn) {
    var body = document.getElementById(btn.getAttribute("aria-controls"));
    var label = btn.querySelector(".toggle__label");
    body.setAttribute("inert", ""); // collapsed content stays in the page for search, but out of tab order
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") === "true";
      btn.setAttribute("aria-expanded", String(!open));
      body.classList.toggle("is-open", !open);
      body.toggleAttribute("inert", open);
      label.textContent = open ? "See our approach" : "Close";
    });
  });

  // Current year in footer
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
