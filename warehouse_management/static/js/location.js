
  function validateLocationId() {
    var location_id = document.getElementById("location_id").value;
    var message = document.getElementById("location_id_error_span");
    if (location_id   == "" ){
      message.innerHTML="\"Location Name\" cannot be empty";
      message.style.visibility="visible";
      return false
    }
    else{
      message.style.visibility="hidden";
      return true
    }

  }
  function validateAll() {
    return validateLocationId();
  }