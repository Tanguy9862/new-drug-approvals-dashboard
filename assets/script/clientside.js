document.addEventListener('mousemove', function(e) {
    if (window.dash_clientside) {
        window.dash_clientside.mouse = {
            x: e.clientX,
            y: e.clientY
        };
    }
});

// Ensure the dash_clientside namespace exists
if (!window.dash_clientside) {
    window.dash_clientside = {};
}

// Define functions within the dash_clientside namespace
window.dash_clientside.clientside = {
    update_mouse_position: function() {
        // Return the mouse position stored earlier
        return window.dash_clientside.mouse || {};
    }
};