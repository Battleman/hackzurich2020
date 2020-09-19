$(function() {
    // Read URL Info
    let urlParams = new URLSearchParams(window.location.search);
    let bountyID = urlParams.get('bounty');

    // Get Bounty Info
    $.getJSON("./dataset/bounties.json", function(data) {
        console.log(JSON.stringify(data[bountyID - 1]));
        let bounty = data[bountyID - 1];
        $('#bountyID').text(bounty.id);
        $('#bountyTitle').text(bounty.title);
        $('#bountyReward').text(bounty.rewards);
        $('#bountyDetail').text(bounty.content);
    }).fail(function() {
        console.log("An error has occurred.");
    });

    const constraints = {
        video: true
    };

    const video = document.querySelector('video');

    navigator.mediaDevices.getUserMedia(constraints).
    then((stream) => { video.srcObject = stream });
});