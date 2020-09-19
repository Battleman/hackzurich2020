$(function() {

    // Read User Info to show the bounties
    $.getJSON("./dataset/user.json", function(data) {
        console.log(JSON.stringify(data));
        $('#category').text(data.category);
    }).fail(function() {
        console.log("An error has occurred.");
    });

    // Read User Info to show the bounties
    $.getJSON("./dataset/bounties.json", function(data) {
        console.log(data.length);
        $.each(data, function(key, val) {
            if (val.category === $('#category').text()) {
                let element = "<div class='card'><div class='content'><h2 class='title'>" + val.title + "</h2><p class='copy'>" + val.content + "</p><p class='copy'>" + val.rewards + "</p><a class='card-btn btn' href='./bounty.html?bounty=" + val.id + "'>Claim</a></div></div>";
                $('.page-content').append(element);
            }
        });
    }).fail(function() {
        console.log("An error has occurred.");
    });


});