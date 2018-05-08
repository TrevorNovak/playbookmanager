var playbook = ["TEST", "NEXT", "THIS"]

function getAttackPattern(){
  $(document).ready(function() {
      $.ajax({
          url: "http://localhost:5000/playbookmanager/api/v1/attack-patterns/1"
      }).then(function(data) {
         $('.attack-pattern-desc').append(data[0].objects[0].description);
      });
  });
}

function removeItem(){
    var ul = document.getElementById("dynamic-list");
    var candidate = document.getElementById("candidate");
    var item = document.getElementById(candidate.value);
    ul.removeChild(item);
}

function printPlaybook() {
  document.write(playbook);
}

function addPattern(pattern) {
  playbook.append(pattern);
}

function getPlaybook() {
  return playbook;
}

function prints() {
  return "here"
}

function iter() {
  for(int i = 0; i < playbook.length; i++) {
    document.write(playbook[i]);
  }
}
