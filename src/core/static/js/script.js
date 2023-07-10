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


//add title overlay effect on images with mouse movement
function moveOverlay(event) {
  var container = event.currentTarget;
  var overlay = container.querySelector(".overlay");
  var containerRect = container.getBoundingClientRect();
  var x = event.clientX - containerRect.left;
  var y = event.clientY - containerRect.top;
  overlay.style.transform = `translate(${x}px, ${y}px)`;
}

document.addEventListener("mousemove", function (event) {
  if (event.target.classList.contains("image")) {
    moveOverlay(event);
  }
});


// Get the modal
var modal = document.getElementById("cartPopup");

// Get the button that opens the modal
var btn = document.getElementById("cartBtn");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}
