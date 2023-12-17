$(document).ready(function () {
  $(".atc").on("click", function () {
    var item_id = this.id.toString();
    addToCart(item_id);
  });

  const addToCart = async (product_id) => {
    const addtocart_btn = document.getElementsByClassName("atc");
    const token = localStorage.getItem("authToken");
    try {
      const response = await fetch("/addtocart/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
        body: JSON.stringify({
          quantity: 1,
          product_id: product_id,
        }),
      });

      if (response.ok) {
        console.log("Product added to cart:");
        getCart();
      } else {
        console.error("Failed to add product to cart");
      }
    } catch (error) {
      console.error("Error adding product to cart:", error);
    }
  };

  const getCart = async () => {
    let cart_products, cart_quantity, cart_total;
    const token = localStorage.getItem("authToken");
    try {
      const response = await fetch("/getcart/", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Token ${token}`,
        },
      });

      if (response.ok) {
        const responseData = await response.json();
        cart_products = responseData.data.attributes.cart_products;
        cart_quantity = responseData.data.attributes.quantity;

        cart_total = responseData.data.attributes.total;
        console.log(cart_quantity, "______", cart_total);
        await setCart(cart_products, cart_quantity, cart_total);
      } else {
        console.error("Faild to get user Cart");
      }
    } catch (error) {
      console.error("Error getting user cart ", error);
    }
  };

setCart = (cart_products, cart_quantity, cart_total) => {
    $("#cart").text(`Cart(${cart_quantity})`);
    var cartString = "<h5> This is your cart </h5>";
    var cnt = 1;
    cart_products.forEach((element) => {
      cartString +=
        cnt +
        " : " +
        element.product_title +
        "  Qty:" +
        element.quantity +
        "<br>";
      cnt += 1;
    });
    cartString +=
      ' <br> <a href="checkout" class="btn btn-success" id="checkout">Checkout</a> ';
    cartString += ` <br> <h4> Total : ${cart_total} `;
    document.getElementById("cart").setAttribute("data-content", cartString);
    $('[data-toggle="popover"]').popover();
  };
  if (localStorage.getItem("authToken")) {
    getCart();
  }
});

// python manage.py runserver
