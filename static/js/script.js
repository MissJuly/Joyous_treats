// Get references to the animated image elements
var image1 = document.getElementById('image1');
var image2 = document.getElementById('image2');

// Register event listener for cursor movement
document.addEventListener('mousemove', handleMouseMove);

// Function to handle cursor movement
function handleMouseMove(event) {
    // Get cursor coordinates
    var mouseX = event.clientX;
    var mouseY = event.clientY;

    // Update image positions based on cursor movement
    image1.style = mouseX + 'px';
    image1.style = mouseY + 'px';
    image2.style = -mouseX + 'px';
    image2.style = -mouseY + 'px';
}
