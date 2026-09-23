// ============================================================
// VARIABLES GLOBALES
// ============================================================
let q_objetivo_global = 0;
let cuotas_global = 0;
let tolerancia_global = 0;

// ============================================================
// ELEMENTOS DEL DOM
// ============================================================
const numProductosSelect = document.getElementById("numProductos");
const blockP3 = document.getElementById("block-p3");
const btnCalcular = document.getElementById("btnCalcular");
const errorBox = document.getElementById("errorBox");

const placeholderResult = document.getElementById("placeholderResult");
const resultContent = document.getElementById("resultContent");
const statusBanner = document.getElementById("statusBanner");
const rebajasDisplay = document.getElementById("rebajasDisplay");

const resCuotas = document.getElementById("resCuotas");
const resCuotaObj = document.getElementById("resCuotaObj");
const resCuotaObt = document.getElementById("resCuotaObt");
const resDifCuota = document.getElementById("resDifCuota");
const resSObj = document.getElementById("resSObj");
const resSObt = document.getElementById("resSObt");

// ============================================================
// EVENTOS Y FORMATEADORES EN TIEMPO REAL
// ============================================================
numProductosSelect.addEventListener("change", actualizarVistaProductos);
btnCalcular.addEventListener("click", calcular);

document.addEventListener("DOMContentLoaded", () => {
  inicializarFormatoInputs();
});

function inicializarFormatoInputs() {
  const camposMoneda = document.querySelectorAll(".input-moneda");
  const camposPorcentaje = document.querySelectorAll(".input-porcentaje");

  camposMoneda.forEach((input) => {
    input.addEventListener("input", (e) => {
      let digitos = e.target.value.replace(/\D/g, "");
      if (digitos === "") {
        e.target.value = "";
      } else {
        const num = parseInt(digitos, 10);
        e.target.value = `$ ${num.toLocaleString("es-CL")}`;
      }
    });

    input.addEventListener("blur", (e) => {
      if (e.target.value.trim() === "$") {
        e.target.value = "";
      }
    });
  });

  camposPorcentaje.forEach((input) => {
    input.addEventListener("input", (e) => {
      let digitos = e.target.value.replace(/\D/g, "");
      if (digitos === "") {
        e.target.value = "";
      } else {
        let num = parseInt(digitos, 10);
        if (num > 100) num = 100;
        e.target.value = `${num} %`;
      }
    });
  });
}

function actualizarVistaProductos() {
  if (numProductosSelect.value === "3") {
    blockP3.classList.remove("hidden");
  } else {
    blockP3.classList.add("hidden");
  }
}

// ============================================================
// AUXILIARES: CONVERSIÓN Y FORMATO
// ============================================================
function obtenerNumero(idCampo) {
  const elemento = document.getElementById(idCampo);
  let texto = elemento ? elemento.value.trim() : "";

  if (texto === "") {
    throw new Error("Hay un campo vacío.");
  }

  // Extraer solo dígitos de los campos formateados
  texto = texto.replace(/\D/g, "");
  const num = parseFloat(texto);

  if (isNaN(num)) {
    throw new Error("Ingresa un valor numérico válido.");
  }

  return num;
}

function formatoMoneda(valor) {
  return new Intl.NumberFormat("es-CL", {
    style: "currency",
    currency: "CLP",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0
  }).format(valor);
}

function ocultarError() {
  errorBox.classList.add("hidden");
  errorBox.innerText = "";
}

function mostrarError(mensaje) {
  errorBox.innerText = mensaje;
  errorBox.classList.remove("hidden");
}

// ============================================================
// CÁLCULO PARA 2 PRODUCTOS
// ============================================================
function calcular2Productos(c1, max_r1, c2, max_r2, S_objetivo, tolerancia) {
  let mejorResultado = null;
  let menorDiferencia = Infinity;

  for (let r1 = max_r1; r1 >= 0; r1--) {
    const capital1 = c1 * (1 - r1 / 100);
    const capital2_necesario = S_objetivo - capital1;

    const r2 = Math.round((1 - capital2_necesario / c2) * 100);

    if (r2 >= 0 && r2 <= max_r2) {
      const capital2 = c2 * (1 - r2 / 100);
      const S_obtenido = capital1 + capital2;
      const q_obtenida = S_obtenido / cuotas_global;
      const diferencia = Math.abs(q_obtenida - q_objetivo_global);

      if (diferencia < menorDiferencia) {
        menorDiferencia = diferencia;
        mejorResultado = {
          r1: r1,
          r2: r2,
          r3: null,
          S_obtenido: S_obtenido,
          q_obtenida: q_obtenida,
          diferencia: diferencia
        };
      }
    }
  }

  const dentroDeTolerancia = mejorResultado !== null && menorDiferencia <= tolerancia;
  return [mejorResultado, dentroDeTolerancia];
}

// ============================================================
// CÁLCULO PARA 3 PRODUCTOS
// ============================================================
function calcular3Productos(c1, max_r1, c2, max_r2, c3, max_r3, S_objetivo, tolerancia) {
  let mejorResultado = null;
  let menorDiferencia = Infinity;

  for (let r1 = max_r1; r1 >= 0; r1--) {
    const capital1 = c1 * (1 - r1 / 100);

    for (let r2 = max_r2; r2 >= 0; r2--) {
      const capital2 = c2 * (1 - r2 / 100);
      const capital3_necesario = S_objetivo - capital1 - capital2;

      const r3 = Math.round((1 - capital3_necesario / c3) * 100);

      if (r3 >= 0 && r3 <= max_r3) {
        const capital3 = c3 * (1 - r3 / 100);
        const S_obtenido = capital1 + capital2 + capital3;
        const q_obtenida = S_obtenido / cuotas_global;
        const diferencia = Math.abs(q_obtenida - q_objetivo_global);

        if (diferencia < menorDiferencia) {
          menorDiferencia = diferencia;
          mejorResultado = {
            r1: r1,
            r2: r2,
            r3: r3,
            S_obtenido: S_obtenido,
            q_obtenida: q_obtenida,
            diferencia: diferencia
          };
        }
      }
    }
  }

  const dentroDeTolerancia = mejorResultado !== null && menorDiferencia <= tolerancia;
  return [mejorResultado, dentroDeTolerancia];
}

// ============================================================
// FUNCIÓN PRINCIPAL DE CÁLCULO
// ============================================================
function calcular() {
  ocultarError();

  try {
    const cuotas = parseInt(document.getElementById("cuotas").value.replace(/\D/g, ""), 10);
    if (isNaN(cuotas) || cuotas <= 0) {
      throw new Error("La cantidad de cuotas debe ser mayor que 0.");
    }

    const q_objetivo = obtenerNumero("cuotaObjetivo");
    const tolerancia = obtenerNumero("tolerancia");

    if (q_objetivo <= 0) {
      throw new Error("La cuota objetivo debe ser mayor que 0.");
    }

    const c1 = obtenerNumero("c1");
    const max_r1 = obtenerNumero("r1");
    const c2 = obtenerNumero("c2");
    const max_r2 = obtenerNumero("r2");

    if (c1 <= 0 || c2 <= 0) {
      throw new Error("Los capitales deben ser mayores que 0.");
    }

    cuotas_global = cuotas;
    q_objetivo_global = q_objetivo;
    tolerancia_global = tolerancia;

    const S_objetivo = q_objetivo * cuotas;
    let resultado = null;
    let encontrado = false;

    if (numProductosSelect.value === "2") {
      [resultado, encontrado] = calcular2Productos(c1, max_r1, c2, max_r2, S_objetivo, tolerancia);
    } else {
      const c3 = obtenerNumero("c3");
      const max_r3 = obtenerNumero("r3");

      if (c3 <= 0) {
        throw new Error("El capital 3 debe ser mayor que 0.");
      }

      [resultado, encontrado] = calcular3Productos(c1, max_r1, c2, max_r2, c3, max_r3, S_objetivo, tolerancia);
    }

    mostrarResultado(resultado, encontrado);

  } catch (err) {
    mostrarError(err.message);
  }
}

// ============================================================
// MOSTRAR RESULTADO EN PANTALLA
// ============================================================
function mostrarResultado(resultado, encontrado) {
  placeholderResult.classList.add("hidden");
  resultContent.classList.remove("hidden");

  if (!resultado) {
    statusBanner.className = "status-banner danger";
    statusBanner.innerText = "NO SE ENCONTRÓ UNA SOLUCIÓN DENTRO DE LOS RANGOS.";
    rebajasDisplay.innerHTML = "";

    resCuotas.innerText = "-";
    resCuotaObj.innerText = "-";
    resCuotaObt.innerText = "-";
    resDifCuota.innerText = "-";
    resSObj.innerText = "-";
    resSObt.innerText = "-";
    return;
  }

  let htmlRebajas = `
    <div class="rebaja-card">
      <span>r1</span>
      <strong>${resultado.r1}%</strong>
    </div>
    <div class="rebaja-card">
      <span>r2</span>
      <strong>${resultado.r2}%</strong>
    </div>
  `;

  if (resultado.r3 !== null) {
    htmlRebajas += `
      <div class="rebaja-card">
        <span>r3</span>
        <strong>${resultado.r3}%</strong>
      </div>
    `;
  }
  rebajasDisplay.innerHTML = htmlRebajas;

  const S_objetivo = q_objetivo_global * cuotas_global;

  resCuotas.innerText = cuotas_global;
  resCuotaObj.innerText = formatoMoneda(q_objetivo_global);
  resCuotaObt.innerText = formatoMoneda(resultado.q_obtenida);
  resDifCuota.innerText = formatoMoneda(resultado.diferencia);
  resSObj.innerText = formatoMoneda(S_objetivo);
  resSObt.innerText = formatoMoneda(resultado.S_obtenido);

  if (encontrado) {
    statusBanner.className = "status-banner success";
    statusBanner.innerText = `✓ SOLUCIÓN ENCONTRADA (Dentro de la tolerancia de ${formatoMoneda(tolerancia_global)})`;
  } else {
    statusBanner.className = "status-banner warning";
    statusBanner.innerText = `⚠ SOLUCIÓN MÁS CERCANA (Fuera de la tolerancia de ${formatoMoneda(tolerancia_global)})`;
  }
}