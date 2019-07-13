$(document).ready(function(){

    $('#id_photo_text , #photo_button').click(function(){
        $('#selectedFile').click();
        //let product_name = $('#id_name').val();        
    });

    $('#selectedFile').change(function(){
        let image_name = $('#selectedFile').val().replace(/.*(\/|\\)/, '');
        $('#id_photo_text').val(image_name); 
    });


    

});