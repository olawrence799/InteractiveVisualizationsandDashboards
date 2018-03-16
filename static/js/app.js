function init() {
    var default_url = '/samples/BB_940'
    Plotly.d3.json(default_url, function(error, response) {
        if (error) return console.warn(error);
        var data = [response.sample_values]
        .slice(0,10);
    })
    // var data = [
    //   {
    //     values: [19, 26, 70, 73],
    //     labels: ['Spotify', 'Soundcloud', 'Pandora', 'Itunes'],
    //     type: 'pie',
    //   },
    // ];
  
    var layout = {
      height: 600,
      width: 800,
    };
  
    Plotly.plot('pie', data, layout);
  }

//   var names_url = '/samples/<sample>'
  var samples_url = '/otu'
  

  function updatePlotly(newdata) {
    var PIE = document.getElementById('pie');
    Plotly.restyle(PIE, 'values', [newdata]);
  }
  
  function optionChanged(route) {
    console.log(route);
    Plotly.d3.json(`/samples/${route}`, function(error, data) {
        console.log("newdata", data);
        updatePlotly(data);
    });
    // var data = [];
    // switch (dataset) {
    //   case 'BB_941':
    //     data = [10, 30, 40, 20];
    //     break;
    //   default:
    //     data = [];
    // }
    // updatePlotly(data);
  }
  
  init();
  

// /* data route */
// var url = '/data';

// function buildPlot() {
//   Plotly.d3.json(url, function(error, response) {
//     console.log(response);
//     var trace1 = {
//       type: 'scatter',
//       mode: 'lines',
//       name: 'Bigfoot Sightings',
//       x: response.years,
//       y: response.sightings,
//       line: {
//         color: '#17BECF',
//       },
//     };

//     var data = [trace1];

//     var layout = {
//       title: 'Bigfoot Sightings Per Year',
//       xaxis: {
//         type: 'date',
//       },
//       yaxis: {
//         autorange: true,
//         type: 'linear',
//       },
//     };

//     Plotly.newPlot('plot', data, layout);
//   });
// }

// buildPlot();
