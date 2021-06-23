$(function(){
	$(".wrapper").slick({
		nextArrow: '<button class="slick-arrow slick-next"> <img src="static/main/images/arrowr.svg" alt=".!."></button>',
		prevArrow: '<button class="slick-arrow slick-prev"> <img src="static/main/images/arrowl.svg" alt=".!."></button>',
});
	if (window.matchMedia("(max-width: 736px)").matches) {
        $(".menu-item a").hover(
			function(){
				$(this).css({"color": "#fff"})
			},function(){
				$(this).css({"color": "#a6a6a6"})
			}
		);
    }
});





$(".hard__slide").slick({
	arrows: false,
	dots: true,
	draggable: false,
	swipe: false
});


$(".hard__button-slider").css("width", $('.hard1__button').css('width'));
$(".hard1__button").on("click", function(){
	$("#slick-slide-control00").click();
	$(".hnum1").addClass("active");
	$(".hnum2").removeClass("active");
	$(".hnum3").removeClass("active");
	var coeff = $('.hard1__button').css('width');
	var position = $('.hard1__button').position();
	$(".hard__button-slider").css("left", position.left).css("width", coeff);
});


$(".hard2__button").on("click", function(){
	$("#slick-slide-control01").click();
	$(".hnum2").addClass("active");
	$(".hnum1").removeClass("active");
	$(".hnum3").removeClass("active");
	var coeff = $('.hard2__button').css('width');
	var position = $('.hard2__button').position();
	$(".hard__button-slider").css("left", position.left).css("width", coeff);
});


$(".hard3__button").on("click", function(){
	$("#slick-slide-control02").click();
	$(".hnum3").addClass("active");
	$(".hnum1").removeClass("active");
	$(".hnum2").removeClass("active");
	var coeff = $('.hard3__button').css('width');
	var position = $('.hard3__button').position();
	$(".hard__button-slider").css("left", position.left).css("width", coeff);
});

