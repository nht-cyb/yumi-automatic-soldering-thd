//backup for the good stuff
// Variables to track clicked positions and dragging
let clickedPositions = [];
let isDragging = false;
let dragStart = { x: 0, y: 0 };
let dragEnd = { x: 0, y: 0 };

// Canvas overlay for interactions
const canvas = document.getElementById("perfboard-overlay");
const image = document.getElementById("perfboard-image");
const ctx = canvas.getContext("2d");

// Ensure canvas dimensions match the image
image.onload = () => {
    canvas.width = image.width;
    canvas.height = image.height;
};

// Mouse down: Start drag or register a single click
canvas.addEventListener("mousedown", (event) => {
    const rect = canvas.getBoundingClientRect();
    dragStart.x = event.clientX - rect.left;
    dragStart.y = event.clientY - rect.top;
    isDragging = true;
});

// Mouse up: Finish drag and select points
canvas.addEventListener("mouseup", (event) => {
    if (isDragging) {
        const rect = canvas.getBoundingClientRect();
        dragEnd.x = event.clientX - rect.left;
        dragEnd.y = event.clientY - rect.top;

        // Select points in the dragged area
        selectPointsInDrag(dragStart, dragEnd);
        isDragging = false;
    }
});

// Mouse move: Show drag rectangle (optional for visualization)
canvas.addEventListener("mousemove", (event) => {
    if (isDragging) {
        const rect = canvas.getBoundingClientRect();
        const currentX = event.clientX - rect.left;
        const currentY = event.clientY - rect.top;

        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear previous drawings
        redrawPoints(); // Redraw points
        drawDragRectangle(dragStart.x, dragStart.y, currentX, currentY); // Draw the drag rectangle
    }
});

// Draw a point with the specified color at the given position
function drawPoint(x, y) {
    ctx.beginPath();
    ctx.arc(x, y, 8, 0, 2 * Math.PI);
    ctx.fillStyle = "#FFFF65"; // Updated color
    ctx.fill();
    ctx.closePath();
}

// Redraw all points from the clickedPositions array
function redrawPoints() {
    clickedPositions.forEach((pos) => drawPoint(pos.x, pos.y));
}

// Draw a rectangle for the dragging area
function drawDragRectangle(x1, y1, x2, y2) {
    ctx.beginPath();
    ctx.rect(x1, y1, x2 - x1, y2 - y1);
    ctx.strokeStyle = "#FFFF65";
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.closePath();
}

// Select points within the dragged area
function selectPointsInDrag(start, end) {
    const minX = Math.min(start.x, end.x);
    const maxX = Math.max(start.x, end.x);
    const minY = Math.min(start.y, end.y);
    const maxY = Math.max(start.y, end.y);

    // Add points within the rectangle to clickedPositions
    for (let x = minX; x <= maxX; x += 20.4) { // Adjust step size based on hole spacing
        for (let y = minY; y <= maxY; y += 20.4) {
            clickedPositions.push({ x: Math.round(x), y: Math.round(y) });
            drawPoint(x, y);
        }
    }
}

// Save positions to a .txt file
document.getElementById("save-button").addEventListener("click", () => {
    const positions = clickedPositions.map(pos => `${pos.x} ${pos.y}`).join("\n");
    const blob = new Blob([positions], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "clicked_positions.txt";
    a.click();
    URL.revokeObjectURL(url);
});

// Clear all points and reset the canvas
document.getElementById("clear-button").addEventListener("click", () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    clickedPositions = [];
});

// Undo the last click or drag selection
document.getElementById("undo-button").addEventListener("click", () => {
    if (clickedPositions.length > 0) {
        clickedPositions.pop(); // Remove the last clicked position
        ctx.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
        redrawPoints(); // Redraw remaining points
    }
});
