//neon
const setProperty = (duration) => {
    document.documentElement.style.setProperty(
        "--animation-time",
        duration + "s"
    );
};

const changeAnimationTime = () => {
    const animationDuration = Math.random();
    setProperty(animationDuration);
};

setInterval(changeAnimationTime, 1000);


//door
if (document.location.search.match(/type=embed/gi)) {
    window.parent.postMessage("resize", "*");
};

var enter = function () {
    var door = document.querySelector('#jamb');
    document.querySelector('#door').classList.add('open');
    document.querySelector('#jamb').classList.add('spread');
    setTimeout(function () {
        door.remove();
        window.location.href = "/portfolio";
    }, 100);
};