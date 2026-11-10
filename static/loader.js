function showLoader(nextPage){

    const loader = document.getElementById("loader");

    loader.style.display = "flex";

    loader.classList.add("loader-active");

    setTimeout(function(){

        window.location.href = nextPage;

    },1800);

}