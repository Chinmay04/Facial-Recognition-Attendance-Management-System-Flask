function validateMember(){
	var name = document.memform.membername.value
	var rollno = document.memform.rollno.value
	var email = document.memform.email.value
	var contact = document.memform.contact.value
	var photo = document.memform.photo.value

  // name
  if(/[^a-zA-Z]/.test(name.replace(/\s/g,'')) || name == null || name == ''){
    return false;
  }

	// Email
	var atposition=email.indexOf("@");  
  var dotposition=email.lastIndexOf(".");  
  if (atposition<1 || dotposition<atposition+2 || dotposition+2>=email.length){  
    alert("Please enter a valid e-mail address \n atpostion:"+atposition+"\n dotposition:"+dotposition);  
    return false;  
    }  

  // contact
  if(contact.length!=10 || isNaN(contact)){
  	return false;
  }

   // rollno
   if(isNaN(rollno)){
   	return false;
  }
}

function validateSignup(){
  var name = document.signupform.username.value
  var pass = document.signupform.password.value
  var email = document.signupform.email.value
  var contact = document.signupform.contact.value
  var repass = document.signupform.repassword.value

  if(/[^a-zA-Z]/.test(name.replace(/\s/g,'')) || name == null || name == ''){
    return false;
  }

  var atposition=email.indexOf("@");  
  var dotposition=email.lastIndexOf(".");  
  if (atposition<1 || dotposition<atposition+2 || dotposition+2>=email.length){  
    return false;  
    }  

  if(contact.length!=10 || isNaN(contact)){
      return false;
    }

    if(pass != repass){
      alert("Passwords don't match")
      return false;
    }
}

function validateLogin(){
  var name = document.loginform.username.value
  var pass = document.loginform.password.value

  if(/[^a-zA-Z]/.test(name.replace(/\s/g,'')) || name == null || name == ''){
    return false;
  }
}