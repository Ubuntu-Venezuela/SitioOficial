(function () {
    "use strict";

    // Navegacion: dropdowns .p-navigation__item--dropdown-toggle (comportamiento Vanilla Framework)
    var dropdownToggles = document.querySelectorAll(
        ".p-navigation__item--dropdown-toggle > .p-navigation__link"
    );

    function closeAllDropdowns(except) {
        dropdownToggles.forEach(function (toggle) {
            if (toggle === except) {
                return;
            }
            var parent = toggle.parentNode;
            var controls = document.getElementById(toggle.getAttribute("aria-controls"));
            if (parent && parent.classList.contains("is-active")) {
                parent.classList.remove("is-active");
            }
            if (controls) {
                controls.setAttribute("aria-hidden", "true");
            }
            toggle.setAttribute("aria-expanded", "false");
        });
    }

    function openDropdown(toggle) {
        var parent = toggle.parentNode;
        var controls = document.getElementById(toggle.getAttribute("aria-controls"));
        closeAllDropdowns(toggle);
        if (parent) {
            parent.classList.add("is-active");
        }
        if (controls) {
            controls.setAttribute("aria-hidden", "false");
        }
        toggle.setAttribute("aria-expanded", "true");
    }

    dropdownToggles.forEach(function (toggle) {
        var parent = toggle.parentNode;
        if (parent) {
            parent.style.position = "relative";
        }

        toggle.addEventListener("click", function (event) {
            event.preventDefault();
            event.stopPropagation();

            var isOpen =
                toggle.getAttribute("aria-expanded") === "true" ||
                (parent && parent.classList.contains("is-active"));

            if (isOpen) {
                closeAllDropdowns(toggle);
                if (parent) {
                    parent.classList.remove("is-active");
                }
                toggle.setAttribute("aria-expanded", "false");
            } else {
                openDropdown(toggle);
            }
        });

        // Apertura con hover en desktop
        if (window.matchMedia("(min-width: 620px)").matches) {
            parent.addEventListener("mouseenter", function () {
                openDropdown(toggle);
            });
            parent.addEventListener("mouseleave", function () {
                closeAllDropdowns(toggle);
            });
        }

        // Apertura por teclado (Enter / Espacio / Flechas)
        toggle.addEventListener("keydown", function (event) {
            if (event.key === "ArrowDown" && !event.shiftKey) {
                event.preventDefault();
                openDropdown(toggle);
                var controls = document.getElementById(toggle.getAttribute("aria-controls"));
                if (controls && controls.firstElementChild) {
                    controls.firstElementChild.focus();
                }
            }
        });
    });

    // Cerrar al hacer click fuera
    document.addEventListener("click", function (event) {
        var isInside = false;
        dropdownToggles.forEach(function (toggle) {
            if (toggle.parentNode && toggle.parentNode.contains(event.target)) {
                isInside = true;
            }
        });
        if (!isInside) {
            closeAllDropdowns();
        }
    });
})();