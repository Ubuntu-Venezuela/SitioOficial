---
title: "Guía de Certificados para Organizadores"
description: "Aprende cómo preparar tus plantillas SVG para generar certificados masivos automáticamente."
backgroundType: suru-topped
layout: single
---

Para que el sistema de Ubuntu Venezuela pueda generar certificados masivos en segundos (como el de tus 3,000 participantes), es vital que tu plantilla siga estos estándares técnicos.

### 1. El Formato SVG
El sistema solo procesa archivos **.svg**. Asegúrate de que las dimensiones sean las estándar para impresión (A4 o Carta).

### 2. El Campo del Nombre (ID Crítico)
El script de Python busca un objeto de texto específico para inyectar el nombre del participante. 
- En tu editor de SVG (como Inkscape), selecciona el texto donde irá el nombre.
- Abre las propiedades del objeto y asegúrate de que el **ID** sea exactamente: `tspan3951`.

### 3. La Lista de Participantes (XLS)
Debes subir un archivo Excel (.xls) con una hoja llamada **Speakers**.
- **Columna A:** ID o número correlativo.
- **Columnas B, C, D:** Partes del nombre del participante.

---

### Recursos Descargables
Aprovecha estas bases para tus propios eventos:

<div class="p-strip--light">
  <div class="row">
    <div class="col-6">
      <div class="p-card">
        <h4>Plantilla SVG Base</h4>
        <p>Modelo oficial con el ID `tspan3951` ya configurado.</p>
        <a href="/recursos/certificados/plantilla-base.svg" class="p-button--neutral" download>Descargar SVG</a>
      </div>
    </div>
    <div class="col-6">
      <div class="p-card">
        <h4>Excel de Ejemplo</h4>
        <p>Formato correcto para la lista de oradores y asistentes.</p>
        <a href="/recursos/certificados/lista-ejemplo.xls" class="p-button--neutral" download>Descargar XLS</a>
      </div>
    </div>
  </div>
</div>

---

> [!NOTE]
> Una vez que tengas ambos archivos listos, súbelos a través del **Wizard de Eventos** en el Panel Administrativo para iniciar la generación masiva.
