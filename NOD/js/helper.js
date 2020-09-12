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