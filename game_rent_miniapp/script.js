const tg = window.Telegram.WebApp;
tg.expand(); // разворачиваем Mini App на весь экран [web:108]

const API_URL = "https://itchy-impalas-peel.loca.lt"; // пока локально

const itemsContainer = document.getElementById("itemsContainer");
const modelInput = document.getElementById("modelFilter");
const filterBtn = document.getElementById("filterBtn");

let cart = [];

const cartCountEl = document.getElementById("cartCount");
const checkoutBtn = document.getElementById("checkoutBtn");
const orderForm = document.getElementById("orderForm");
const orderFormContainer = document.getElementById("orderFormContainer");
const cartItemsView = document.getElementById("cartItemsView");

function addToCart(itemId) {
  const existing = cart.find(c => c.id === itemId);
  if (existing) {
    existing.count += 1;
  } else {
    cart.push({ id: itemId, count: 1 });
  }
  updateCartUI();
}

function changeCartItem(id, delta) {
  const item = cart.find(c => c.id === id);
  if (!item) return;
  item.count += delta;
  if (item.count <= 0) {
    cart = cart.filter(c => c.id !== id);
  }
  updateCartUI();
}

function removeFromCart(id) {
  cart = cart.filter(c => c.id !== id);
  updateCartUI();
}

function updateCartUI() {
  const totalCount = cart.reduce((sum, item) => sum + item.count, 0);
  cartCountEl.textContent = totalCount;
  checkoutBtn.disabled = totalCount === 0;

  // если форма открыта — перерисуем список позиций
  renderCartItemsView();
}

function updateCartUI() {
  const totalCount = cart.reduce((sum, item) => sum + item.count, 0);
  cartCountEl.textContent = totalCount;
  checkoutBtn.disabled = totalCount === 0;

  // если форма открыта — перерисуем список позиций
  renderCartItemsView();
}

function renderCartItemsView() {
  if (!cartItemsView) return;

  if (cart.length === 0) {
    cartItemsView.innerHTML = "<div class='cart-empty'>Корзина пуста</div>";
    return;
  }

  cartItemsView.innerHTML = "";
  cart.forEach(item => {
    const row = document.createElement("div");
    row.className = "cart-item-row";
    row.innerHTML = `
      <span class="cart-item-title">ID ${item.id}</span>
      <div class="cart-item-controls">
        <button class="qty-btn" data-id="${item.id}" data-delta="-1">−</button>
        <span class="cart-item-qty">${item.count}</span>
        <button class="qty-btn" data-id="${item.id}" data-delta="1">+</button>
        <button class="remove-btn" data-id="${item.id}">✕</button>
      </div>
    `;
    cartItemsView.appendChild(row);
  });

  // обработчики + / − / удалить
  cartItemsView.querySelectorAll(".qty-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = Number(btn.dataset.id);
      const delta = Number(btn.dataset.delta);
      changeCartItem(id, delta);
    });
  });

  cartItemsView.querySelectorAll(".remove-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const id = Number(btn.dataset.id);
      removeFromCart(id);
    });
  });
}

checkoutBtn.addEventListener("click", () => {
  if (cart.length === 0) return;
  orderFormContainer.style.display = "block";
  renderCartItemsView();
});
  
checkoutBtn.addEventListener("click", () => {
  if (cart.length === 0) return;
  orderFormContainer.style.display = "block";
});

async function loadItems(model) {
  itemsContainer.innerHTML = "Загрузка...";

  const params = new URLSearchParams();
  if (model) params.append("model", model);
  params.append("only_available", "true");

  try {
    const res = await fetch(`${API_URL}/items?${params.toString()}`);
    const data = await res.json();

    if (!Array.isArray(data) || data.length === 0) {
      itemsContainer.innerHTML = "Нет доступного оборудования.";
      return;
    }

    itemsContainer.innerHTML = "";
    data.forEach(item => {
      const div = document.createElement("div");
      div.className = "item-card";
div.innerHTML = `
  <div class="item-title">${item.model}</div>
  <div class="item-meta">
    ${item.params || ""}<br/>
    В наличии: ${item.available_count} шт<br/>
    Цена: ${item.price_per_day} ₽/день
  </div>
  <button class="add-btn" data-id="${item.id}">+ В корзину</button>
`;
      itemsContainer.appendChild(div);
    });
    itemsContainer.querySelectorAll(".add-btn").forEach(btn => {
  btn.addEventListener("click", () => {
    const id = Number(btn.dataset.id);
    addToCart(id);
  });
});
  } catch (e) {
    console.error(e);
    itemsContainer.innerHTML = "Ошибка загрузки каталога.";
  }
}

filterBtn.addEventListener("click", () => {
  loadItems(modelInput.value.trim());
});

orderForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (cart.length === 0) return;

  const formData = new FormData(orderForm);

  const payload = {
    user_id: tg.initDataUnsafe?.user?.id || 0,
    user_name: tg.initDataUnsafe?.user?.username || "",
    phone: formData.get("phone"),
    email: formData.get("email"),
    delivery_address: formData.get("address") || "",
    items: cart.map(c => ({ id: c.id, count: c.count }))
  };

  try {
    const res = await fetch(`${API_URL}/orders`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || `Ошибка API: ${res.status}`);
    }
    const data = await res.json();
    tg.showAlert(`Заказ #${data.id} создан! Статус: ${data.status}`);
    cart = [];
    updateCartUI();
    orderForm.reset();
    orderFormContainer.style.display = "none";
  } catch (err) {
    console.error(err);
    tg.showAlert("Не удалось оформить заказ. Попробуйте позже.");
  }
});


// первый загруз
loadItems();
