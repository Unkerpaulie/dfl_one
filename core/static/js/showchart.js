  // data elements: {labels(list), values(list), charttype, unit}
  function showlinechart(chart_cont, data) {
    const cv = document.createElement("canvas");
    // cv.height = 240;
    cv.classList.add("my-4");
    cv.classList.add("w-100");
    chart_cont.appendChild(cv);
      new Chart(cv, {
      type: data.charttype,
      data: {
        labels: data.labels,
        datasets: [{
          label: data.unit,
          data: data.values,
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        },
        plugins: {
          title: {
            display: true,
            text: `Total: ${data.total} ${data.unit}`
          },
          legend: {
            display: false
          }
        }
      }
    });
  }
  

