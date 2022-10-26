$("form[name=signup-form").submit(function(e) {
    let $form = $(this);
    let $error = $form.find(".error");
    let data = $form.serialize()

    $.ajax({
        url: '/signup',
        type: 'POST',
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp)
            window.location.href = '/dashboard'
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});

$("form[name=login-form").submit(function(e) {
    let $form = $(this);
    let $error = $form.find(".error");
    let data = $form.serialize()

    $.ajax({
        url: '/login',
        type: 'POST',
        data: data,
        dataType: "json",
        success: function(resp) {
            console.log(resp)
            window.location.href = '/dashboard'
        },
        error: function(resp){
            console.log(resp);
            $error.text(resp.responseJSON.error).removeClass("error--hidden");
        }
    });
    e.preventDefault();
});