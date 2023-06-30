// shows search bar when search icon is clicked
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

// function performSearch(searchTerm) {
//   fetch('/search?q=' + searchTerm)
//     .then(function(response) {
//       return response.json();
//     })
//     .then(function(data) {
//       displaySearchResults(data);
//     })
//     .catch(function(error) {
//       console.log('An error occurred: ' + error);
//     });
// }

// function displaySearchResults(results) {
//   var searchResultsDiv = document.getElementById('search-results');
//   searchResultsDiv.innerHTML = '';

//   for (var i = 0; i < results.length; i++) {
//     var result = results[i];
//     var resultItem = document.createElement('div');
//     resultItem.textContent = result.title;
//     searchResultsDiv.appendChild(resultItem);
//   }
// }








//adds title overlay effect on images with mouse movement

function moveOverlay(event) {
  var container = event.currentTarget;
  var overlay = container.querySelector(".overlay");
  var containerRect = container.getBoundingClientRect();
  var x = event.clientX - containerRect.left;
  var y = event.clientY - containerRect.top;
  overlay.style.transform = `translate(${x}px, ${y}px)`;
}
