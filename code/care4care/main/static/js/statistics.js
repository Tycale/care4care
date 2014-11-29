(function() {
  $(function() {
    var GREEN_RGB, LIGHT_BLUE_RGB, ORANGE_RGB, c_line, c_polar, c_radar, create_chart, data, draw_chart_type, get2dContext, get_rgba, line_chart, polar_chart, polar_data, radar_chart;
    get2dContext = function(id) {
      return document.getElementById(id).getContext("2d");
    };
    create_chart = function(url_json, canvas_id, chart_type) {
      return $.ajax(url_json, {
        dataType: "json",
        success: function(json_data) {
          var context;
          context = get2dContext(canvas_id);
          return draw_chart_type(context, chart_type, json_data);
        },
        error: function(err) {
          return console.log("Could not load: " + url_json);
        }
      });
    };
    draw_chart_type = function(context, chart_type, data) {
      var chart;
      chart = new Chart(context);
      switch (chart_type) {
        case "Line":
          return chart.Line(data);
        case "Doughnut":
          return chart.Doughnut(data);
        case "Radar":
          return chart.Radar(data);
      }
    };
    create_chart("/statistics/registrated_users_json", "global_registration", "Line");
    create_chart("/statistics/account_types_json", "account_types", "Doughnut");
    create_chart("/statistics/users_status_json", "users_status_canvas", "Line");
    LIGHT_BLUE_RGB = [151, 187, 205];
    GREEN_RGB = [46, 217, 138];
    ORANGE_RGB = [255, 169, 0];
    get_rgba = function(my_rgb, a) {
      return "rgba(" + my_rgb[0] + ", " + my_rgb[1] + ", " + my_rgb[2] + ", " + a + ")";
    };
    document.getElementById("users_status_legend").innerHTML = "Légende: <ul style='display: inline; padding-left: 0px;'> <li style='display: inline; padding-left: 7px; color: " + (get_rgba(LIGHT_BLUE_RGB, 1)) + "'> Actifs </li> <li style='display: inline; padding-left: 7px; color: " + (get_rgba(GREEN_RGB, 1)) + "'> En vacances </li> <li style='display: inline; padding-left: 7px; color: " + (get_rgba(ORANGE_RGB, 1)) + "'> Désactivés </li> </ul>";
    create_chart("/statistics/job_categories_json", "job_categories", "Radar");
    data = {
      labels: ["January", "February", "March", "April", "May", "June", "July"],
      datasets: [
        {
          label: "My First dataset",
          fillColor: "rgba(220,220,220,0.2)",
          strokeColor: "rgba(220,220,220,1)",
          pointColor: "rgba(220,220,220,1)",
          pointStrokeColor: "#fff",
          pointHighlightFill: "#fff",
          pointHighlightStroke: "rgba(220,220,220,1)",
          data: [65, 59, 80, 81, 56, 55, 40]
        }, {
          label: "My Second dataset",
          fillColor: "rgba(151,187,205,0.2)",
          strokeColor: "rgba(151,187,205,1)",
          pointColor: "rgba(151,187,205,1)",
          pointStrokeColor: "#fff",
          pointHighlightFill: "#fff",
          pointHighlightStroke: "rgba(151,187,205,1)",
          data: [28, 48, 40, 19, 86, 27, 90]
        }
      ]
    };
    c_line = document.getElementById("chart_line").getContext("2d");
    line_chart = new Chart(c_line).Line(data);
    c_radar = document.getElementById("chart_radar").getContext("2d");
    radar_chart = new Chart(c_radar).Radar(data);
    polar_data = [
      {
        value: 300,
        color: "#F7464A",
        highlight: "#FF5A5E",
        label: "Red"
      }, {
        value: 50,
        color: "#46BFBD",
        highlight: "#5AD3D1",
        label: "Green"
      }, {
        value: 100,
        color: "#FDB45C",
        highlight: "#FFC870",
        label: "Yellow"
      }, {
        value: 40,
        color: "#949FB1",
        highlight: "#A8B3C5",
        label: "Grey"
      }, {
        value: 120,
        color: "#4D5360",
        highlight: "#616774",
        label: "Dark Grey"
      }
    ];
    c_polar = document.getElementById("chart_polar").getContext("2d");
    return polar_chart = new Chart(c_polar).PolarArea(polar_data);
  });

}).call(this);
