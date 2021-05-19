// console.log(io)
var socket = io.connect('http://' + document.domain + ':' + location.port + '/charts');
      
socket.on('makeChart', function(msg) {
    console.log('Chart connected');
    console.log(msg.values);

    google.charts.load('current', {packages: ['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawAnnotations);

    function drawAnnotations() {
        var points = [['Element', 'Percentage', { role: 'style' }]]
        for(i in msg.values){
        points.push([i, msg.values[i], '#blue'])
    }  

  var data = google.visualization.arrayToDataTable(points);

  var options = {
    title: 'Average Attendance of all Sessions',
    chartArea: {width: '50%'},
    annotations: {
      alwaysOutside: true,
      textStyle: {
        fontSize: 12,
        auraColor: 'none',
        color: '#555'
      },
      boxStyle: {
        stroke: '#ccc',
        strokeWidth: 1,
        gradient: {
          color1: '#f3e5f5',
          color2: '#f3e5f5',
          x1: '0%', y1: '0%',
          x2: '100%', y2: '100%'
        }
      }
    },
    hAxis: {
      title: 'Attendance in Percentage',
      minValue: 0,
    },
    vAxis: {
      title: 'Sessions'
    }
  };
  var chart = new google.visualization.BarChart(document.getElementById('chart_div'));
  chart.draw(data, options);
  }
    });

