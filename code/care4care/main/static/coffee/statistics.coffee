
get2dContext = (id) ->
    document.getElementById(id).getContext("2d")


# Create a chart
window.create_chart = (url_json, canvas_id, chart_type) ->
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
        when "Bar"
            chart.Bar(data)
        when "Doughnut"
            chart.Doughnut(data)
        when "Radar"
            chart.Radar(data)
