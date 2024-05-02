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
        return window.dash_clientside.mouse || {};
    },

    toggle_modal_data_source: function(n_clicks, opened) {
            if(n_clicks === undefined) {
                return window.dash_clientside.no_update;
            }
            return !opened;
    }
};