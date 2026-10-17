(() => {
  "use strict";
  const products = JSON.parse(document.getElementById("products-data").textContent);
  const isEnglish = document.documentElement.lang === "en";
  const tr = (spanish, english) => isEnglish ? english : spanish;
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
      button.innerHTML = added ? tr("Agregado", "Added") + ' <span aria-hidden="true">✓</span>' : tr("Agregar", "Add") + ' <span aria-hidden="true">＋</span>';
      button.setAttribute("aria-pressed", String(added));
    });
    items.replaceChildren();
    footer.replaceChildren();
    if (!selection.length) {
      const empty = document.createElement("div");
      empty.className = "drawer-empty";
      empty.innerHTML = '<span class="empty-mark" aria-hidden="true">∅</span><h3>' + tr("Aún no hay productos aquí.", "No products selected yet.") + '</h3><p>' + tr("Explora el catálogo y agrega las referencias que quieras consultar.", "Explore the catalog and add products you would like to ask about.") + '</p>';
      items.append(empty);
      const link = document.createElement("a");
      link.href = "/catalogo";
      link.className = "btn btn-orange";
      link.textContent = tr("Explorar catálogo", "Explore catalog");
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
      remove.textContent = tr("Quitar", "Remove");
      remove.setAttribute("aria-label", tr(`Quitar ${product.titulo} de mi selección`, `Remove ${product.titulo} from my selection`));
      remove.addEventListener("click", () => { selection = selection.filter((item) => item !== id); persist(); });
      row.append(image, title, remove);
      items.append(row);
    });
    const note = document.createElement("p");
    note.textContent = tr("Tu selección se incluirá en un mensaje de WhatsApp. Podrás editarlo antes de enviarlo.", "Your selection will be included in a WhatsApp message. You can review it before sending.");
    const link = document.createElement("a");
    link.className = "btn btn-orange";
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    const quoteIntro = tr("Hola, equipo Nutricol Foods. Quisiera solicitar información y una cotización B2B de estos productos:", "Hello, Nutricol Foods team. I would like information and a B2B quote for these products:");
    const companyPrompt = tr("Mi empresa es:", "My company is:");
    const marketPrompt = tr("El mercado de destino es:", "The destination market is:");
    const thanks = tr("Gracias.", "Thank you.");
    link.href = `https://wa.me/573246331156?text=${encodeURIComponent(quoteIntro + "\n\n" + selection.map((id, index) => `${index + 1}. ${byId.get(id).titulo}`).join("\n") + `\n\n${companyPrompt} \n${marketPrompt} \n${thanks}`)}`;
    link.innerHTML = tr("Solicitar cotización", "Request a quote") + ' <span class="arrow" aria-hidden="true">↗</span>';
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
    toggle.setAttribute("aria-label", open ? tr("Cerrar menú", "Close menu") : tr("Abrir menú", "Open menu"));
  });
  nav.querySelectorAll("a").forEach((link) => link.addEventListener("click", () => {
    nav.classList.remove("open");
    toggle.setAttribute("aria-expanded", "false");
    toggle.setAttribute("aria-label", tr("Abrir menú", "Open menu"));
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
    document.getElementById("catalog-count").textContent = `${visible} ${visible === 1 ? tr("producto", "product") : tr("productos", "products")}`;
  }));

  const form = document.getElementById("contact-form");
  if (form) form.addEventListener("submit", (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;
    const data = new FormData(form);
    const message = `${tr("Hola, equipo Nutricol Foods. Quisiera conversar sobre una oportunidad comercial.", "Hello, Nutricol Foods team. I would like to discuss a business opportunity.")}\n\n${tr("Nombre", "Name")}: ${data.get("name")}\n${tr("Empresa", "Company")}: ${data.get("company")}\n${tr("Correo", "Email")}: ${data.get("email")}\n${tr("Tipo de negocio", "Business type")}: ${data.get("type")}\n\n${tr("Mi consulta", "My inquiry")}: ${data.get("message")}`;
    const url = `https://wa.me/573246331156?text=${encodeURIComponent(message)}`;
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