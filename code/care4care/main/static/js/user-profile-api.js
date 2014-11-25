$(document).ready(function(){
  $('#add_favorite_link').click(function () {
    if ($('#is_favorite_star').hasClass("glyphicon-star-empty")){
      $.ajax({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken",  $.cookie('csrftoken'));
        },
        type: "PUT",
        dataType: "json",
        url: "/accounts/api/member_favorite/"+$("#user_id").val()+"/",
        success: function(r) {
          if (r){
            $("#is_favorite_star").removeClass("glyphicon-star-empty");
            $("#is_favorite_star").addClass("glyphicon-star");
          }
        },
        error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
      });
    }else{
      $.ajax({
        beforeSend: function(xhr, settings) {
          xhr.setRequestHeader("X-CSRFToken",  $.cookie('csrftoken'));
        },
        type: "DELETE",
        dataType: "json",
        url: "/accounts/api/member_favorite/"+$("#user_id").val()+"/",
        success: function(r) {
          if (r){
            $("#is_favorite_star").addClass("glyphicon-star-empty");
            $("#is_favorite_star").removeClass("glyphicon-star");
          }
        },
        error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
      });
    }


  });
});
