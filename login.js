var jwt = localStorage.getItem("jwt");
if (jwt != null) {
  window.location.href = './demo.html'
}

function login() {
  const loginemail = document.getElementById("loginemail").value;
 
  const loginpassword = document.getElementById("loginpassword").value;
  

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://65.2.62.107:8083/api/login");
  xhttp.setRequestHeader("Content-Type", "application/json;");
  xhttp.send(JSON.stringify({
    "email": loginemail,
    "password": loginpassword
  }));
  
  xhttp.onreadystatechange = function () {
    
    if (this.readyState == 4) {
      console.log(this.readyState);
      console.log(this.responseText);
      const objects = JSON.parse(this.responseText);
      console.log(objects);
      if (objects['status'] == 'ok') {
        localStorage.setItem("jwt", objects['accessToken']);
        Swal.fire({
          text: objects['message'],
          icon: 'success',
          confirmButtonText: 'OK'
        }).then((result) => {
          if (result.isConfirmed) {
            window.location.href = './demo.html';
          }
        });
      } else {
        
        Swal.fire({
          text: objects[0]['message'],
          icon: 'error',
          confirmButtonText: 'OK'
        });
      }
    }
  };
  return false;
}