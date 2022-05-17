navWrap = document.getElementById('nav-wrap')
nav = document.getElementById('nav')
side = document.getElementById('sideBar')
nav.addEventListener('click',  () => {
    nav.classList.toggle('open')
    // if (nav.classList.contains('open')){
    //     side.style.display = 'block'
    // } else {
    //     side.style.display = 'none'
    // }
    side.classList.toggle('display')
})
side.addEventListener('click', () => {
    nav.classList.remove('open')
    side.classList.add('display')
})