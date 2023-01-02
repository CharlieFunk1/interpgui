window.addEventListener('load', function(){
      if (localStorage.pick) {
          var sel = document.querySelector('#strip-selector');
          sel.value = localStorage.pick;
      }
});

  function getSelectValue(){
      var sel = document.querySelector('#strip-selector');
      localStorage.pick = sel.value;
      location.replace('/setup/' + localStorage.pick);
  }

var drawstripstart = document.getElementById('drawstripstart');
drawstripstart.addEventListener('click', function(){
    
    var sel = document.querySelector('#strip-selector');
    location.replace('/drawstripstart/' + sel.value);
});

var drawstripend = document.getElementById('drawstripend');
drawstripend.addEventListener('click', function(){
    
    var sel = document.querySelector('#strip-selector');
    location.replace('/drawstripend/' + sel.value);
});

