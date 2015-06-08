$(document).ready(function(){

       //// Test **************************
         $('#test').on('click', function(e) {
          
            e.preventDefault();
            ajaxPost('/test', { 'myvar': '3' }, function(content){
                    alert('done');
            });
            
        });   
        //**************************************************

//// add to cart **************************
         $('.add_to_cart').on('click', function(e) {
            var idp = $(this).attr('data-id-product');          
            console.log(idp);
            e.preventDefault();
            ajaxGet('/add/to/cart', { 'product_id': idp }, function(content){
                   
            });
            
        });   
        //**************************************************


})
