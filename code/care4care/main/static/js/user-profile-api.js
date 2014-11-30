var manage_favorite_url = "/accounts/api/member_favorite/";
var manage_network_url =  "/accounts/api/member_personal_network/";
var manage_ignored_url = "/accounts/api/ignore_list/";

function remove_favorite(user_id, success_function, failed_function) {
  remove(manage_favorite_url,user_id,success_function, failed_function)
}

function add_favorite(user_id, success_function, failed_function) {
  add(manage_favorite_url,user_id,success_function, failed_function)
}

function remove_network(user_id, success_function, failed_function) {
  remove(manage_network_url,user_id,success_function, failed_function)
}

function add_network(user_id, success_function, failed_function) {
  add(manage_network_url,user_id,success_function, failed_function)
}

function add_ignored(user_id, success_function, failed_function) {
  add(manage_ignored_url,user_id,success_function, failed_function)
}

function remove_ignored(user_id, success_function, failed_function) {
  remove(manage_ignored_url,user_id,success_function, failed_function)
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
          success_function(r["name"],user_id)
        }
      },
      error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
    });
}

function add(url_base,user_id, success_function, failed_function) {
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
       success_function(r["name"])
      }
    },
    error : function(xhr,errmsg,err) {
      if (xhr.status == 422){
        failed_function()
      }
      console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
  });
}
