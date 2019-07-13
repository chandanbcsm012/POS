$(document).ready(function(){

  // $('th').addClass("font-weight-bold");
  $(':input[type="number"]').attr('min', '0');

  $('select, input, textarea').addClass('form-control');  

  $(':input[type="file"]').addClass("inputFileHidden");

  $(':input[type="number"]').css("text-align", "right");

  $(".btn-image").on("click", function(){
    $(".inputFileHidden").click();
  });

  $(".inputFileHidden").on("change", function(){
    let text = $(".inputFileHidden").val().split('\\').pop();
    $(".inputFileVisible").val(text);
  });

  $("select").addClass("selectpicker");
  
  $("select").attr({"data-style": "btn btn-link", "data-max-options": "2"});
 

  $('select').selectpicker();
 
  $("textarea").attr('rows', '2');

      // Update Butoon Active
      $("input, select, textarea").change(function () {
        $("#updatebutton").removeAttr('disabled');
      });

    let menuDropdown = $("li.active").closest('div.collapse');
    menuDropdown.addClass('show');
    // let navLink =  menuDropdown.closest('a.nav-link');
    // navLink.attr('aria-expanded','true');
    $(document).on(".btn-back", function(){
      goBack();
    });

    $(document).on(".btn-forward", function(){
      goForward();
    });

    function goBack() {
      window.history.back();
    }

    function goForward() {
      window.history.forward();
    }

    function printWindow(selector) {
      let select = $(document).find(selector);
      select.printThis();
    }
    
});