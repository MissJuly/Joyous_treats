// show search bar when search icon is clicked
$(document).ready(function() {
  $('#search-icon').click(function() {
    $('#search-overlay').toggle();
    $('#search-input').focus();
  });

$('#search-form').submit(function(event) {
  event.preventDefault();

  var searchTerm = $('#search-input').val();
  performSearch(searchTerm);
  });
});


// show drop down menu when clicked
function myFunction() {
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
