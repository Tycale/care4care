var remove_success = function(){
  $("#is_favorite_star").addClass("glyphicon-star-empty");
  $("#is_favorite_star").removeClass("glyphicon-star");
}

var add_success = function(){
  $("#is_favorite_star").removeClass("glyphicon-star-empty");
  $("#is_favorite_star").addClass("glyphicon-star");
}

var remove_from_list_success = function(id_remove){
 $("#delete_" + id_remove).remove();
}

$(document).ready(function(){
  $('#add_favorite_link').click(function () {
    if ($('#is_favorite_star').hasClass("glyphicon-star-empty")){
      add_favorite($("#user_id").val(),add_success);
    }else{
      remove_favorite($("#user_id").val(), remove_success);
    }
  });

  $('.remove_favorite_link').click(function (event) {
    event.preventDefault();
    remove_favorite($(this).attr("href"), remove_from_list_success);
  });
});

var manage_favorite_url = "/accounts/api/member_favorite/";
var manage_network_url =  "/accounts/api/member_personal_network/";

function remove_favorite(user_id, success_function) {
  remove(manage_favorite_url,user_id,success_function)
}

function add_favorite(user_id, success_function) {
  add(manage_favorite_url,user_id,success_function)
}

function remove_network(user_id, success_function) {
  remove(manage_network_url,user_id,success_function)
}

function add_network(user_id, success_function) {
  add(manage_network_url,user_id,success_function)
}


function remove(url_base,user_id, success_function) {
    url_param = url_base + user_id +"/"
    $.ajax({
      beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken",  $.cookie('csrftoken'));
      },
      type: "DELETE",
      dataType: "json",
      url: url_param,
      success: function(r) {
        if (r){
          success_function(user_id)
        }
      },
      error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
}

function add(url_base,user_id, success_function) {
  url_param = url_base + user_id +"/"
  $.ajax({
    beforeSend: function(xhr, settings) {
      xhr.setRequestHeader("X-CSRFToken",  $.cookie('csrftoken'));
    },
    type: "PUT",
    dataType: "json",
    url: url_param,
    success: function(r) {
      if (r){
       success_function()
      }
    },
    error : function(xhr,errmsg,err) {
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}
