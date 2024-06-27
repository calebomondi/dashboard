//Handles Message Visibility
function showHidden() {
    var hidden = document.getElementById('message');
    hidden.style.visibility = 'visible';
}

//AJAX
$(document).ready(function () {
    //post All
    $('#postFormAll').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postAll,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormAll')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post FB
    $('#postFormFb').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postFb,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormFb')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //post IG
    $('#postFormIg').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: postIg,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormIg')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Post.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
    //setup
    $('#postFormSet').on('submit', function (e) {
        e.preventDefault(); // Prevent the default form submission

        var formData = new FormData(this);

        $.ajax({
            url: setupUrl,
            type: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                $('#message').text(response.message); // Display the response message
                $('#postFormSet')[0].reset();
            },
            error: function () {
                $('#message').text('Could Not Sumbit.Please Try Again Later!.'); // Display error message if AJAX request fails
            }
        });
    });
});

//Which Site Is ACtive
function fbDash(id) {
    var fb = document.getElementById('fbSite');
    var ig = document.getElementById('igSite');
    var set = document.getElementById('setSite');
    var all = document.getElementById('allSite');

    if(id == 0) {
        //FB
        ig.style.borderLeft = 'none';
        set.style.borderLeft = 'none';
        all.style.borderLeft = 'none';
        fb.style.borderLeft = '3px solid var(--white)';
    } else if (id == 1){
        //IG
        ig.style.borderLeft = '3px solid var(--white)';
        fb.style.borderLeft = 'none';
        set.style.borderLeft = 'none';
        all.style.borderLeft = 'none';
    } else if (id == 2){
        //SET
        set.style.borderLeft = '3px solid var(--white)';
        fb.style.borderLeft = 'none';
        ig.style.borderLeft = 'none';
        all.style.borderLeft = 'none';
    } else if (id == 3){
        //All
        set.style.borderLeft = 'none';
        fb.style.borderLeft = 'none';
        ig.style.borderLeft = 'none';
        all.style.borderLeft = '3px solid var(--white)';
    } else {
        fb.style.borderLeft = 'none';
        ig.style.borderLeft = 'none';
        set.style.borderLeft = 'none';
        all.style.borderLeft = 'none';
    }
}
document.getElementById('fbDash').addEventListener('click', () => {fbDash(0)});
document.getElementById('igDash').addEventListener('click', () => {fbDash(1)});
document.getElementById('setDash').addEventListener('click', () => {fbDash(2)});
document.getElementById('allDash').addEventListener('click', () => {fbDash(3)});

function getPath() {
    var currentPath = window.location.pathname;
    var pathSegments = currentPath.split('/');
    if (pathSegments[1] == 'facebook')
        fbDash(0);
    else if(pathSegments[1] == 'instagram')
        fbDash(1);
    else if(pathSegments[1] == 'setup')
        fbDash(2);
    else if(pathSegments[1] == 'all')
        fbDash(3);
    else
        fbDash(4)
}
//onload
getPath()
//on path change
window.addEventListener('popstate', getPath);