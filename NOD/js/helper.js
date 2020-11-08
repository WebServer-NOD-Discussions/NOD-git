function accordian(a) {
  var x = document.getElementById(a);
  //alert(x.style.display === "");
  if (x.style.display === "" || x.style.display === "none") {
    //alert(2);
    x.style.display = "block";
  } else {
   // alert(3);
    x.style.display = "none";
  }
}

var slider1 = document.getElementById("myRange1");
var output1 = document.getElementById("SliderVal1");
output1.innerHTML = slider1.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider1.oninput = function() {
  output1.innerHTML = this.value;
} 

var slider2 = document.getElementById("myRange2");
var output2 = document.getElementById("SliderVal2");
output2.innerHTML = slider2.value; // Display the default slider value

// Update the current slider value (each time you drag the slider handle)
slider2.oninput = function() {
  output2.innerHTML = this.value;
}