$(document).ready(function() {

$(".banner-slider").owlCarousel({
    loop: true,
    margin: 10,
    nav: false,
    dots: true,
    autoplay: true,
    autoplayTimeout: 5000,
    responsive: {
      0: {
        items: 1,
      },
      600: {
        items: 1,
      },
      1000: {
        items: 1,
      },
    },
  });
  
$(".bolg-slider").owlCarousel({
  loop: true,
  margin: 15,
  nav: false,
  dots: true,
  autoplay: true,
  autoplayTimeout: 5000,
  responsive: {
    0: {
      items: 1,
    },
    576: {
      items: 2,
    },
    768: {
      items: 2,
    },
    991: {
      items: 3,
    },
    1200: {
      items: 4,
    },
  },
});
// navbar
  $('.navTrigger').click(function () {
    $(this).toggleClass('active');
    console.log("Clicked menu");
    $("#mainListDiv").toggleClass("see-list");
    $("#mainListDiv").fadeIn();

});

// on-scroll
function handleScroll() {
  if (window.scrollY > 100) {
      document.body.classList.add('on-scroll');
  } else {
      document.body.classList.remove('on-scroll');
  }
}

// Attach the scroll event listener to the window
window.addEventListener('scroll', handleScroll);

});