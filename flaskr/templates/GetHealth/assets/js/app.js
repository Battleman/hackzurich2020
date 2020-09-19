$(function() {
    // Read Profile Info
    $.getJSON("./dataset/user.json", function(data) {
        console.log(JSON.stringify(data));
        $('#username').text(data.username);
        $('#profession').text(data.profession);
        $('#email').text(data.email);
    }).fail(function() {
        console.log("An error has occurred.");
    });

    // Sidebar toggle behavior
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar, #content').toggleClass('active');
        if ($('#sidebar').hasClass('active')) {
            $('#toggleText').text("Show NavBar");
        } else {
            $('#toggleText').text("Hide NavBar");
        }
    });


});