// var updateBtns = document.getElementsByClassName('update-cart');

// for (var i = 0; i < updateBtns.length; i++) {
//     updateBtns[i].addEventListener('click', function() {
//         var productId = this.dataset.product;
//         var action = this.dataset.action;
//         console.log('productId:', productId, 'Action:', action);

//         console.log('USER: ', user);
//         if (user === 'AnonymousUser') {
//             console.log('Not logged in');
//         } else {
//             updateUserOrder(productId, action);
//         }
//     });
// }

// function updateUserOrder(productId, action) {
//     console.log('User is logged in, sending data...');
    

//     // var url = '/update_item/' //Corrected URL

//     fetch({
//         type:'POST',
//         url: '{% url "customer:cart_add" %}',
//         // method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken':csrftoken,
//         },
//         body: JSON.stringify({ 'productId': productId, 'action': action })
//     })
//     .then(function(response){
//         return response.json();
//     })
//     .then(function(data){
//         console.log('data:', data);
//         location.reload();
//     });
// }


// // document.getElementsByClassName('update-cart').addEventListener('click',function(){
// //     var productId = this.dataset.product;
// //     var xhr = new XML HttpRequest();
// //     xhr.open('POST','/customer/update_item/',true);
// //     xhr.setRequestHeader('Content-Type','application/json');
// //     xhr.send(JSON.stringify({product_id:productId}));

// //     xhr.onload = function(){
// //         if(xhr.status === 200){
// //             alert('Item added to the cart!');
// //         }else{
// //             alert('Error adding item to the cart. Please try again.');
// //         }
// //     };
// // })


// // Check if button pressed
