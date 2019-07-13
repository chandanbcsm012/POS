$(document).ready(function () {
  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-sale .modal-content").html("");
        $("#modal-sale").modal("show");
      },
      success: function (data) {
        $("#modal-sale .modal-content").html(data.html_form);
        let select = $(document).find("select");
        select.addClass("selectpicker");
        select.attr({
          "data-style": "btn btn-link"
        });
      }
    });
  };


  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#sale-table tbody").html(data.html_sale_list);
          $("#modal-sale").modal("hide");
        }
        else {
          $("#modal-sale .modal-content").html(data.html_form);
        }
      },
      error: function (data) {
        //get the status code
        if (code == 400) {
          alert("Page Not found");
        }
        if (code == 500) {
          alert('Server Internal Error');
        }
      },
    });
    return false;
  };
  /* Binding */
  // Create sale
  $(".js-create-sale").click(loadForm);
  $("#modal-sale").on("submit", ".js-sale-create-form", saveForm);
  // Update sale
  $("#sale-table").on("click", ".js-update-sale", loadForm);
  $("#modal-sale").on("submit", ".js-sale-update-form", saveForm);
  // Delete sale
  $("#sale-table").on("click", ".js-delete-sale", loadForm);
  $("#modal-sale").on("submit", ".js-sale-delete-form", saveForm);

  $("a.printThis").click(function () {

    let invoice;
    let a = $(this);
    $.ajax({
      url: a.attr("data-href"),
      type: 'get',
      dataType: 'json',
      success: function (data) {
        let bill = $(".printInvoice .modal-content").html(data.invoice_template);
        let invoice = bill.find("#sale_invoice");
        let options = {
          importCSS: false,
          loadCSS: "https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css",
          pageTitle: "Invoice",
          base: "",
        };
        invoice.printThis(options);
      },
    }
    );
  });

  $("a.add-payment").on("click", function(){
    let a = $(this);
    $.ajax({
      url: a.attr("data-href"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $(".addpayment .modal-content").html("");
        $(".addpayment").modal("show");
      },
      success: function (data) {
        $(".addpayment .modal-content").html(data.form);
        $("#id_paid_amount, #id_payemnt_method").prop('required',true);
        let dueAmountCtrl = $(document).find("#id_due_amount");
        dueAmountCtrl.prop('disabled', true);
        $(document).find("#id_payment_status").prop('disabled', true);
        $(document).find("#id_total_paid").prop('disabled', true);
        $(document).find("input, select, textarea").addClass("form-control");
        $(document).find("#id_payment_note").attr("rows", "2");
        let selectControlpayMethod = $(document).find("select#id_payemnt_method");
        
        selectControlpayMethod.attr({
          "data-max-options": 2,
          "data-style": "btn btn-link"
        });
        
        selectControlpayMethod.change(function () {
          let paymentMethod = $("#id_payemnt_method").val();
          $(".pcard, .pcheque, .pbank").addClass("d-none");
          if (paymentMethod == "card") {
            $(".pcard").removeClass("d-none");
          } else if (paymentMethod == "cheque") {
            $(".pcheque").removeClass("d-none");
          } else if (paymentMethod == "bank") {
            $(".pbank").removeClass("d-none");
          }
        });
        let paidAmountControl = $(document).find("#id_paid_amount");
        let dueAmountControl = $(document).find("#id_due_amount");
        
        let dueAmount = dueAmountControl.val().trim();
        let due = dueAmount;
        let paymentStatusControl = $(document).find("#id_payment_status");
        let payStatus = paymentStatusControl.val();
        due = parseFloat(due);
        paidAmountControl.blur(function () {
          let remainingAmount = 0;
          let paidAmount = paidAmountControl.val().trim();
          if (paidAmount != "") {
            paidAmount = parseFloat(paidAmount);
          }
          if (dueAmount != "") {
            dueAmount = parseFloat(dueAmount);
          } else {
            dueAmountControl.val(due.toFixed(2));
          }
          if (parseFloat(paidAmount) > parseFloat(due) && paidAmount != "") {
            swal("Alert", "Paid amount is greater than due amount. Please check values.", "warning");
            dueAmountControl.val(due.toFixed(2));
            paidAmountControl.val(0);
          }
          if (paidAmount < 0) {
            swal("Alert", "Paid amount  should be greater then 0 . Please check values.", "warning");
            dueAmountControl.val(due.toFixed(2));
            paidAmountControl.val(0);
          }
          else if (paidAmount >= 0 && due >= paidAmount) {
            remainingAmount = dueAmount - paidAmount;
            dueAmountControl.val(remainingAmount.toFixed(2));
          } else {
            dueAmountControl.val(due.toFixed(2));
          }

          if(dueAmountControl.val()==due){
            paymentStatusControl.val(payStatus);
          }else if(dueAmountControl.val() == "0.00"){
            paymentStatusControl.val("paid")
          }else{
            paymentStatusControl.val("partial");
          }
        });
      },
    }
    );
  });


  var saveForm = function () {
    $(document).find("#id_due_amount").prop('disabled', false);
    $(document).find("#id_payment_status").prop('disabled', false);
    let totalPaidControl = $(document).find("#id_total_paid");
    let paidAmountControl = $(document).find("#id_paid_amount");
    totalPaidControl.prop('disabled', false);
    let totalPaid = parseFloat(totalPaidControl.val());
    let paidAmount = parseFloat(paidAmountControl.val());
    totalPaidControl.val(totalPaid + paidAmount);

    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
          $("#PaymentAdd").modal("hide");
          swal("Payment", data.msg, "alert", {
            button: "Ok",
          }).then((value) => {
            location.reload(true);
          });
      }
    });
    return false;
  };
  $("#PaymentAdd").on("submit", "#salePaymentForm", saveForm);
  
  
});