(function() {
  $(function() {
    create_chart("/statistics/registrated_users_json", "global_registration", "Line");
    create_chart("/statistics/account_types_json", "account_types", "Doughnut");
    create_chart("/statistics/users_status_json", "users_status_canvas", "Doughnut");
    return create_chart("/statistics/job_categories_json", "job_categories", "Radar");
  });

}).call(this);
