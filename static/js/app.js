// Secciones colapsables de los estados financieros
document.querySelectorAll(".plegar").forEach((boton) => {
  boton.addEventListener("click", () => {
    const abierto = boton.getAttribute("aria-expanded") === "true";
    boton.setAttribute("aria-expanded", String(!abierto));
    boton.closest("tbody").classList.toggle("plegado", abierto);
  });
});

// Muestra el saldo actual de la cuenta elegida en la barra de ajuste
const cuenta = document.getElementById("ajuste-cuenta");
if (cuenta) {
  const mostrar = () => {
    document.getElementById("ajuste-actual").textContent =
      "Saldo actual: " + cuenta.selectedOptions[0].dataset.saldo;
  };
  cuenta.addEventListener("change", mostrar);
  mostrar();
}

// Al imprimir se abren todas las secciones
window.addEventListener("beforeprint", () => {
  document.querySelectorAll("details").forEach((d) => { d.open = true; });
});
