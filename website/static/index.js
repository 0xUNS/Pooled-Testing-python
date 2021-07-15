function deleteGroup(groupId) {
  fetch("/delete-group", {
    method: "POST",
    body: JSON.stringify({ groupId: groupId }),
  }).then((_res) => {
    window.location.href = "/";
  });
}

function deletePerson(personId, groupId) {
  fetch("/delete-person", {
    method: "POST",
    body: JSON.stringify({ personId: personId }),
  }).then((_res) => {
    window.location.href = "/groupe/" + groupId;
  });
}

function viewGroup(groupId){
  window.location.href = "/groupe/" + groupId;
}

function addPerson(groupId){
  window.location.href = "/groupe/" + groupId + "/add-person";
}

function makeTests(groupId){
  window.location.href = "/groupe/" + groupId + "/rang";
}