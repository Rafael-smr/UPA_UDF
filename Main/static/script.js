function adicionarFila() {
  const tipo = encodeURIComponent(document.getElementById("tipo").value);
  const preferencial = document.getElementById("preferencial").value;

  fetch(`/add/${tipo}/${preferencial}`)
    .then(response => {
      if (response.redirected) {
        window.location.href = response.url;
      }
    });
}
