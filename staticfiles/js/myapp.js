const hero = document.querySelector('.banner');

const tl = new TimelineMax();

tl.fromTo(hero,1,{height: "0%"} ,{height: "80%"})