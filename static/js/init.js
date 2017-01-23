
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
  executeImage(data.id);
}

function executeImage(compid) {
  let des = {
    cmps: []
  }
  for (let c of design.design.cmps) {
    des.cmps.push(c);
    if (c.id == compid) {
      break;
    }
  }
  let data = {
    id: design.id,
    design: des
  }
  console.log(data);
  $.post('/calculate', JSON.stringify(data), (s) => {
    if (s.picture) {
      $('img[name="' + compid + '"]').attr('src', s.picture)
    }
    console.log('calculate res', s)
    $('#' + compid).removeClass('invalid-card')
  }, 'json').fail(function () {
    $('#' + compid).addClass('invalid-card')
  })
}

function setNotSaved(notsaved) {
  if (notsaved) {
    $("#logo-container").text("Image Pipeline **")
  } else {
    $("#logo-container").text("Image Pipeline")
  }
}

function updateCmp(data, form) {
  setNotSaved(true)
  console.log('updateCmp', data)
  if (!design.design) {
    return
  }
  let redrawed = false;
  for (let c of design.design.cmps) {
    if (c.id === data.id) {
      c.args = data.args;
      if (c.cmp !== data.cmp) {
        redrawed = true;
        redrawForm(c, data.cmp, null, form);
      } else if (c.method !== data.method) {
        redrawed = true;
        redrawForm(c, c.cmp, data.method, form);
      }
      break;
    }
  }
  if (redrawed) {
    return
  }
  executeAll();
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
  $.post('/update', str, cb, 'json')
  deleteCookie('design')
}

function saveDesign(cb) {
  setNotSaved(false)
  if (!design.id) {
    $.get('/newDesign', function (data) {
      console.log('new design', data.id)
      design.id = data.id;
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
  $.get("/allComponents", function (data) {
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
  deleteCookie('id')
  setTimeout(function () {
    console.log(getCookie('id'));
    window.location.href = '/';
  }, 5);
}

function componentForm(f, id) {
  f.addEventListener('submit', function (ev) {
    ev.preventDefault();
    $('#' + id).remove();
    var index = design.design.cmps.findIndex((v) => {
      return v.id === id
    })
    if (index >= 0) {
      design.design.cmps.splice(index, 1);
      saveDesign(() => {
        executeAll();
      });
    }
  }, false);
}

function executeAll() {
  for (let i = 0; i < design.design.cmps.length; i++) {
    var t = design.design.cmps[i];
    executeImage(t.id);
  }
}

function execute() {
  for (let i = 0; i < document.forms.length; i++) {
    let f = document.forms.item(i);
    if (f.name == 'fileupload') { continue }
    componentForm(f, f.name);
  }
  executeAll();
}

function deleteCookie(name) {
  document.cookie = name + '=; Path=/; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
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

String.prototype.replaceAll = function (search, replacement) {
  var target = this;
  return target.split(search).join(replacement);
};

function handleDesignUpload() {
  document.getElementById('fileinput').addEventListener('change', function () {
    if (this.files.length !== 1) {
      return;
    }
    var file = this.files[0];
    var reader = new FileReader();
    reader.onload = (e) => {
      console.log(e);
      try {
        var obj = JSON.parse(e.target.result);
        if (typeof obj.design !== "undefined") {
          design.design = obj.design;
          saveDesign(() => {
            window.location.reload();
          })
        } else {
          console.error("json file does not contain design", obj);
        }
      } catch (err) {
        console.error(err)
      }
    }
    reader.readAsText(file);
  }, false);
}

function sendFile(fileData) {
  var formData = new FormData();

  formData.append('image', fileData);
  formData.append('id', design.id);

  $.ajax({
    type: 'POST',
    url: '/upload',
    data: formData,
    contentType: false,
    processData: false,
    success: function (data) {
      executeAll();
    },
    error: function (data) {
      alert('There was an error uploading your file!');
    }
  });
}

function handleImageUpload() {
  document.getElementById('imageupload').addEventListener('change', function () {
    if (this.files.length !== 1) { return; }
    let file = this.files[0]
    saveDesign(() => {
      sendFile(file);
    })
  }, false);
}

(function ($) {
  getAllComponentsAndMethods();
  design.design = JSON.parse(designObj);
  design.id = designID;

  $(document).ready(function () {
    $('select').material_select();
    $('.tooltipped').tooltip({ delay: 50 });
    execute()
    handleDesignUpload();
    handleImageUpload();
    $('#saveBtn').click(() => { saveDesign(() => { }) });
    $("#addBtn").click(addComponent);
    $("#resetBtn").click(resetDesign);
    $('form input').on('keypress', function (e) {
      return e.which !== 13;
    });
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
