document.getElementById("jsonInput").addEventListener("input", function () {
  const val = this.value;
  document.getElementById("output").innerHTML = `<pre>${val}</pre>`;
});
