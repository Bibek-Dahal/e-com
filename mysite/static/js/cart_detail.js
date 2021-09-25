
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
    //console.log("add_to_cart clicked");
    //console.log("obj", obj);
}

function handleClick(obj, id, title, price) {
    //console.log("add button clicked");
    //console.log(`#${id}`);
    //console.log($(`#${id}`).html());
    //console.log("obj", obj.getAttribute("data-btn"));
    let name = obj.getAttribute("data-btn");

    if (name == "add_btn") {
        let value = $(`#${id}`).html();
        $(`#${id}`).html(parseInt(value) + 1);
        //$(`#${id}`).val(parseInt(value)+1)
        let finalVal = $(`#${id}`).html();
        ////console.log(finalVal);
        ////console.log(!isNaN(finalVal));
        if (!isNaN(finalVal) && parseInt(finalVal) <= 3) {
            ////console.log("nice");
            quantity = $(`#${id}`).html();
            $.ajax({
                method: "post",
                url: "http://127.0.0.1:8000/cart/add-to-cart/",
                data: {
                    id: id,
                    title: title,
                    price: price,
                    quantity: quantity,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: (response) => {
                    ////console.log(response);
                    ////console.log(response.data);
                    $(`.${id}`).html(`Rs${parseInt(response.data)}`);
                    $("#s_total").html(`Rs ${response.s_price}`);
                    $("#price").html(`Price(${response.length} items)`);
                    $("#total_charge").html(
                        `Rs ${response.total_charge.toFixed(2)}`
                    );
                    $("shipping_charge").html(
                        `Rs ${response.shipping_charge.toFixed(2)}`
                    );
                    $('#cart-quan').html(response.length)
                },
                error: (response) => {
                    //alert(response);
                },
            });
        } else {
            handleChange(id);
        }
    }

    if (name == "dec_btn") {
        ////console.log("dec button clicked");
        let value = $(`#${id}`).html();
        //$(`#${id}`).val(parseInt(value)-1);
        $(`#${id}`).html(parseInt(value) - 1);
        let finalVal = $(`#${id}`).html();
        ////console.log(finalVal);
        ////console.log(!isNaN(finalVal));

        if (!isNaN(finalVal) && parseInt(finalVal) >= 1) {
            ////console.log("nice");
            quantity = $(`#${id}`).html();
            $.ajax({
                method: "post",
                url: "http://127.0.0.1:8000/cart/add-to-cart/",
                data: {
                    id: id,
                    title: title,
                    price: price,
                    quantity: quantity,
                    csrfmiddlewaretoken: csrftoken,
                },
                success: (response) => {
                   // //console.log(response);
                    ////console.log(response.data);
                    $(`.${id}`).html(`Rs${parseInt(response.data)}`);
                    $("#s_total").html(`Rs ${response.s_price.toFixed(2)}`);
                    $("#price").html(`Price(${response.length} items)`);
                    $("#total_charge").html(
                        `Rs ${response.total_charge.toFixed(2)}`
                    );
                    $("shipping_charge").html(
                        `Rs ${response.shipping_charge.toFixed(2)}`
                    );
                    $('#cart-quan').html(response.length)
                },
                error: (error) => {
                    //alert(error);
                },
            });
        } else {
            handleChange(id);
        }
    }
}

function handleChange(id) {
    let value = $(`#${id}`).html();
    /*if(value.length !==0){
                        if(isNaN(value)){
                            $(`#${id}`).val(1);
                        }
                        else{
                            if(parseInt(value)>3){
                                $(`#${id}`).val(3);
                            }
                            if(parseInt(value)<1){
                                $(`#${id}`).val(1);
                            }
                        }
                    } */

    if (parseInt(value) > 3) {
        //$(`#${id}`).val(3);
        $(`#${id}`).html(3);
    }
    if (parseInt(value) < 1) {
        //$(`#${id}`).val(1);
        $(`#${id}`).html(1);
    }
}

function removeCart(id) {
    ////console.log("remove cart clicked");
    ////console.log(id);
    $.ajax({
        method: "post",
        url: "http://127.0.0.1:8000/cart/remove-cart/",
        data: {
            pk: id,
            csrfmiddlewaretoken: csrftoken,
        },

        success: (response) => {
            ////console.log(response);
            obj = $(`[data-cart-container=${response.id}]`);
            obj.remove();
            $("#s_total").html(`Rs ${response.s_price.toFixed(2)}`);
            $("#price").html(`Price(${response.length} items)`);
            $("#total_charge").html(`Rs ${response.total_charge.toFixed(2)}`);
            $("shipping_charge").html(
                `Rs ${response.shipping_charge.toFixed(2)}`
            );
            $('#cart-quan').html(response.length)

            if (parseInt(response.length) == 0) {
                ////console.log("less then 0");
                $("#cart_detail").remove();
            }
        },
    });
}