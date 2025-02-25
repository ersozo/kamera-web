document.addEventListener("DOMContentLoaded", () => {
  const container = document.querySelector(".layout-container");
  const layout = document.querySelector(".layout");
  const links = document.querySelectorAll(".link");

  function adjustLinkPositions() {
    const containerRect = container.getBoundingClientRect();
    const layoutRect = layout.getBoundingClientRect();

    links.forEach((link) => {
      const percentageTop = parseFloat(link.getAttribute("data-top"));
      const percentageLeft = parseFloat(link.getAttribute("data-left"));

      const top = (layoutRect.height * percentageTop) / 100;
      const left = (layoutRect.width * percentageLeft) / 100;

      link.style.top = `${top}px`;
      link.style.left = `${left}px`;

      // Set arrow rotation based on data-direction
      const direction = parseFloat(link.getAttribute("data-direction")) || 0;
      link.style.setProperty("--arrow-rotation", `${direction}deg`);
    });
  }
  // Adjust positions on load and resize
  adjustLinkPositions();
  window.addEventListener("resize", adjustLinkPositions);
});
