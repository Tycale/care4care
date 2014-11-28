$ ->
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



    get2dContext = (id) ->
        document.getElementById(id).getContext("2d")


    # Care4Care example data

    # Color constants
    LIGHT_BLUE_RGB = [151, 187, 205]
    GREEN_RGB  = [46, 217, 138]
    ORANGE_RGB = [255, 169, 0]

    get_rgba = (my_rgb, a) ->
        "rgba(#{my_rgb[0]}, #{my_rgb[1]}, #{my_rgb[2]}, #{a})"


    # TODO: TRANSLATIONS !
    users_registration =
        labels: [
            "Avril"
            "Mai"
            "Juin"
            "Juillet"
            "Août"
            "Septembre"
            "Octobre"
        ]
        datasets: [
            fillColor: "rgba(151,187,205,0.2)"
            strokeColor: "rgba(151,187,205,1)"
            pointColor: "rgba(151,187,205,1)"
            pointStrokeColor: "#fff"
            pointHighlightFill: "#fff"
            pointHighlightStroke: "rgba(151,187,205,1)"
            data: [
                10
                15
                22
                33
                48
                69
                99
            ]
        ]
    global_registration = document.getElementById("global_registration").getContext("2d")
    global_users_chart = new Chart(global_registration).Line(users_registration)


    # Account types
    data_account_types = [
        {
            label: "Membres"
            value: 69
            color: "#F7464A"
        }
        {
            label: "Membres vérifiés"
            value: 21
            color: "#FDB45C"
        }
        {
            label: "Non-membres"
            value: 10
            color: "#46BFBD"
        }
    ]
    account_types = get2dContext("account_types")
    account_types_chart = new Chart(account_types).Doughnut(data_account_types)



    # TODO: How Users Discovered Care4Care



    # TODO: Evolution of users status (active, on holiday, deactivated)
    # in regard of time
    data_users_status =
        labels: [
            "Avril"
            "Mai"
            "Juin"
            "Juillet"
            "Août"
            "Septembre"
            "Octobre"
        ]
        datasets: [
            {
                label: "Actifs"
                fillColor: "rgba(151,187,205,0.2)"
                strokeColor: "rgba(151,187,205,1)"
                pointColor: "rgba(151,187,205,1)"
                pointStrokeColor: "#fff"
                pointHighlightFill: "#fff"
                pointHighlightStroke: "rgba(151,187,205,1)"
                data: [
                    10
                    14
                    20
                    28
                    40
                    61
                    87
                ]
            }
            {
                label: "En vacances"
                fillColor: "rgba(46,217,138,0.2)"
                strokeColor: "rgba(46,217,138,1)"
                pointColor: "rgba(46,217,138,1)"
                pointStrokeColor: "#fff"
                pointHighlightFill: "#fff"
                pointHighlightStroke: "rgba(46,217,138,1)"
                data: [
                    2
                    5
                    9
                    14
                    20
                    15
                    9
                ]
            }
            {
                label: "Désactivés"
                fillColor: get_rgba(ORANGE_RGB, 0.2)
                strokeColor: get_rgba(ORANGE_RGB, 1)
                pointColor: get_rgba(ORANGE_RGB, 1)
                pointStrokeColor: "#fff"
                pointHighlightFill: "#fff"
                pointHighlightStroke: get_rgba(ORANGE_RGB, 1)
                data: [
                    0
                    1
                    2
                    3
                    4
                    3
                    3
                ]
            }
        ]

    users_status_canvas = get2dContext("users_status_canvas")
    chart_user_status = new Chart(users_status_canvas).Line(data_users_status)
    document.getElementById("users_status_legend").innerHTML = "Légende: <ul style='display: inline; padding-left: 0px;'>
            <li style='display: inline; padding-left: 7px; color: #{get_rgba(LIGHT_BLUE_RGB, 1)}'> Actifs </li>
            <li style='display: inline; padding-left: 7px; color: #{get_rgba(GREEN_RGB, 1)}'> En vacances </li>
            <li style='display: inline; padding-left: 7px; color: #{get_rgba(ORANGE_RGB, 1)}'> Désactivés </li>
        </ul>"


    # Most done job categories
    data_job_categories =
        labels: [
            "Visites à domicile"
            "Tenir compagnie"
            "Transport par voiture"
            "Shopping"
            "Garder la maison"
            "Boulots manuels"
            "Jardinage"
            "Soins personnels"
            "Administratif"
            "Autre"
            "Spécial... :D"
        ]
        datasets: [
            label: "Membres"
            fillColor: "rgba(151,187,205,0.2)"
            strokeColor: "rgba(151,187,205,1)"
            pointColor: "rgba(151,187,205,1)"
            pointStrokeColor: "#fff"
            pointHighlightFill: "#fff"
            pointHighlightStroke: "rgba(151,187,205,1)"
            data: [
                40
                30
                60
                70
                25
                47
                39
                69
                34
                23
                69
            ]
        ]

    job_categories = get2dContext("job_categories")
    chart_job_categories = new Chart(job_categories).Radar(data_job_categories)

