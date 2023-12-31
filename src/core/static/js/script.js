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
document.addEventListener("mousemove", function (event) {
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
document.addEventListener('DOMContentLoaded', function() {
  // Get all modal elements
  var modals = document.getElementsByClassName('modal');

  // Function to handle opening a modal
  function openModal(modal) {
    modal.style.display = 'block';
  }

  // Function to handle closing a modal
  function closeModal(modal) {
    modal.style.display = 'none';
  }

  // Add event listeners to open and close the modals
  Array.prototype.forEach.call(modals, function(modal) {
    // Get the modal's close button
    var closeBtn = modal.querySelector('.close');

    // Open the modal when the corresponding link is clicked
    var openBtns = document.querySelectorAll('[data-target="#' + modal.id + '"]');
    openBtns.forEach(function(openBtn) {
      openBtn.addEventListener('click', function() {
        openModal(modal);
      });
    });

    // Close the modal when the close button is clicked
    if (closeBtn) {
      closeBtn.addEventListener('click', function() {
        closeModal(modal);
      });
    }

    // Close the modal when clicking outside the modal content
    window.addEventListener('click', function(event) {
      if (event.target === modal) {
        closeModal(modal);
      }
    });

    // Prevent the modal from closing when clicking inside the modal content
    modal.addEventListener('click', function(event) {
      event.stopPropagation();
    });
  });
});
