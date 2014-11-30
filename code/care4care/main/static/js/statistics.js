(function() {
  var draw_chart_type, get2dContext;

  get2dContext = function(id) {
    return document.getElementById(id).getContext("2d");
  };

  window.create_chart = function(url_json, canvas_id, chart_type) {
    return $.ajax(url_json, {
      dataType: "json",
      success: function(json_data) {
        var context;
        context = get2dContext(canvas_id);
        return draw_chart_type(context, json_data, chart_type);
      },
      error: function(err) {
        return console.log("Could not load: " + url_json);
      }
    });
  };

  draw_chart_type = function(context, data, chart_type) {
    var chart;
    chart = new Chart(context);
    switch (chart_type) {
      case "Line":
        return chart.Line(data);
      case "Bar":
        return chart.Bar(data);
      case "Doughnut":
        return chart.Doughnut(data);
      case "Radar":
        return chart.Radar(data);
    }
  };

}).call(this);
