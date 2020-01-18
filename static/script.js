document.getElementById('select_report').onchange = function() {
    document.querySelectorAll('.forma form').forEach(function(e) {
      e.style.display = 'none';
    });
    document.getElementById(this.value).style.display = 'block';
  }

  function sendAlert() {
      if (document.getElementById('select_report').value == "None") {
        swal({
            title: "Ошибка!",
            text: "Выберите тип отчёта!",
            type: "error",
            confirmButtonText: "Понятно"
        });
      }
      
      if ((document.getElementById('select_category').value == "None") &
      (document.getElementById('select_report').value == "category")) {
        swal({
            title: "Ошибка!",
            text: "Выберите категорию!",
            type: "error",
            confirmButtonText: "Понятно"
        });
      }
  }

  
    