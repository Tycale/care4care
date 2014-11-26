$(document).ready(function(){
  $('#add_favorite_link').click(function () {
    if ($('#is_favorite_star').hasClass("glyphicon-star-empty")){
      var url = "/accounts/api/member_favorite/"+$("#user_id").val()+"/";
      add_favorite(url);
    }else{
      var url = "/accounts/api/member_favorite/"+$("#user_id").val()+"/";
      remove_favorite(url);
    }
  });

  $('.remove_favorite_link').click(function (event) {
    event.preventDefault();
    var url = $(this).attr("href");
    remove_favorite(url);
  });

function remove_favorite(url_param) {
    $.ajax({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken",  $.cookie('csrftoken'));
      },
      type: "DELETE",
      dataType: "json",
      url: url_param,
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

function add_favorite(url_param) {
  $.ajax({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken",  $.cookie('csrftoken'));
    },
    type: "PUT",
    dataType: "json",
    url: url_param,
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
}

});
