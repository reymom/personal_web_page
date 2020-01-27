let myImage = document.querySelector('img');

myImage.onclick = function() {
    let mySrc = myImage.getAttribute('src');
    if (mySrc === 'images/logo-reymon.png') {
        myImage.setAttribute('src', 'images/logo-reymon2.png');
    } else {
        myImage.setAttribute('src', 'images/logo-reymon.png');
    }
}

let myButton = document.querySelector('[name="button1"]');
let myHeading = document.querySelector('h1');

function setUserName() {
    let myName = prompt('What\'s your name? :)');
    if (!myName || myName === null) {
        setUserName();
    } else {
        localStorage.setItem('name', myName);
        myHeading.textContent = 'Customizing ' + myName + '\'s Predictions'
    }
}

if (!localStorage.getItem('name')) {
    setUserName();
} else {
    let storedName = localStorage.getItem('name');
    myHeading.textContent = 'Customizing ' + storedName + '\'s Predictions'
}

myButton.onclick = function() {
    setUserName();
}
