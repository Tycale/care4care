$ ->
    get2dContext = (id) ->
        document.getElementById(id).getContext("2d")


    # Create a chart
    create_chart = (url_json, canvas_id, chart_type) ->
        $.ajax(url_json,
            dataType: "json"
            success: (json_data) ->
                context = get2dContext(canvas_id)
                draw_chart_type(context, json_data, chart_type)
            error: (err) ->
                console.log("Could not load: "+url_json)
        )


    draw_chart_type = (context, data, chart_type) ->
        chart = new Chart(context)
        switch chart_type
            when "Line"
                chart.Line(data)
            when "Doughnut"
                chart.Doughnut(data)
            when "Radar"
                chart.Radar(data)


    # Care4Care data charts

    # Registrated users
    create_chart("/statistics/registrated_users_json", "global_registration", "Line")


    # TODO: How Users Discovered Care4Care


    # Account types
    create_chart("/statistics/account_types_json", "account_types", "Doughnut")


    # Evolution of users status (active, on holiday, deactivated)
    # in regard of time
    create_chart("/statistics/users_status_json", "users_status_canvas", "Line")


    # Most done job categories
    create_chart("/statistics/job_categories_json", "job_categories", "Radar")

