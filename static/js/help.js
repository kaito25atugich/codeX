let nav = document.getElementById('nav')
let mqNav = document.getElementById('mq-nav')
let hum = document.getElementById('hum')
let children = hum.children
let a = document.getElementsByClassName('hum-nav')
let retBtn = document.getElementById('ret-btn')

retBtn.addEventListener('click', (e) => {
    let duration = 500
    let currentY = window.pageYOffset
    let step = duration/currentY > 1 ? 20 : 120
    let timeStep = duration/currentY * step
    let intervalID = setInterval(()=> {
        currentY = window.pageYOffset
        if(currentY === 0) {
            clearInterval(intervalID)
        } else {
            scrollBy( 0, -step )
        }
    }, timeStep)
})

hum.addEventListener('click', (e) => {
    if (!hum.classList.contains('open')) {
        hum.classList.add('open')
        for (let i=0;i<children.length;i++) {
            children.item(i).setAttribute('style', 'border-bottom:solid 5px #444;')
        }
        mqNav.setAttribute('style', 'right: 0;')
    } else {
        hum.classList.remove('open')
        for (let i=0;i<children.length;i++) {
            children.item(i).setAttribute('style', 'border-bottom:solid 5px #fff;')
        }
        mqNav.setAttribute('style', 'right: -100vw;')
    }
    }, false)
if (hum.classList.contains('open')) {
    mqNav.addEventListener('click', (e) => {
        hum.classList.remove('open')
        for (let i=0;i<children.length;i++) {
            children.item(i).setAttribute('style', 'border-bottom:solid 5px #fff;')
        }
        mqNav.setAttribute('style', 'right: -100vw;')
    }, false)
}
function humNav () {
    let hum = document.getElementById('hum')
    let children = hum.children
    let mqNav = document.getElementById('mq-nav')
    hum.classList.remove('open')
    mqNav.setAttribute('style', 'right: -100vw;')
    for (let i=0;i<children.length;i++) {
        children.item(i).setAttribute('style', 'border-bottom:solid 5px #444;')
    }
}

function fixedNav () {
    let scrollY = window.pageYOffset;
    let child = document.getElementById('hum').children
    let trigger = document.getElementById('trigger')
    let triggerClientRect = trigger.getBoundingClientRect()
    let triggerY = scrollY + triggerClientRect.top
    if(scrollY > triggerY) {
        retBtn.setAttribute('style', 'bottom: 3vh;')
        for (let i=0;i <child.length;i++) {
            child.item(i).setAttribute('style','border-bottom:solid 5px #444;')
        }
    } else {
        retBtn.setAttribute('style', 'bottom: -20vh;')
        for (let i=0;i <child.length;i++) {
            child.item(i).setAttribute('style', 'border-bottom:solid 5px #fff;')
        }
    }
}
window.addEventListener('scroll', fixedNav)

let usage = document.getElementById('usage-wrapper')
let child = usage.children
let counter = usage.dataset.counter
counter = parseInt(counter, 10)
child.item(counter).setAttribute('style', 'display:block')

let rArr = document.getElementById('right-arrow')
let lArr = document.getElementById('left-arrow')
rArr.addEventListener('click', rightSlide)
lArr.addEventListener('click', leftSlide)
function rightSlide () {
    let counter = usage.dataset.counter
    counter = parseInt(counter, 10)
    if (counter < child.length - 3) {
        let num = counter + 1
        child.item(counter).setAttribute('style', 'display:none;')
        child.item(num).setAttribute('style', 'display:block;')
        usage.dataset.counter = num
    }else if (counter === child.length - 3) {
        let num = 0
        child.item(counter).setAttribute('style', 'display:none;')
        child.item(num).setAttribute('style', 'display:block;')
        usage.dataset.counter = num
    }
}
function leftSlide () {
    let counter = usage.dataset.counter
    counter = parseInt(counter, 10)
    if (counter > 0) {
        let num = counter - 1
        child.item(counter).setAttribute('style', 'display:none;')
        child.item(num).setAttribute('style', 'display:block;')
        usage.dataset.counter = num
    }else if (counter === 0) {
        let num = child.length - 3
        child.item(counter).setAttribute('style', 'display:none;')
        child.item(num).setAttribute('style', 'display:block;')
        usage.dataset.counter = num
    }
}