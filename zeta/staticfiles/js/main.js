$(function() {

    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

function create_user() {
    console.log("creating user")
    $.ajax({
        url : "create_user/", 
        type : "POST", 
        data : { 
            name : $('#registration-form #name').val(), 
            mobile : $('#registration-form #mobile').val() 
        },

        // handle a successful response
        success : function(json) {
            $('#registration-form #name').val('');
            $('#registration-form #mobile').val(''); 
            console.log(json); 
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
        }
    });
};

function change_password() {
    console.log("changing password")
    $.ajax({
        url : "change_password/", 
        type : "POST", 
        data : { 
            userid : $('#password-form #userid').val(), 
            newpass : $('#password-form #newpass').val() 
        },

        // handle a successful response
        success : function(json) {
            $('#password-form #userid').val('');
            $('#password-form #newpass').val(''); 
            console.log(json); 
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
        }
    });
};

function change_pin() {
    console.log("changing pin")
    $.ajax({
        url : "change_pin/", 
        type : "POST", 
        data : { 
            userid : $('#pin-form #userid').val(), 
            newpin : $('#pin-form #newpin').val() 
        },

        // handle a successful response
        success : function(json) {
            $('#pin-form #userid').val('');
            $('#pin-form #newpin').val(''); 
            console.log(json); 
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
        }
    });
};

function lock_user(is_active) {
    console.log("changing user status")
    $.ajax({
        url : "lock/", 
        type : "POST", 
        data : { 
            userid : $('#lock-form #userid').val(),
            is_active : is_active
        },

        // handle a successful response
        success : function(json) {
            $('#lock-form #userid').val('');
            console.log(json); 
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
        }
    });
};

function send_money(is_active) {
    console.log("started transcation")
    $.ajax({
        url : "send_money/", 
        type : "POST", 
        data : { 
            userid : $('#money-form #userid').val(),
            amount : $('#money-form #amount').val()
        },

        // handle a successful response
        success : function(json) {
            $('#money-form #userid').val('');
            $('#money-form #amount').val('');
            console.log(json); 
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
        }
    });
};

function fetch_history(is_active) {
    console.log("started transcation")
    $.ajax({
        url : "history/", 
        type : "GET",
        // handle a successful response
        success : function(json) {
            json.data.forEach(function(item){
                console.log(item);
                var row_item = "<tr class='entry'><td>" + item.user + "</td><td>" + item.amount + "</td><td>" + item.date +"</td><tr>"
                $('#history #transactions').append(row_item);
            });
            // console.log(json); 
            console.log("success");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error");
        }
    });
};

$('#registration-form').submit(function(event){
    event.preventDefault();
    console.log("reg form submitted!");
    create_user();
});

$('#password-form').submit(function(event){
    event.preventDefault();
    console.log("pass form submitted!");
    change_password();
});

$('#pin-form').submit(function(event){
    event.preventDefault();
    console.log("pin form submitted!");
    change_pin();
});

$('#lock-form #lock_button').click(function(event){
    event.preventDefault();
    console.log("user locked!");
    lock_user("false");
});

$('#lock-form #unlock_button').click(function(event){
    event.preventDefault();
    console.log("user unlocked!");
    lock_user("true");
});

$('#money-form').submit(function(event){
    event.preventDefault();
    console.log("transfer started");
    send_money();
});

$("#history").click(function(event){
    event.preventDefault();
    console.log("fetch history");
    $("#history #transactions .entry").remove()
    fetch_history();
});