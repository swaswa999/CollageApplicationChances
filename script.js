//BLOCKS FORM RELOADING WARNING
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
  }

//COPY TEXT
function copyTheText() {
  var copyText = document.getElementById("outputbox");
  var textToCopy = copyText.textContent || copyText.innerText;

  var textarea = document.createElement("textarea");
  textarea.value = textToCopy;
  document.body.appendChild(textarea);

  textarea.select();
  document.execCommand("copy");

  document.body.removeChild(textarea);

  alert("Text Added To Clipboard");
}
