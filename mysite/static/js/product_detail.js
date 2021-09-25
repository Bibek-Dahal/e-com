function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");
function addToCart(obj, id, price, title) {
  //console.log('add_to_cart clicked')
  $.ajax({
    method: 'post',
    url: "http://127.0.0.1:8000/cart/add-to-cart/",
    data: {
      id: id, title: title, price: price, quantity: 1,
      csrfmiddlewaretoken: csrftoken
    },
    success: (response) => {
      obj = $('#add_to_cart').html('Go To Cart')
      obj.attr('class', 'btn btn-warning')
      obj.attr('onclick', `goToCart(${id})`)
      //console.log('{{cart_session.show_quantity}}')
      $('#cart-quan').html(response.length)



      //console.log(response)
    }
  })

}
function goToCart(id) {
  //console.log('go to cart clicked')
  //obj.getAttribute('data-pid')
  window.location.href = "http://127.0.0.1:8000/cart/cart-detail/"
}

$(".container").attr('class','d-none container mt-2');


$(window).on("load", function () {
  
  $("#spin").remove();
  $(".container").attr('class','container mt-2');
  
    $('.owl-carousel').owlCarousel({
        loop:true,
        margin:10,
        nav:true,
        dots:true,
        autoHeight:true,
        autoplay: true,
        autoplayTimeout: 3000,
        responsive:{
            0:{
                items:1
            },
            600:{
                items:1
            },
            1000:{
                items:1
            }
        }
    })
});