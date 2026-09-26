(() => {
  "use strict";
  const products = JSON.parse(document.getElementById("products-data").textContent);
  const byId = new Map(products.map((product) => [product.id, product]));
  const storageKey = "nutricol-quote-selection";
  let selection;
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || "[]");
    selection = Array.isArray(saved) ? [...new Set(saved.map(String))].filter((id) => byId.has(id)) : [];
  } catch {
    selection = [];
  }
  const drawer = document.getElementById("quote-drawer");
  const panel = drawer.querySelector(".drawer-panel");
  const items = document.getElementById("drawer-items");
  const footer = document.getElementById("drawer-footer");
  let previousFocus = null;

  function persist() {
    try { localStorage.setItem(storageKey, JSON.stringify(selection)); } catch { /* Storage unavailable; selection remains in memory. */ }
    renderSelection();
  }
  function renderSelection() {
    document.querySelectorAll("[data-quote-count]").forEach((el) => { el.textContent = selection.length; });
    document.querySelectorAll("[data-add-product]").forEach((button) => {
      const added = selection.includes(button.dataset.addProduct);
      button.classList.toggle("is-added", added);
      button.innerHTML = added ? 'Agregado <span aria-hidden="true">✓</span>' : 'Agregar <span aria-hidden="true">＋</span>';
      button.setAttribute("aria-pressed", String(added));
    });
    items.replaceChildren();
    footer.replaceChildren();
    if (!selection.length) {
      const empty = document.createElement("div");
      empty.className = "drawer-empty";
      empty.innerHTML = '<span class="empty-mark" aria-hidden="true">∅</span><h3>Aún no hay productos aquí.</h3><p>Explora el catálogo y agrega las referencias que quieras consultar.</p>';
      items.append(empty);
      const link = document.createElement("a");
      link.href = "/catalogo";
      link.className = "btn btn-orange";
      link.textContent = "Explorar catálogo";
      footer.append(link);
      return;
    }
    selection.forEach((id) => {
      const product = byId.get(id);
      const row = document.createElement("div");
      row.className = "drawer-item";
      const image = document.createElement("img");
      image.src = product.image_url;
      image.alt = product.titulo;
      const title = document.createElement("span");
      title.className = "drawer-item-name";
      title.textContent = product.titulo;
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "remove-item";
      remove.textContent = "Quitar";
      remove.setAttribute("aria-label", `Quitar ${product.titulo} de mi selección`);
      remove.addEventListener("click", () => { selection = selection.filter((item) => item !== id); persist(); });
      row.append(image, title, remove);
      items.append(row);
    });
    const note = document.createElement("p");
    note.textContent = "Tu selección se incluirá en un mensaje de WhatsApp. Podrás editarlo antes de enviarlo.";
    const link = document.createElement("a");
    link.className = "btn btn-orange";
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.href = `https://wa.me/573017357829?text=${encodeURIComponent("Hola, equipo Nutricol Foods. Quisiera solicitar información y una cotización B2B de estos productos:\n\n" + selection.map((id, index) => `${index + 1}. ${byId.get(id).titulo}`).join("\n") + "\n\nMi empresa es: \nEl mercado de destino es: \nGracias.")}`;
    link.innerHTML = 'Solicitar cotización <span class="arrow" aria-hidden="true">↗</span>';
    footer.append(note, link);
  }
  function openDrawer() {
    previousFocus = document.activeElement;
    drawer.classList.add("open");
    drawer.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    panel.focus();
  }
  function closeDrawer() {
    drawer.classList.remove("open");
    drawer.setAttribute("aria-hidden", "true");
    document.body.style.overflow = "";
    if (previousFocus && previousFocus.focus) previousFocus.focus();
  }
  document.querySelectorAll("[data-open-quote]").forEach((button) => button.addEventListener("click", openDrawer));
  document.querySelectorAll("[data-close-quote]").forEach((button) => button.addEventListener("click", closeDrawer));
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
    if (event.key === "Tab" && drawer.classList.contains("open")) {
      const focusable = [...panel.querySelectorAll('a[href],button:not([disabled])')];
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
      else if (document.activeElement === panel) { event.preventDefault(); first.focus(); }
    }
  });
  document.querySelectorAll("[data-add-product]").forEach((button) => button.addEventListener("click", () => {
    const id = button.dataset.addProduct;
    selection = selection.includes(id) ? selection.filter((item) => item !== id) : [...selection, id];
    persist();
  }));
  renderSelection();

  const toggle = document.querySelector(".menu-toggle");
  const nav = document.getElementById("primary-nav");
  toggle.addEventListener("click", () => {
    const open = nav.classList.toggle("open");
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú");
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", "Abrir menú");
  }));

  const filters = document.querySelectorAll("[data-filter]");
  filters.forEach((filter) => filter.addEventListener("click", () => {
    filters.forEach((button) => { button.classList.remove("active"); button.setAttribute("aria-pressed", "false"); });
    filter.classList.add("active");
    filter.setAttribute("aria-pressed", "true");
    let visible = 0;
    document.querySelectorAll("#catalog-grid .product-card").forEach((card) => {
      const show = filter.dataset.filter === "Todos" || card.dataset.category === filter.dataset.filter;
      card.hidden = !show;
      if (show) visible += 1;
    });
    document.getElementById("catalog-count").textContent = `${visible} ${visible === 1 ? "producto" : "productos"}`;
  }));

  const form = document.getElementById("contact-form");
  if (form) form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const message = `Hola, equipo Nutricol Foods. Quisiera conversar sobre una oportunidad comercial.\n\nNombre: ${data.get("name")}\nEmpresa: ${data.get("company")}\nCorreo: ${data.get("email")}\nTipo de negocio: ${data.get("type")}\n\nMi consulta: ${data.get("message")}`;
    const url = `https://wa.me/573017357829?text=${encodeURIComponent(message)}`;
    const opened = window.open(url, "_blank", "noopener,noreferrer");
    if (!opened) window.location.href = url;
  });
  if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("visible"); observer.unobserve(entry.target); } });
    }, { threshold: .08 });
    document.querySelectorAll(".reveal").forEach((element) => observer.observe(element));
  } else {
    document.querySelectorAll(".reveal").forEach((element) => element.classList.add("visible"));
  }
})();