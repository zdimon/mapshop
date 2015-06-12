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


        //// del from cart **************************
         $('#my_basket').on('click', '.del_product_from_cart', function(e) {
            var idp = $(this).attr('data-id');          
            console.log(idp);
            e.preventDefault();
            ajaxGet('/del/from/cart', { 'item_id': idp }, function(content){});
            
        });   
        //**************************************************



        ajaxGet('/add/to/cart', { }, function(content){
                    
            });


})
