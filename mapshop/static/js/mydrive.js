$(document).ready(function(){

        $('#show_predorder_form').on('click')



        //// show order history **************************
         $('#mapshop_show_order_history').on('click', function(e) {

            ajaxGet('/cart/show', { }, function(content){
                   
            });
            
        });   
        //**************************************************




        //// show preorder form **************************
         $('#show_predorder_form').on('click', function(e) {

            $('#predorder_form').show();
    
        });   
        //**************************************************



        //// handle with preorder form **************************
         $('#mapshop_preorder_save').on('click', function(e) {

    
            var product_id = $('#mapshop_product_id').val(); 
            var phone = $('#mapshop_preorder_phone').val(); 
            var email = $('#mapshop_preorder_email').val();          
            e.preventDefault();
            ajaxGet('/preorder/save', { 'phone': phone, 'email': email, 'product_id': product_id }, function(content){
                   
            });
            
        });   
        //**************************************************



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

//// ********BIND SEARCH INPUT TO AJAX FUNC*************

$('#mapshop_search_kiosk').on('input',function(e){
    var key = $(this).val();
    var order_id = $(this).attr('data-order-id');
    if(key.length>0) {
        $("#mapshop_ajax_indicator").show();
        ajaxGet('/mapshop/search/kiosk', { 'key': key, 'order_id': order_id }, function(content){
         $("#mapshop_ajax_indicator").hide();
        }); 
    }
});

//*************************************************

//// ********BIND CLICK ON SEARCH REZULT*************

$('#mapshop_search_rezult').on('click', '.mapshop_search_rezult', function(e) {

     var kiosk_id = $(this).attr('data-kiosk-id');
     var order_id = $(this).attr('data-order-id');
     ajaxGet('/getinfo/kiosk', { 'kiosk_id': kiosk_id, 'order_id': order_id }, function(content){});


});

//*************************************************


})
