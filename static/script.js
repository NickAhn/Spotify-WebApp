let tabs = document.querySelectorAll(".tabs-header h3");
let tabContents = document.querySelectorAll(".tab-content div");

// Event listener: for each tab, remove "active" class and add it to the clicked tab
tabs.forEach((tab, index) => {
    tab.addEventListener("click", () => {
        tabContents.forEach((content) => {
            content.classList.remove("active");
        });

        tabs.forEach((tab) => {
            tab.classList.remove("active");
        });

        tabContents[index].classList.add("active");
        tabs[index].classList.add("active");
    });
});