// console.log(io)
    function myfunc(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    var sessions = $('#session_cat').find(":selected").text();
    var dates = $('#date_cat').find(":selected").text();
    var members = $('#member_cat').find(":selected").text();

    socket.emit("message", {sessions, dates, members})
    // socket.send($('#session_cat').find(":selected").text())


    //receive details from server
    socket.on('display', function(msg) {
        console.table("Received number" + msg.number);
        var t = "<center><table border=2><thead>";
        for(row in msg.number){
            t = t + "<tr>";
            for(value in msg.number[row]){
                if(row==0){
                    t = t + '<th style="font-weight: bold;">'
                }
                else{
                    t = t + "<td>";
                }
                t = t + msg.number[row][value];
                if(row==0){
                    t = t + "</th>"
                }
                else{
                t = t + "</td>";
                }
            }
            if(row==0){
                t = t + "</thead><tbody>"
            }
            else{
            t = t + "</tr>"
            }
        }
        t = t + "</tbody></table></center>";
        $('#log').html(t);
        //     if(msg.per!=-1){
        //     var r = "<table><tbody>"
        //     for(var i in msg.all_per){
        //         r = r +"<tr><td>" + i + "</td><td>" + msg.all_per[i] + "</td></tr>"
        //     }
        //     r = r + "</tbody></table>"
        //     $('#memrec').html(r)
        // }
    });

};


function mymemfunc(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.emit("membermessage", $('#memname').find(":selected").text())
        
    socket.on('memdisplay', function(msg) {
        img_src_string = '<img src="' + "/static/User%20Accounts/" + msg.mems[5].slice(21) + '" width="200">'
        content = '<table><tbody><tr><td id="memid">'+msg.mems[0]+"</td><td rowspan='5' id='image'>" + img_src_string + "</td></tr>"+
    '<tr><td id="memn">'+msg.mems[1]+"</td></tr> <tr><td>"+msg.mems[2]+"</td></tr> <tr><td>"+msg.mems[3]+"</td> </tr><tr><td>"+msg.mems[4]+"</td></tr></tbody></table>"
        $('#rec').html(content);

    console.table(msg.all_rec);
    console.log(msg.total_p);
    $('h2#totalatt').html('Average Attendance: '+ msg.total_p.toString() + '%');
    $('#chartHeader').html('Average Attendance of above member in all Sessions');

    google.charts.load('current', {packages: ['corechart', 'bar']});
    google.charts.setOnLoadCallback(drawAnnotations);

    function drawAnnotations() {
        var points = [['Element', 'Percentage', { role: 'style' }]]
        for(i in msg.all_rec){
        points.push([i, msg.all_rec[i], '#blue'])
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
  var chart = new google.visualization.BarChart(document.getElementById('chart_per'));
  chart.draw(data, options);
  }

    });
};


function delMeme(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var memID = $('#memid').text()
    var memN = $('#memn').text()
    socket.emit("delmem", {memID,memN})
    console.log($('#memid').text())
    alert('Member '+memN+' Deleted, Refresh the page to see changes')
        
}



function showStatus(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var memD = $('#memd').find(":selected").text();
    var memNs = $('#memn').find(":selected").text();
    socket.emit("showST", {memD,memNs});
}

function updateS(){
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var memD = $('#memd').find(":selected").text();
    var memNs = $('#memn').find(":selected").text();
    var r = $("h2").text();
    socket.emit("upST", {memD,memNs,r});
    alert('Record updated, Refresh the page to see changes')
}

var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

socket.on('uName', function(msg) {
    console.log(msg.name);
    console.log($('a').attr('href'));
    $('a#filepath').attr('href', "/static/User%20Accounts/"+msg.name+"/sheets/records.csv")

});
        
socket.on('uStatus', function(msg) {
    $("h2").html(msg.s)

});
  
socket.on('makeChart', function(msg) {
    console.log('App Conn')
    console.log(msg.values);

});

