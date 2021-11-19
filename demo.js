var token = localStorage.getItem("jwt");
var customData =localStorage.getItem("customData")
var session_id = localStorage.getItem("sessionid");
console.log(session_id)
console.log(typeof(customData));
if (token == null) {
  window.location.href = './login.html'
}


function loadUser() {
  
  let name = document.getElementById("geeks")
  let form = document.getElementById("myform")
  
  /* var file = name.files[0]; */
  // form.addEventListener('submit',async function(e) {
  //   e.preventDefault()
  //   let file = name.files[0]
  //   let formData = new FormData()
  //  formData.append('file', file)
//    async function(e) {
   const response =  fetch('http://65.2.62.107:8083/auth/user', {
      method: 'POST',
      headers:{
        'Authorization':token
      }
     
    }).then(response=>{
    if(response.status == 200){
        return response.text()
        objects = response.text();
                  
    }
    else{
      throw response.status
    }
    }).then(data=>{
     objects =  JSON.parse(data)
      
     localStorage.setItem("customData",JSON.stringify({ language: "en","Name_with_Initials":objects["user"]["Name_with_Initials"],"userName":objects["user"]["firstname"]+" " +objects["user"]["lastname"] , "email" : objects["user"]["email"],"image":null}))
  //    setTimeout(function(){
  //     window.location.reload();
  // }, 60);
     document.getElementById("firstname").innerHTML = "Hello, " +objects["user"]["firstname"]+" " +objects["user"]["lastname"];
    !(function () {
                         var session_id = localStorage.getItem("sessionid");
console.log(session_id)

        // console.log(objects["user"]["firstname"]+" " +objects["user"]["lastname"]);
      let e = document.createElement("script"),
        t = document.head || document.getElementsByTagName("head")[0];
        // console.log(t);
      (e.src =
        "http://65.2.62.107:9000/rasa/lib/index.js"),
        // Replace 1.x.x with the version that you want
        (e.async = !0),
        (e.onload = () => {
          window.WebChat.default(
            {

              customData:{ language: "en", "userName":objects["user"]["firstname"]+" " +objects["user"]["lastname"] , "email" : objects["user"]["email"],"session_id" :session_id},
                socketUrl: "http://3.229.112.164:5005/",
		params:{
		storage:"session"}
	       //old link - socketUrl: "http://16977b983d6e.ngrok.io/",
              // add other props here
            }
                      );
        }),
        // alert("username: "+objects["user"]["firstname"]+" " +objects["user"]["lastname"]+"\n"+ "email: "+objects["user"]["email"])
        t.insertBefore(e, t.firstChild);
        
    })();
	   
    
    }).catch(err=>{
       console.log(err);
     })
   
   
 
}
loadUser()
function logout() {
  localStorage.removeItem("jwt");
  window.location.href = './login.html'
}
