const marqueeWrapper = document.getElementById("marquee-wrapper");
const marqueeContent = marqueeWrapper.querySelector(".marquee-content");

// Clona o conteúdo das logos
const clone = marqueeContent.cloneNode(true);

// Adiciona a cópia ao wrapper
marqueeWrapper.appendChild(clone);