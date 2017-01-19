
function saveComponent() {

}

function getAllComponentsAndMethods() {
  $.get("allComponents", function (data) {
    console.log(data)
  })
}

function execute() {
  var form = document.forms.namedItem("fileupload");
  form.addEventListener('submit', function (ev) {
    var oOutput = document.getElementById('execute-result')
    var oData = new FormData(form);

    oData.append("CustomField", "This is some extra data");

    var oReq = new XMLHttpRequest();
    oReq.open("POST", "imageButton", true);
    oOutput.innerHTML = "Loading..."
    oReq.onload = function (oEvent) {
      console.log(oReq);
      if (oReq.status == 200) {
        let result = JSON.parse(oReq.responseText)
        if (typeof result.error === "undefined") {
          oOutput.innerHTML = '<img class="output-image" src="' + result.picture + '" />'
        } else {
          oOutput.innerHTML = "Error:" + result.error;
        }
      } else {
        oOutput.innerHTML = "Error " + oReq.status + " occurred when trying to upload your file.<br \/>";
      }
    };

    oReq.send(oData);
    ev.preventDefault();
  }, false);
}

function executeImage(compid) {
  let data = {
    id: 'asdasd',
    design: {
      cmps: [{

      }]
    }
  }
  $.ajax({
    type: "POST",
    url: "calculate",
    data: data,
    dataType: "application/json",
    success: (s) => {
      let result = JSON.parse(s)
      console.log(result.picture)
    },
  });
}

(function ($) {
  $(document).ready(function () {
    $('select').material_select();
    execute()
    $('#saveBtn').click(function () {
      console.log("saveBtn clicked")
      getAllComponentsAndMethods()
    })
  });
})(jQuery); // end of jQuery name space

