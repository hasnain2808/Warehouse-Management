function validateProductId() {
    var product_id = document.getElementById("product_id").value;
    var message = document.getElementById("product_id_error_span");
    if (product_id   == "" ){
      message.innerHTML="\"Product Name\" cannot be empty";
      message.style.visibility="visible";
      return false
    }
    else{
      message.style.visibility="hidden";
      return true
    }

  }
  function validateAll() {
    return validateProductId();
  }
