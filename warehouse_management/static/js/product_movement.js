
  function validateQuantity() {
    var quantity = document.getElementById("quantity").value;
    var message = document.getElementById("quantity_error_span");
    if (quantity   == "" ){
      message.innerHTML="\"Quantity\" cannot be empty";
      message.style.visibility="visible";
      return false
    }
    else{
      message.style.visibility="hidden";
      return true
    }
  }
  
  function validateFromLocationSelect(){
    var from = document.getElementById("from_location_id").selectedIndex;
    var to = document.getElementById("to_location_id").selectedIndex;
    var from_message = document.getElementById("from_location_id_error_span");
    var to_message = document.getElementById("to_location_id_error_span");
  
   if(from==to){
      from_message.innerHTML="\"From Location\" cannot be equal to \"To Location\"";
      from_message.style.visibility="visible";
      return false
    }
    else{
      from_message.style.visibility="hidden";
      to_message.style.visibility="hidden";
      return true
    }
  }
  
  function validateToLocationSelect(){
    var from = document.getElementById("from_location_id").selectedIndex;
    var to = document.getElementById("to_location_id").selectedIndex;
    var from_message = document.getElementById("from_location_id_error_span");
    var to_message = document.getElementById("to_location_id_error_span");
    if(from==to){
      to_message.innerHTML="\"To Location\" cannot be equal to \"From Location\"";
      to_message.style.visibility="visible";
      return false
    }
    else{
      to_message.style.visibility="hidden";
      from_message.style.visibility="hidden";
      return true
    }
  }
  
  function validateAll(){
    return ( validateFromLocationSelect() && validateQuantity() && validateToLocationSelect() );
  }