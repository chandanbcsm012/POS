$(document).ready(function () {
  let formGroup = $("div.form-group");
  formGroup.addClass("label-floating");
  let label = formGroup.children("label");
  formGroup.append(`<span class="material-icons form-control-feedback d-none">clear</span>`);
  label.addClass("control-label");

  $("#id_supplier").attr({
    "data-live-search": true,
  });
  // file upload style
  $('#id_file_input_control, #id_file_input_button').click(function () {
    $('#id_document').click();
  });
  $('#id_document').change(function () {
    let fileValue = $('#id_document').val().split('\\').pop();
    $('#id_file_input_control').val(fileValue);
  });

  $("#id_total, #id_date").attr('disabled', 'disabled');


  $("#id_product_search_control").autocomplete({
    position: { my: "left top", at: "left bottom" },
    source: "/purchase/ajax/product/search",
    minLength: 1,
    open: function () {
      setTimeout(function () {
        $('.ui-autocomplete').css('z-index', 100);
      }, 0);
    },
    select: function (event, ui) {
      var product_name = ui.item.label;
      if (productNameExist(product_name)) {
        swal("Alert", "Product is allready exists.", "warning");
      } else {
        add_product(product_name);
      }
      $('#purchaseCollapseTow').addClass("show");
    },
  });

  $("#id_product_search_button").click(function () {
    $("#id_product_search_control").val("");
    $("#id_search_icon").text("search");
    $("#id_search_icon").removeClass("text-danger");
    $("#id_product_search_control").focus();
  });

  $("#id_product_search_control").on("change, keyup", function () {
    let text = $("#id_product_search_control").val();
    if (text === "") {
      $("#id_search_icon").text("search");
      $("#id_search_icon").removeClass("text-danger");
    } else {
      $("#id_search_icon").text("close");
      $("#id_search_icon").addClass("text-danger");
    }
  });

  // search product by name
  function search_product_by_name(product_name) {
    var product;
    $.ajax({
      url: '/purchase/ajax/product/',
      async: false,
      data: {
        'name': product_name
      },
      dataType: 'json',
      success: function (data) {
        var obj = JSON.parse(data);
        product = obj;
      }
    }).fail(function () {
      product = null;
    });
    return product;
  };
  var product_object_list = [];
  let product_total_amount = 0;

  // Add table row with product
  function add_product(product_name) {
    var product = search_product_by_name(product_name);
    var productPK = product[0].pk;
    product = product[0].fields;
    let product_unit_cost = parseFloat(product.cost);
    let product_unit_price = parseFloat(product.price);
    let product_quantity = parseInt(product.quantity);
    // let product_unit_cost_of_one_iteam = parseFloat(product_unit_cost / product_quantity);
    // product_unit_cost_of_one_iteam = parseFloat(product_unit_cost_of_one_iteam.toFixed(2));
    let product_amount = product_unit_cost * product_quantity;
    product_amount = parseFloat(product_amount.toFixed(2));
    //product object 
    let product_obj = {
      id: productPK,
      name: product.name,
      type: product.type,
      code: product.code,
      brand: product.brand,
      category: product.category,
      alert_quantity: parseInt(product.alert_quantity),
      cost: parseFloat(product.category),
      description: product.description,
      image: product.image,
      price: parseFloat(product.price),
      quantity: parseInt(product.quantity),
      tax_method: product.tax_method,
    };
    product_object_list.push(product_obj);
    var row = `
    <tr class="purchase_row">
      <input type="hidden" name="id" class="product-id" value="${product_obj.id}">
      <td class="text-center"> 
        <div class="img-container rounded">
          <img src="/media/${product_obj.image}" alt="product image" height="50">
        </div>
      </td>
      <td class="td_prduct_name font-weight-bold">
         ${product_obj.name}
      </td>
      <td class="td_unit_cost text-center">
        
        <input type="number" rel="tooltip" data-placement="left" title="Enter product unit price" class="col-8 purchase_unit_cost purchase_input" min="1" value="${product_unit_cost}">
      </td>
      <td class="td_quantity text-center">
        <input type="number" rel="tooltip" data-placement="left" title="Enter product quantity" class="col-5 purchase_product_quantity purchase_input" min="1" value="${product_obj.quantity}">
      </td>
      <td class="td_unit_price text-center">
       
        <input type="number" rel="tooltip" data-placement="left" title="Enter product unit price" class="col-8 purchase_unit_price purchase_input" min="1" value="${product_unit_price}">
      </td>
      <td class="td_product_amount text-center">
      <span class="product_amount text-primary font-weight-bold"> ${product_amount} </span> 
      </td>
      <td class="td-actions text-center">
        <button type="button" rel="tooltip" data-placement="left" title="Remove product" class="btn btn-link btn-danger remove_btn">
        <i class="material-icons">close</i>
        </button>
      </td>
    </tr>
    `;
    //add row in table
    $('#id_purchase_product_table').prepend(row);
    //total update
    update_total();
  }

  //purchase product price or quantity change
  $(document).on('change', '.purchase_unit_cost, .purchase_product_quantity', function () {
    let row = $(this).closest('tr');
    let unit_cost = row.find('input.purchase_unit_cost').val();
    if (unit_cost != "") {
      unit_cost = parseFloat(unit_cost);
      row.find('input.purchase_unit_cost').val(unit_cost);
    } else if (unit_cost == "") {
      unit_cost = 1.0;
      row.find('input.purchase_unit_cost').val(unit_cost);
    }
    let product_quantity = row.find('input.purchase_product_quantity').val().trim();
    if (product_quantity != "") {
      product_quantity = parseFloat(product_quantity);
      row.find('input.purchase_product_quantity').val(product_quantity);
    } else if (product_quantity == "") {
      product_quantity = 1.0;
      row.find('input.purchase_product_quantity').val(product_quantity);
    }
    if (unit_cost < 1) {
      unit_cost = 1.00;
      row.find('input.purchase_unit_cost').val(unit_cost);
    } else if (product_quantity < 1) {
      product_quantity = 1;
      row.find('input.purchase_product_quantity').val(product_quantity);
    }
    let product_amount = parseFloat(unit_cost * product_quantity).toFixed(2);

    row.find('span.product_amount').text(product_amount);
    update_total();
  });

  //purchase product row remove
  $(document).on('click', '.remove_btn', function () {
    swal({
      title: "Are you sure?",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((value) => {
      if (value) {
        let productid = $(this).closest(".product-id").val();
        $(this).closest('tr').remove();
        update_total();
      }
    });
  });

  //Check product name exist or not in purchase table
  function productNameExist(product_name) {
    var flag = false;
    $(document).find(".td_prduct_name").each(function () {
      var name = $(this).text().trim();
      if (name === product_name.trim()) {
        flag = true;
      }
    });
    return flag;
  }

  //Check product id exist or not in purchase table
  function productIdExist(id) {
    var flag = false;
    $(document).find(".product-id").each(function () {
      var pid = $(this).val().trim();
      if (id === parseInt(id)) {
        flag = true;
      }
    });
    return flag;
  }

  //set total amount in purchase product table footer
  function setTotalAmount(product_total_amount) {
    $('#id_total').val(parseFloat(product_total_amount));
  }

  //update total of all product
  function update_total() {
    let total_amount = 0;
    $(document).find(".purchase_row").each(function () {
      total_amount += parseFloat($(this).find('.product_amount').text());
    });
    $("#table_total_amount").text(parseFloat(total_amount));
    setTotalAmount(total_amount);
    update_grand_total();
  }

  //Purchase detials works start
  var taxArray = [];
  var taxArray1 = [];
  var totalTax = 0;
  let product_amount = 0;
  function update_grand_total() {
    product_amount = parseFloat($('#table_total_amount').text());
    //dicount
    let discountType = $('select#id_discount_type').val();
    let discountAmount = $('#id_discount').val().trim();
    if (discountAmount === "") {
      $('#id_discount').val(0);
      discountAmount = 0;
    }
    discountAmount = parseFloat(discountAmount);
    let totalDiscount = discountCalculate(discountType, discountAmount, product_amount);
    $('#total_discount_amount').text(totalDiscount);
    let totalPurchaseAmount = product_amount - totalDiscount;

    //tax
    $(document).find("#purchaseTaxDetails").empty();
    let taxText = $('select#id_tax option:selected').text().trim();
    totalTax = 0;
    if (taxText != "" && totalPurchaseAmount > 0) {
      let taxTemp = taxText.toLocaleLowerCase();
      let taxList = taxTemp.split("%");
      taxArray = [];
      taxArray1 = [];
      for (let i = 0; i < taxList.length - 1; i++) {
        let taxText = taxList[i].split(" ");
        let taxAmt = calculateTax(totalPurchaseAmount, parseFloat(taxText[1]));
        let taxObj = {

          name: taxText[0],
          percentage: parseFloat(taxText[1]),
          amount: taxAmt
        };
        taxArray.push(taxObj);
        taxArray1.push(`  ${taxText[0]}  ${parseFloat(taxText[1])}% of ${totalPurchaseAmount} = ${taxAmt}`);
      }
      taxArray.forEach(element => {
        totalTax = totalTax + element.amount;
        $("#purchaseTaxDetails").append(`<h6 class="tax-details">${element.name} ${element.percentage}% of ${totalPurchaseAmount} = ${element.amount}</h6>`);
      });
    }

    $('#purchaseTax').text(totalTax);
    totalPurchaseAmount = totalPurchaseAmount + totalTax;
    //shipping charge
    let shippingCharges = $('#id_shipping_charges').val().trim();
    if (shippingCharges !== "") {
      shippingCharges = parseFloat(shippingCharges);
    } else {
      shippingCharges = 0;
      $('#id_shipping_charges').val(0);
    }
    if (totalPurchaseAmount > 0 && shippingCharges > 0) {
      totalPurchaseAmount = totalPurchaseAmount + shippingCharges;
    }
    //Additional Charges
    let additionalChargeText = $("#id_additional").val().trim();
    let additionalCharge;
    if (additionalChargeText !== "") {
      additionalCharge = parseFloat(additionalChargeText);
    } else {
      additionalCharge = 0;
      $("#id_additional").val(0);
    }
    if (totalPurchaseAmount > 0 && additionalCharge > 0) {
      totalPurchaseAmount = totalPurchaseAmount + additionalCharge;
    }
    $('#grand_total_amount').text(totalPurchaseAmount.toFixed(2));
    //payment
    $("#payAmount").removeClass("text-rose");
    let dueAmount = totalPurchaseAmount;
    $("#payAmount").attr({
      "max": totalPurchaseAmount,
    });
    var paidAmount = $("#payAmount").val();
    if (paidAmount == "") {
      $("#payAmount").val(0);
      paidAmount = 0;
    } else if (paidAmount > 0 && paidAmount != "") {
      paidAmount = parseFloat(paidAmount);
      if (paidAmount > dueAmount) {
        swal("Alert", "Paid amount is greater than total amount.", "warning");
        $("#payAmount").addClass("text-rose");
        $("#payAmount").val(0);
      } else {
        $("#payAmount").addClass("text-primary");
        dueAmount = totalPurchaseAmount - paidAmount;
      }

    }
    $("#due_amount").removeClass("text-primary");
    if (paidAmount == 0) {
      $("#due_amount").text(dueAmount.toFixed(2));
    } else {
      $("#due_amount").addClass("text-primary");
      $("#due_amount").text(dueAmount.toFixed(2));
    }


  }
  var discountformGroup = $('#id_discount').closest("div.form-group");
  discountformGroup.hide();
  discountformGroup.val("");
  //discount type change or discount amount change or tax amount change and shipping charges
  $("#payAmount, #id_additional, #id_tax, #id_discount_type, #id_discount, #id_shipping_charges").on("change", function () {
    update_grand_total();
  });

  function discountCalculate(type, amount, totalAmount) {
    var discountformGroup = $('#id_discount').closest("div.form-group");
    var discountAmount = 0;
    if (type === 'none' || type === "") {
      discountformGroup.hide();
      discountformGroup.val("");
      return discountAmount = 0;
    }
    else if (amount == 0 || amount < 0 || amount === NaN) {
      discountformGroup.show();
      return discountAmount = 0;
    }
    discountformGroup.show();
    switch (type) {
      case "fixed":
        if (amount > totalAmount) {
          swal("Alert", "Discount amount is greater than total amount.", "warning");
          $('#id_discount').val(0);
        } else {
          discountAmount = amount;
        }
        break;
      case "%":
        if (amount > totalAmount) {
          swal("Alert", "Discount amount is greater than total amount.", "warning");
          $('#id_discount').val(0);
        } else if (amount > 100) {
          swal("Alert", "Discount % is greater than 100%.", "warning");
          $('#id_discount').val(0);
        } else {
          discountAmount = (amount * totalAmount) / 100;
        }
        break;
    }
    return discountAmount;
  }

  function calculateTax(amount, percentage) {
    var taxamount = 0;
    if (amount > 0 && percentage > 0) {
      taxamount = (percentage * amount) / 100;
    }
    return taxamount;
  }



  // https://jsfiddle.net/emkey08/tvx5e7q3
  (function ($) {
    $.fn.inputFilter = function (inputFilter) {
      return this.on("input keydown keyup mousedown mouseup select contextmenu drop", function () {
        if (inputFilter(this.value)) {
          this.oldValue = this.value;
          this.oldSelectionStart = this.selectionStart;
          this.oldSelectionEnd = this.selectionEnd;
        } else if (this.hasOwnProperty("oldValue")) {
          this.value = this.oldValue;
          this.setSelectionRange(this.oldSelectionStart, this.oldSelectionEnd);
        }
      });
    };
  }(jQuery));

  //Discount Amount, Pay Amonut
  // $("#id_discount, #payAmount, #id_shipping_charges, #id_additional, .purchase_unit_cost, .purchase_unit_price").inputFilter(function (value) {
  //   return /^-?\d*[.,]?\d{0,2}$/.test(value);
  // });


  //Payment method form
  let paymentMethod = null;
  $("#payemntMethod").change(function () {
    $(".card-control, .cheque-control, .bank-control").addClass("d-none");
    paymentMethod = $('select#payemntMethod').val().trim();
    if (paymentMethod == "card") {
      $(".card-control").removeClass("d-none");
    } else if (paymentMethod == "cheque") {
      $(".cheque-control").removeClass("d-none");
    } else if (paymentMethod == "bank") {
      $(".bank-control").removeClass("d-none");
    }
  });

  //get purchase product details
  function get_purchase_product() {
    var product_lists = [];
    $(document).find(".purchase_row").each(function () {
      let product_id = parseInt($(this).find(".product-id").val());
      let product_name = $(this).find(".td_prduct_name").text().trim();
      let purchase_unit_cost = parseFloat($(this).find(".purchase_unit_cost").val().trim());
      let purchase_product_quantity = parseInt($(this).find(".purchase_product_quantity").val().trim());
      let purchase_unit_seleing_price = parseFloat($(this).find(".purchase_unit_price").val().trim());
      let product_amount = parseFloat($(this).find(".product_amount").text().trim());

      let product_o = {
        name: product_name,
        product_id: product_id,
        unit_cost: purchase_unit_cost,
        quantity: purchase_product_quantity,
        unit_seleing_price: purchase_unit_seleing_price,
        total_cost: product_amount
      };
      product_lists.push(product_o);
    });
    return product_lists;
  }



  function getTaxId() {
    let tax_id = $("select#id_tax").val();
    return tax_id;
  }

  //purchase save
  $(document).on("click", "#id_btn_save", function () {

    var products = get_purchase_product();
    
    //purchase value get
    let supplier = $("#id_supplier").val().trim();
    let referance_no = $("#id_referance_no").val().trim();
    let date = $("#initial-id_date").val().trim();
    let status = $("#id_purchase_status").val().trim();
    let location = $("#id_location").val().trim();
    let document = $("#id_document").val();
    let net_amount = $("#table_total_amount").text().trim();

    net_amount = parseFloat(net_amount);
    console.log("net amount = " + net_amount);
    let discount_type = $("#id_discount_type").val().trim();
    let discount_value = $("#id_discount").val().trim();
    if (discount_value != "") {
      discount_value = parseFloat(discount_value);
    } else {
      discount_value = 0;
    }
    let discount_amount = $("#total_discount_amount").text().trim();
    discount_amount = parseFloat(discount_amount);

    var tax = taxArray;
    let shipping_details = $("#id_shipping_details").val().trim();
    let shipping_charges = $("#id_shipping_charges").val().trim();
    if (shipping_charges != "") {
      shipping_charges = parseFloat(shipping_charges);
      shipping_charges = shipping_charges.toFixed(2);
    } else {
      shipping_charges = 0;
    }
    let additional_charges = $("#id_additional").val().trim();
    if (additional_charges != "") {
      additional_charges = parseFloat(additional_charges);
      additional_charges = additional_charges.toFixed(2);
    } else {
      additional_charges = 0;
    }
    let total_purchase_amount = $("#grand_total_amount").text().trim();
    if (total_purchase_amount != "") {
      total_purchase_amount = parseFloat(total_purchase_amount);
    }

    taxArray1 = taxArray1.toString();
    //purchase object
    let purchases_obj = {
      supplier_id: supplier,
      referance_no: referance_no,
      date: date,
      purchase_status: status,
      location: location,
      document: document,
      net_amount: net_amount,
      discount_type: discount_type,
      discount: discount_value,
      discount_amount: discount_amount,
      tax_total: totalTax,
      shipping_details: shipping_details,
      shipping_charges: shipping_charges,
      additional: additional_charges,
      total_purchase_amount: total_purchase_amount,
      tax_details: taxArray1
    };
    
    let pay_amount = $("#payAmount").val().trim();
    if (pay_amount != "") {
      pay_amount = parseFloat(pay_amount);
      pay_amount = pay_amount.toFixed(2);
    } else {
      pay_amount = 0;
    }
    let payemnt_method = $("#payemntMethod").val().trim();

    //card
    let card_no = $("#id_card_no").val().trim();
    let card_holder_name = $("#id_card_holder_name").val();
    let card_transaction_no = $("#id_card_transaction_no").val().trim();
    let cad_type = $("#id_card_type").val().trim();
    let card_month = parseInt($("#id_card_month").val().trim());
    if (Number.isNaN(card_month)) {
      card_month = 0;
    }
    let card_year = parseInt($("#id_card_year").val().trim());
    if (Number.isNaN(card_year)) {
      card_year = 0;
    }
    let card_sec_code = parseInt($("#id_card_security_code").val().trim())
    if (Number.isNaN(card_sec_code)) {
      card_sec_code = 0;
    }
    //cheque
    let cheque_no = $("#id_cheque").val().trim();
    //bank
    let bank_account = $("#id_cheque").val().trim();
    let payment_note = $("#id_payment_note").val().trim();
    let due_amount = $("#due_amount").text().trim();

    //csrf token
    const csrf_token = $("[name=csrfmiddlewaretoken]").val();
    let tax_id = getTaxId();

    var p_status = "due";
    if (total_purchase_amount != 0) {
      if (pay_amount == total_purchase_amount) {
        p_status = "paid";
      } else if (pay_amount != 0) {
        p_status = "partial";
      } else {
        p_status = "due";
      }
    }

    let payemnt_obj = {
      paid_amount: pay_amount,
      payemnt_method: payemnt_method,
      card_no: card_no,
      card_holder_name: card_holder_name,
      card_transaction_no: card_transaction_no,
      cad_type: cad_type,
      card_month: card_month,
      card_year: card_year,
      cvv: card_sec_code,
      cheque_no: cheque_no,
      bank_account: bank_account,
      payment_note: payment_note,
      due_amount: due_amount,
      payment_status: p_status
    };

    let a = "csrfmiddlewaretoken: csrf_token";
    purchases_obj = JSON.stringify(purchases_obj);
    products = JSON.stringify(products);
    tax_id = JSON.stringify(tax_id);
    payemnt_obj = JSON.stringify(payemnt_obj);
    console.log(purchases_obj);
    $.post(
      "/purchase/",
      {
        purchases_obj,
        payemnt_obj,
        products,
        tax_id,
        csrfmiddlewaretoken: csrf_token
      },
      function (data, status) {
        console.log(window.location);
        console.log(window.location.hostname);
        if (data == "success") {
          swal("Good job!", `Your purchase is saved ${data}.`, "success", {
            button: "Ok",
          }).then((value) => {
            window.location = `${window.location.href}list`;
          });
        }
      });
  });

  $("#update_btn").click(function () {
    let products = get_purchase_product();
    let purchase_obj = getPurchaseObject();
    purchase_obj.purchase__id = parseInt($("#purchase_id").val());
    let tax_id = getTaxId();
    const csrf_token = $("[name=csrfmiddlewaretoken]").val();
    purchase_obj = JSON.stringify(purchase_obj);
    products = JSON.stringify(products);
    tax_id = JSON.stringify(tax_id);
    let url = $(location).attr("href");
    $.post(
      url,
      {
        purchase: purchase_obj,
        products: products,
        tax__id: tax_id, 
        csrfmiddlewaretoken: csrf_token
      },
      function (data, status) {
        console.log(data);
      }
    );
    console.log(url);
  });
});