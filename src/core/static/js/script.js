// Get the pop-up container
var popupContainer = document.getElementById('popup-container');

// Get all close buttons
var closeButtons = document.getElementsByClassName('close-btn');

// Function to show the pop-up
function showPopup() {
    popupContainer.style.display = 'block';
}

// Function to hide the pop-up
function hidePopup() {
    popupContainer.style.display = 'none';
}

// Attach click event listener to each close button
for (var i = 0; i < closeButtons.length; i++) {
    closeButtons[i].addEventListener('click', function () {
        // Find the parent element (message) and remove it
        var message = this.parentNode;
        message.parentNode.removeChild(message);

        // Hide the pop-up if there are no more messages
        if (document.getElementsByClassName('message').length === 0) {
            hidePopup();
        }
    });
}

// Show the pop-up if there are messages
if (document.getElementsByClassName('message').length > 0) {
    showPopup();
}

// show search bar when search icon is clicked
$(document).ready(function() {
  $('#search-icon').click(function() {
    $('#search-overlay').toggle();
    $('#search-input').focus();
  });
});


// show drop down menu when account is clicked
function accountFunction() {
  document.getElementById('myDropdown').classList.toggle('show');
}

// Close the dropdown when clicked outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}

document.addEventListener("mousemove", function (event) {
  if (event.target.classList.contains("image")) {
    moveOverlay(event);
  }
});



//add title overlay effect on images with mouse movement
function moveOverlay(event) {
  var container = event.currentTarget;
  var overlay = container.querySelector(".overlay");
  var containerRect = container.getBoundingClientRect();
  var x = event.clientX - containerRect.left;
  var y = event.clientY - containerRect.top;
  overlay.style.transform = `translate(${x}px, ${y}px)`;
}



// Function to show the cart pop-up
function showCart() {
    updateCart();
    var cartPopup = document.getElementById('cart-popup');
    cartPopup.style.display = 'block';
}

// Function to hide the cart pop-up
function hideCart() {
    var cartPopup = document.getElementById('cart-popup');
    cartPopup.style.display = 'none';
}

// Function to add an item to the cart
function addToCart(itemId) {
  var quantity = parseInt(document.getElementById('quantity' + itemId).value);
  var data = { 'name': 'Product ' + itemId, 'quantity': quantity };

  $.ajax({
      url: '/cart/add',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
          alert(response.message);
          updateCart();
      }
  });
}

// Function to remove an item from the cart
function removeFromCart(itemId) {
  var data = { 'item_id': itemId };

  $.ajax({
      url: '/cart/remove',
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(data),
      success: function(response) {
          alert(response.message);
          updateCart();
      }
  });
}

// Function to update the cart display
function updateCart() {
  $.ajax({
      url: '/cart',
      type: 'GET',
      success: function(response) {
          var cartItems = response;

          // Clear the cart display
          var cartItemsElement = document.getElementById('cart-items');
          cartItemsElement.innerHTML = '';

          // Update the cart display with the retrieved cart items
          cartItems.forEach(function(item) {
              var li = document.createElement('li');
              var itemText = document.createTextNode(item.name + ' (Quantity: ' + item.quantity + ')');
              li.appendChild(itemText);

              var removeButton = document.createElement('button');
              removeButton.innerHTML = 'Remove';
              removeButton.onclick = function() {
                  removeFromCart(item.id);
              };
              li.appendChild(removeButton);

              cartItemsElement.appendChild(li);
          });

          // Calculate and display the total
          var total = calculateTotal(cartItems);
          var totalElement = document.getElementById('total');
          totalElement.innerHTML = 'Total: $' + total.toFixed(2);
      }
  });
}

// Function to calculate the total of cart items
function calculateTotal(cartItems) {
  var total = 0;
  cartItems.forEach(function(item) {
      // Perform calculation based on item price and quantity
      // Modify this calculation based on your specific requirements
      total += item.price * item.quantity;
  });
  return total;
}
