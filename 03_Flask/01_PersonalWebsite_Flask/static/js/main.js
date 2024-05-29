function menu_function(){
    var btn_menu = document.getElementById("Nav_Menu");
    if (btn_menu.className === "nav_menu"){
        btn_menu.className += " responsive";
    } else{
        btn_menu.className = "nav_menu";
    }
}

var typing = new Typed(".typed_text",{
    strings : ["Programmer in the information technology and services industry. Skilled in Python, Image Processing, Machine Learning, Deep Learning, Graduated engineer from Sadjad University of Technology."],
    loop : false,
    typeSpeed : 50
})
