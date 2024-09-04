document.addEventListener("DOMContentLoaded", function () {
  const addPizzaBtn = document.getElementById("addPizzaBtn");
  const pizzaSelect = document.getElementById("pizzaSelect");
  const orderSummary = document.getElementById("orderSummary");
  const totalPriceElem = document.getElementById("totalPrice");
  const deliveryFeeElem = document.getElementById("deliveryFee");
  const orderTypeSelect = document.getElementById("orderType");
  let totalPrice = 0.0;
  let deliveryFee = 0.0;

  function updateTotalPrice() {
    let finalPrice = totalPrice + deliveryFee;
    totalPriceElem.textContent = finalPrice.toFixed(2);
  }

  function removePizza(li, pizzaPrice) {
    orderSummary.removeChild(li);
    totalPrice -= pizzaPrice;
    updateTotalPrice();
  }

  addPizzaBtn.addEventListener("click", function () {
    const selectedOption = pizzaSelect.options[pizzaSelect.selectedIndex];
    const pizzaId = selectedOption.value;
    const pizzaText = selectedOption.text;

    if (!pizzaId) {
      alert("Please select a pizza.");
      return;
    }

    // Add pizza to the order summary
    const li = document.createElement("li");
    li.className =
      "list-group-item d-flex justify-content-between align-items-center";

    const pizzaInfo = document.createElement("div");
    pizzaInfo.textContent = pizzaText;

    const removeBtn = document.createElement("button");
    removeBtn.className = "btn btn-danger btn-sm";
    removeBtn.textContent = "Remove";

    // Add a hidden input to the form to keep track of the pizza IDs
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = "pizzas[]";
    input.value = pizzaId;

    let pizzaPrice = 0.0;
    if (pizzaText.includes("Small")) {
      pizzaPrice = 10.0;
    } else if (pizzaText.includes("Medium")) {
      pizzaPrice = 14.0;
    } else if (pizzaText.includes("Large")) {
      pizzaPrice = 18.0;
    }
    totalPrice += pizzaPrice;

    removeBtn.addEventListener("click", function () {
      removePizza(li, pizzaPrice);
    });

    li.appendChild(pizzaInfo);
    li.appendChild(removeBtn);
    li.appendChild(input);
    orderSummary.appendChild(li);

    updateTotalPrice();

    // Reset the pizza select
    pizzaSelect.selectedIndex = 0;
  });

  orderTypeSelect.addEventListener("change", function () {
    if (orderTypeSelect.value === "delivery") {
      deliveryFee = 4.99;
    } else {
      deliveryFee = 0.0;
    }
    deliveryFeeElem.textContent = deliveryFee.toFixed(2);
    updateTotalPrice();
  });
});
