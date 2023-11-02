//Functions for setting cookies
function setCookie(name,value,days) {
  var expires = "";
  if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days*24*60*60*1000));
      expires = "; expires=" + date.toUTCString();
  }
  document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

function getCookie(name) {
  var nameEQ = name + "=";
  var ca = document.cookie.split(';');
  for(var i=0;i < ca.length;i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1,c.length);
      if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
  }
  return null;
}

function eraseCookie(name) {   
  document.cookie = name +'=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;';
}

// Everything below here is website specific code for blord.xyz. You should delete it if use this code as it won't to anything for you
// =-=-=-=-=-=-=-=-=-=-=

//Nginx handels what index is sent based on the cookie 'index_style'
var indxstyle = getCookie('index_style');

//Gets input from box, sets the cookie and then reloads the page
function index_cookie_input(input) {
valid_input="1";
  if (input=="fancy") {
  setCookie('index_style','fancy',1000);
} else if (input=="old") {
  setCookie('index_style','old',1000);
  } else if (input=="remove" || input=="default") {
  eraseCookie('index_style');
  } else if (input=="") {
  
} else {
  valid_input="0";
}

var indxstyle = getCookie('index_style');

if (valid_input=="1") {
  //console.log("Index style set to '" +  indxstyle + "'")
              alert("Index style set to '" +  indxstyle + "'")
  document.location.reload(true)
} else {
  //console.log("Invalid input")
              alert("Invalid input")
}
}
line_start="Currently set to '";
line_end="'";

const app = document.getElementById('cookie');
const container = document.createElement('div');
container.setAttribute('class', 'container');
app.appendChild(container);
const card = document.createElement('div');
card.setAttribute('class', 'card');

const p1 = document.createElement('p');
p1.textContent = line_start + indxstyle + line_end;

container.appendChild(card);
card.appendChild(p1);

//console.log("Current index style is set to '" + indxstyle + "'");
