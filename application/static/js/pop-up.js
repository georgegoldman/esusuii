
function joinGroup(group_id) {
  
  var group_id = group_id;
  
  var entry = {
    group_id: group_id
  };

  fetch(`${window.origin}/join_group?${group_id}`, {
    method: "POST",
    credentials: "include",
    body: JSON.stringify(entry),
    cache: "no-cache",
    headers: new Headers({
      "content-type": "application/json"
    })
  })
  .then(function (response) {

    if (response.status !== 200) {

      console.log(`Response status was not 200: ${response.status}`);
      return ;

    }

    response.json().then(function (data) {

      alert(data['message']);
      location.reload();

    })

  })

}

function leaveGroup(group_id, user_id, member_id) {

  var group_id = group_id;
  
  var entry = {
    group_id: group_id
  };

  if (user_id == member_id){
    confrim_leave = confirm('Click ok to confirm leave');
    if (confrim_leave){
      fetch(`${window.origin}/leave_group?${group_id}`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(entry),
        cache: "no-cache",
        headers: new Headers({
          "content-type": "application/json"
        })
      })
        .then(function (response){

          if (response.status !== 200){
            console.log(`your response status was not 200: ${response.status}` );
            return ;
          }

          response.json().then(function (data) {
            alert(data['msg']);
            location.reload()

          })
        })
     }

  }
  else{
    confirm('Leave rights to members only.');
  }

}


document.getElementById('msg').addEventListener('click', rstem);

function rstem() {
  var email = prompt('enter email');
  console.log(email);

  if (email) {
    fetch(`${window.origin}/send_reset_password_mail?email=${email}`)

      .then( function (response) {
        if (response.status != 200){
          console.log(`Response status was not 200: ${response.status}`);
          return ;
        }

        response.json().then(function (data) {
          alert(data['msg']);
        })
      })
  }
}