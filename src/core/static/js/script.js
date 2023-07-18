// Get the pop-up container for flash messages
var popupContainer = document.getElementById("popup-container");

// Get all close buttons
var closeButtons = document.getElementsByClassName("close-btn");

// Function to show the pop-up
function showPopup() {
  popupContainer.style.display = "block";
}

// Function to hide the pop-up
function hidePopup() {
  popupContainer.style.display = "none";
}

// Attach click event listener to each close button
for (var i = 0; i < closeButtons.length; i++) {
  closeButtons[i].addEventListener("click", function () {
    // Find the parent element (message) and remove it
    var message = this.parentNode;
    message.parentNode.removeChild(message);

    // Hide the pop-up if there are no more messages
    if (document.getElementsByClassName("message").length === 0) {
      hidePopup();
    }
  });
}

// Show the pop-up if there are messages
if (document.getElementsByClassName("message").length > 0) {
  showPopup();
}

// show search bar when search icon is clicked
$(document).ready(function () {
  var searchOverlay = $("#search-overlay");
  var searchModalOverlay = $("#search-modal-overlay");

  $("#search-icon").click(function () {
    searchOverlay.toggleClass("show");
    searchModalOverlay.toggleClass("show");
    $("#search-input").focus();
  });

  searchModalOverlay.click(function () {
    searchOverlay.removeClass("show");
    searchModalOverlay.removeClass("show");
  });
});

// show drop account down menu when account is clicked
function accountFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the account dropdown when clicked outside of it
window.onclick = function (e) {
  if (!e.target.matches(".dropbtn")) {
    var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains("show")) {
      myDropdown.classList.remove("show");
    }
  }
};

// //add title overlay effect on images with mouse movement
document.addEventListener("mousemove", function(event) {
  var target = event.target;
  if (target.classList.contains("image")) {
    moveOverlay(event);
  }
});

function moveOverlay(event) {
  var container = event.currentTarget;
  var overlay = container.querySelector(".overlay");
  var containerRect = container.getBoundingClientRect();
  var x = event.clientX - containerRect.left;
  var y = event.clientY - containerRect.top;
  overlay.style.transform = `translate(${x}px, ${y}px)`;
}

// Add your JavaScript code to handle the modal functionality
// Get all edit links
var editLinks = document.querySelectorAll('.edit-link');

// Function to handle opening a modal
function openModal(event) {
    event.preventDefault();
    var targetModalId = this.getAttribute('data-target');
    var modal = document.querySelector(targetModalId);
    modal.classList.add('show');
}

// Function to handle closing a modal
function closeModal(event) {
    event.preventDefault();
    var modal = this.closest('.modal');
    modal.classList.remove('show');
}

// Add event listeners to open the modals
Array.prototype.forEach.call(editLinks, function(link) {
    link.addEventListener('click', openModal);
});

// Add event listeners to close the modals
var closeButtons = document.querySelectorAll('.modal .close');
Array.prototype.forEach.call(closeButtons, function(button) {
    button.addEventListener('click', closeModal);
});

//  // Close the modal when clicking outside the modal content
//  window.addEventListener('click', function(event) {
//   var modals = document.querySelectorAll('.modal');
//   Array.prototype.forEach.call(modals, function(modal) {
//       if (modal.classList.contains('show') && !modal.contains(event.target)) {
//           modal.classList.remove('show');
//       }
//   });
// });
