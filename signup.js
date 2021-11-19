var jwt = localStorage.getItem("jwt");
if (jwt != null) {
  window.location.href = './demo.html'
}

function signup() {
  const Name_with_Initials  =document.getElementById("Name with Initials").value;
  const firstname = document.getElementById("firstname").value;
  const lastname = document.getElementById("lastname").value;
  const password = document.getElementById("password").value;
  const email = document.getElementById("email").value;
  const business_name = document.getElementById("bname").value;
  const business_type = document.getElementById("btype").value;
  const business_address = document.getElementById("baddress").value;
  
  

  const xhttp = new XMLHttpRequest();
  xhttp.open("POST", "http://65.2.62.107:8083/signup",true);
  xhttp.setRequestHeader("Content-Type", "application/json;");
  xhttp.send(JSON.stringify({
	"Name_with_Initials":Name_with_Initials,
    "email": email,
    "password": password,
    "firstname":firstname,
    "lastname":lastname,
    "business_name":business_name,
    "business_type":business_type,
    "business_address":business_address
  }));
  
console.log(xhttp.response)
xhttp.onreadystatechange = function () {
  console.log("in")
  if (this.readyState == 4) {
      
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
        text: objects['message'],
        icon: 'error',
        confirmButtonText: 'OK'
      });
    }
  }
};
  return false;
}

