function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');
const addToCart = (userId,productId) =>{
    return new Promise((resolve, reject) => {

        if(!currentUserID){
        Swal.fire({
          title: "User not logged in!",
          text: "You need to login first to add your cart!",
          icon: "warning",
          allowOutsideClick:false,
          allowEscapeKey:false
        }).then((result) => {
              if (result.isConfirmed) {
                  reject("User not logged in!")
              }
            });
            reject("User not logged in!");
            return;
        }

        $.ajax({
            url: "/api/add-to-cart",
            type: 'POST',
            headers: {'X-CSRFToken': csrftoken},
            data:{
                "productId": productId,
                "userId": userId,
            },
            dataType: 'json',
            success: function (res) {
                Swal.fire({
                  title: "Product has been add to cart successfully!",
                  icon: "success",
                  allowOutsideClick:false,
                  allowEscapeKey:false
                }).then((result) => {
                  if (result.isConfirmed) {
                      resolve(res);
                  }
                });
            },
            error: function (error) {
                reject(error);
            }
        })
    })
}