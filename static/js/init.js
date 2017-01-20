
const design = { id: "", design: null, all: null };


function redrawForm(data, newType, newMethod, form) {
  let config = null;
  console.log(newType, newMethod)
  for (let d of design.all.components) {
    if (d.key == newType) {
      config = d;
      break;
    }
  }
  if (!config) {
    return;
  }
  data.cmp = newType;
  data.method = newMethod;
  let select = $(form).find('select[name="cmpmethod"]')
  select.empty();
  select.append($('<option></option>')
    .attr('value', "")
    .attr('disabled', "")
    .text('Choose your option'));
  if (newMethod === null) {
    newMethod = config.methods[0].name
  }
  for (let m of config.methods) {
    let o = $('<option></option>')
      .attr('value', m.name)
      .text(m.name)
    if (m.name == newMethod) {
      o.attr('selected', "")
    }
    select.append(o);
  }
  $(form).find('div:gt(3)').remove();
  let btn = $(form).find('button')
  for (let a of config.attributes) {
    if (a.required_by.indexOf(newMethod) < 0) {
      continue;
    }
    let iff = $('<div class="input-field"></div>')

    if (a.props.enum) {
      let select = $('<select onchange="onformchanged(this.form)" > </select>').attr('name', a.name)
      select.append($('<option></option>')
        .attr('value', "")
        .attr('disabled', "")
        .text('Choose your option'));
      for (let o of a.props.enum) {
        let p = $('<option></option>')
          .attr('value', o)
          .text(o)
        select.append(p);
      }
      iff.append(select)
      let llb = $('<label class="active" ></label>')
      llb.text(a.name)
      iff.append(llb)
    } else {
      let inp = $('<input class="validate" onchange="onformchanged(this.form)" >')
      inp.attr('name', a.name)
      if (a.type === 'float') {
        inp.attr('type', 'number')
        inp.attr('step', '0.01')
        inp.attr('value', '0')
      } if (a.type === 'int') {
        inp.attr('type', 'number')
        inp.attr('step', '1')
        inp.attr('value', '0')
      } else if (a.type === 'str') {
        inp.attr('type', 'text')
        inp.attr('value', '')
      }
      iff.append(inp)
      let llb = $('<label class="active" ></label>')
      llb.attr('for', a.name)
      llb.text(a.name)
      iff.append(llb)
    }
    iff.insertBefore(btn)
  }

  $('select').material_select();
}

function updateCmp(data, form) {
  console.log('updateCmp', data)
  if (!design.design) {
    return
  }
  for (let c of design.design.cmps) {
    if (c.id === data.id) {
      c.args = data.args;
      if (c.cmp !== data.cmp) {
        redrawForm(c, data.cmp, null, form);
      } else if (c.method !== data.method) {
        redrawForm(c, c.cmp, data.method, form);
      }
      return
    }
  }
}

function deleteCmp(id) {
  if (!design.design) {
    return
  }
  let index = design.design.cmps.findIndex((v) => v.id === id)
  design.design.cmps.splice(index, 1)
}

function updateDesign(data, cb) {
  let str = JSON.stringify(data)
  $.post('update', str, cb, 'json')
  deleteCookie('design')
}

function saveDesign(cb) {
  if (!design.id) {
    $.get('newDesign', function (data) {
      console.log('new design', data.id)
      design.id = data.id;
      window.localStorage.setItem('id', data.id);
      updateDesign({ id: data.id, design: design.design }, (s) => {
        console.log(s);
        if (cb) {
          cb(s)
        }
      })
    })
  } else {
    let data = { id: design.id, design: design.design }
    updateDesign(data, (s) => {
      console.log(s);
      if (cb) {
        cb(s)
      }
    })
  }
}
function makeid() {
  var text = "";
  var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
  for (var i = 0; i < 10; i++)
    text += possible.charAt(Math.floor(Math.random() * possible.length));
  return text;
}

function getAllComponentsAndMethods() {
  $.get("allComponents", function (data) {
    design.all = data;
  })
}

function addComponent() {
  let cmp = design.all.components[0]
  design.design.cmps.push({
    id: makeid(),
    cmp: cmp.key,
    method: cmp.methods[0].name,
    args: {}
  })
  console.log(design.design)
  saveDesign(() => {
    window.location.reload()
  })
}

function resetDesign() {
  deleteCookie('design')
  deleteCookie('id')
  window.localStorage.removeItem('id')
  window.location.reload();
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
function deleteCookie(name) {
  document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}
function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue;
}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for (var i = 0; i < ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return "";
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
String.prototype.replaceAll = function (search, replacement) {
  var target = this;
  return target.split(search).join(replacement);
};

(function ($) {
  getAllComponentsAndMethods();
  let d = getCookie('design')
  if (d) {
    try {
      let rep = d.replaceAll('\\"', '"').replaceAll('\\054', ',')
      rep = rep.substring(1, rep.length - 1)
      let des = JSON.parse(rep)
      design.design = des
    } catch (ex) {
      console.error(d, ex)
    }
  } else {
    console.log("no design cookie")
  }
  design.id = window.localStorage.getItem('id')
  if (getCookie('id') === "" && design.id !== null) {
    setCookie('id', design.id)
  }
  $(document).ready(function () {
    $('select').material_select();
    $('.tooltipped').tooltip({ delay: 50 });
    execute()
    $('#saveBtn').click(() => { saveDesign(() => { }) });
    $("#addBtn").click(addComponent);
    $("#resetBtn").click(resetDesign);
  })
})(jQuery); // end of jQuery name space


function serializeComp(f) {
  let arr = $(f).serializeArray();
  let d = { args: {} }
  for (let o of arr) {
    if (o.name == "cmpid") {
      d['id'] = o.value;
    } else if (o.name == 'cmpmethod') {
      d['method'] = o.value;
    } else if (o.name == 'cmptype') {
      d['cmp'] = o.value;
    }
  }
  let config = null;
  for (let c of design.all.components) {
    if (c.key == d.cmp) {
      config = c;
      break;
    }
  }
  for (let o of arr) {
    if ((o.name != "cmpid") && (o.name !== 'cmpmethod') && (o.name !== 'cmptype')) {
      d.args[o.name] = o.value
      for (let a of config.attributes) {
        if (a.name == o.name) {
          if (a.type == "float") {
            d.args[o.name] = parseFloat(o.value)
          } else if (a.type == "int") {
            d.args[o.name] = parseInt(o.value)
          }
        }
      }
    }
  }
  return d;
}

function onformchanged(f) {
  updateCmp(serializeComp(f), f)
}
