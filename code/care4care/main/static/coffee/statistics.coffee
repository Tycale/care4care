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




    # Tests graphs
    ###
    data =
        labels: [
            "January"
            "February"
            "March"
            "April"
            "May"
            "June"
            "July"
        ]
        datasets: [
            {
                label: "My First dataset"
                fillColor: "rgba(220,220,220,0.2)"
                strokeColor: "rgba(220,220,220,1)"
                pointColor: "rgba(220,220,220,1)"
                pointStrokeColor: "#fff"
                pointHighlightFill: "#fff"
                pointHighlightStroke: "rgba(220,220,220,1)"
                data: [
                    65
                    59
                    80
                    81
                    56
                    55
                    40
                ]
            }
            {
                label: "My Second dataset"
                fillColor: "rgba(151,187,205,0.2)"
                strokeColor: "rgba(151,187,205,1)"
                pointColor: "rgba(151,187,205,1)"
                pointStrokeColor: "#fff"
                pointHighlightFill: "#fff"
                pointHighlightStroke: "rgba(151,187,205,1)"
                data: [
                    28
                    48
                    40
                    19
                    86
                    27
                    90
                ]
            }
        ]


    # First graph
    c_line = document.getElementById("chart_line").getContext("2d")
    line_chart = new Chart(c_line).Line(data)

    # Second graph
    c_radar = document.getElementById("chart_radar").getContext("2d")
    radar_chart = new Chart(c_radar).Radar(data)

    # Third graph
    polar_data = [
        {
            value: 300
            color: "#F7464A"
            highlight: "#FF5A5E"
            label: "Red"
        }
        {
            value: 50
            color: "#46BFBD"
            highlight: "#5AD3D1"
            label: "Green"
        }
        {
            value: 100
            color: "#FDB45C"
            highlight: "#FFC870"
            label: "Yellow"
        }
        {
            value: 40
            color: "#949FB1"
            highlight: "#A8B3C5"
            label: "Grey"
        }
        {
            value: 120
            color: "#4D5360"
            highlight: "#616774"
            label: "Dark Grey"
        }
    ]
    c_polar = document.getElementById("chart_polar").getContext("2d")
    polar_chart = new Chart(c_polar).PolarArea(polar_data)
    ###
