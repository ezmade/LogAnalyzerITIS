document.getElementById('select_report').onchange = function () {
  document.querySelectorAll('.forma form').forEach(function (e) {
    e.style.display = 'none';
  });
  if ((this.value == 'country_category') || (this.value == 'time_category')) {
    document.getElementById('category').style.display = 'block';
  }

}

var chart;

function getReport() {

  var report = document.getElementById('select_report').value;
  var category = document.getElementById('select_category').value;

  if (report == "None") {
    swal({
      title: "Ошибка!",
      text: "Выберите тип отчёта!",
      type: "error",
      confirmButtonText: "Понятно"
    });
  }

  else if ((category == "None") &
    ((report == "country_category") ||
      (report == "time_category"))) {
    swal({
      title: "Ошибка!",
      text: "Выберите категорию!",
      type: "error",
      confirmButtonText: "Понятно"
    });
  }

  else {
    document.getElementById('myChart').style.display = 'grid';
    switch (report) {
      case 'country':
        reportByCountries();
        break;
      case 'country_category':
        reportByCountriesAndCategory(category);
        break;
      case 'time_category':
        reportByTimeAndCategory(category);
        break;
    }
  }
}


function reportByCountries() {
  var xhr = new XMLHttpRequest();
  xhr.open('GET', 'reportByCountries');
  xhr.send();
  xhr.onreadystatechange = function () {
    if (xhr.responseText !== '') {
      var serverResponse = JSON.parse(xhr.responseText);
      var axisX = [];
      var axisY = [];
      for (var i = 0; i < serverResponse.length; i++) {
        axisY.push(serverResponse[i][0]);
        axisX.push(serverResponse[i][1]);
      }
      var ctx = document.getElementById('myChart').getContext('2d');
      if (chart)
        chart.destroy();
      chart = new Chart(ctx, {
        type: 'horizontalBar',

        data: {
          labels: axisY,
          datasets: [{
            label: 'Действия на сайте по странам',
            backgroundColor: '#3976d3',
            data: axisX
          }]
        },

        options: {}
      });
    }
  }
}

function reportByCountriesAndCategory(category) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'reportByCountriesAndCategory', true);
  xhr.send(category);
  xhr.onreadystatechange = function () {
      if (xhr.responseText !== '') {
        var serverResponse = JSON.parse(xhr.responseText);
        var axisX = [];
        var axisY = [];
        for (var i = 0; i < serverResponse.length; i++) {
          axisY.push(serverResponse[i][0]);
          axisX.push(serverResponse[i][1]);
        }
        var ctx = document.getElementById('myChart').getContext('2d');
        if (chart)
          chart.destroy();
        chart = new Chart(ctx, {
          type: 'horizontalBar',

          data: {
            labels: axisY,
            datasets: [{
              label: 'Количество посетителей категории ' + category.toString() + ' по странам',
              backgroundColor: '#3976d3',
              data: axisX
            }]
          },

          options: {}
        });
      }
  }
}

function reportByTimeAndCategory(category) {
  var xhr = new XMLHttpRequest();
  xhr.open('POST', 'reportByTimeAndCategory', true);
  xhr.send(category);
  xhr.onreadystatechange = function () {
    if (xhr.responseText !== '') {
      var serverResponse = JSON.parse(xhr.responseText);
      var ctx = document.getElementById('myChart').getContext('2d');
      if (chart)
        chart.destroy();
      chart = new Chart(ctx, {
        type: 'doughnut',

        data: {
          labels: ["NIGHT", "MORNING", "DAY", "EVENING"],
          datasets: [{
            backgroundColor: ['#e93838', '#3976d3', '#d4872f', '#3976d3'],
            borderColor: 'black',
            data: [serverResponse["NIGHT"].toString(), serverResponse["MORNING"].toString(), serverResponse["DAY"].toString(), serverResponse["EVENING"].toString()]
          }]
        },

        options: {}
      });
    }
  }
}

