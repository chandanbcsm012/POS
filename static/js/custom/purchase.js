$(document).ready(function () {
  //invoice purchase print
  var printInvoice = function () {
    var a = $(this);
    $.ajax({
      url: a.attr("data-href"),
      type: 'get',
      dataType: 'json',
      // beforeSend: function () {
      //     $(".bd-invoice-modal-lg .modal-content").html("");
      //     $(".bd-invoice-modal-lg").modal("show");
      // },
      success: function (data) {
        let bill = $(".bd-invoice-modal-lg .modal-content").html(data.invoice_template);
        let invoice = bill.find('#purchase_invoice');
        invoice.printThis({
          debug: false,
          importCSS: true,
          importStyle: false,
          printContainer: true,
          loadCSS: "../static/css/bootstrap.min.css",
          pageTitle: "Purchase Invoice",
          removeInline: false,
          printDelay: 333,
          header: "<h3>Invoice</h3>",
          footer: null,
          base: false,
          formValues: false,
          canvas: false,
          doctypeString: null,
          removeScripts: false,
          copyTagClasses: false
        });
      }
    });
  };

  $(".printThis").click(printInvoice);

  //View Payment
  let viewPayment = function () {
    let a = $(this);
    $.ajax({
      url: a.attr("data-href"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $(".bd-payment-view-modal-lg .modal-content").html("");
        $(".bd-payment-view-modal-lg").modal("show");
      },
      success: function (data) {
        $(".bd-payment-view-modal-lg .modal-content").html(data.template);
      },
    });
  };

  $(".view-payment").click(viewPayment);

  let loadPaymentForm = function () {
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
    });
  };

  $(".add-payment").click(loadPaymentForm);

  var saveForm = function () {
    $(document).find("#id_due_amount").prop('disabled', false);
    $(document).find("#id_payment_status").prop('disabled', false);
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
  $("#PaymentAdd").on("submit", "#purchasePaymentFOrm", saveForm);
});

