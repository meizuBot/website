(function() {
    let userTheme = localStorage.getItem("theme") || "light";
    let element = document.body;
    element.setAttribute("data-theme", userTheme)
  })();
  
function toggleTheme() {
    let element = document.body;
  
    let theme = localStorage.getItem("theme");
    if (theme && theme === "dark") {
        element.setAttribute("data-theme", "light")
        localStorage.setItem("theme", "light");
        console.log("Set 'theme' to 'light'")
    } 
    if (theme && theme === "light") {
        element.setAttribute("data-theme", "dark")
        localStorage.setItem("theme", "dark");
        console.log("Set 'theme' to 'dark'")
    }
  
}