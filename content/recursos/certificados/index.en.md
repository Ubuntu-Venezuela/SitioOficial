---
title: "Certificate Guide for Organizers"
description: "Learn how to prepare your SVG templates to automatically generate certificates in bulk."
backgroundType: suru-topped
layout: single
---

For the Ubuntu Venezuela system to generate certificates in seconds (like for your 3,000 participants), it is vital that your template follows these technical standards.

### 1. The SVG Format
The system only processes **.svg** files. Make sure the dimensions are standard for printing (A4 or Letter).

### 2. The Name Field (Critical ID)
The Python script searches for a specific text object to inject the participant's name.
- In your SVG editor (like Inkscape), select the text where the name will go.
- Open the object properties and make sure the **ID** is exactly: `tspan3951`.

### 3. The Participant List (XLS)
You must upload an Excel file (.xls) with a sheet named **Speakers**.
- **Column A:** ID or sequential number.
- **Columns B, C, D:** Parts of the participant's name.

---

### Downloadable Resources
Use these bases for your own events:

<div class="p-strip--light">
  <div class="row">
    <div class="col-6">
      <div class="p-card">
        <h4>Base SVG Template</h4>
        <p>Official model with the `tspan3951` ID already configured.</p>
        <a href="/recursos/certificados/plantilla-base.svg" class="p-button--neutral" download>Download SVG</a>
      </div>
    </div>
    <div class="col-6">
      <div class="p-card">
        <h4>Example Excel</h4>
        <p>Correct format for the speaker and attendee list.</p>
        <a href="/recursos/certificados/lista-ejemplo.xls" class="p-button--neutral" download>Download XLS</a>
      </div>
    </div>
  </div>
</div>

---

> [!NOTE]
> Once you have both files ready, upload them through the **Event Wizard** in the Admin Panel to start bulk generation.
