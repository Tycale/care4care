$ ->
    # Care4Care data charts

    # Registrated users
    create_chart("/statistics/registrated_users_json", "global_registration", "Line")


    # TODO: How Users Discovered Care4Care


    # Account types
    create_chart("/statistics/account_types_json", "account_types", "Doughnut")


    # Evolution of users status (active, on holiday, deactivated)
    # in regard of time
    create_chart("/statistics/users_status_json", "users_status_canvas", "Doughnut")


    # Most done job categories
    create_chart("/statistics/job_categories_json", "job_categories", "Radar")

