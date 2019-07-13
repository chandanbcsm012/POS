$(document).ready(function () {
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

  $("#id_product_search_control").autocomplete({
    source: "/purchase/ajax/product/search",
    select: function (event, ui) {
      //console.log(ui.item.value);
      $('#salesCollapseTow').addClass("show");
      if (productNameExist(ui.item.value)) {
        swal("Alert", "Product is allready exists.", "warning");
      } else {
        addProduct(ui.item.value);
      }
    },
  });


  function addProduct(productName) {
    let product = findProductByName(productName);
    let row = `<tr class="table-row">
   <td><input type="hidden"  name="productId" value="${product[0].pk}" class="product-id"> <strong class="product-name">${product[0].fields.name}</strong></td>
   <td><input type="number" name="productQuantity" value="${product[0].fields.quantity}" class="product-quantity"></td>
   <td><input type="number" name="productprice" value="${product[0].fields.price}" class="product-price"></td>
   <td><strong class="product-subtotal">${product[0].fields.price * product[0].fields.quantity}</strong></td>
   <td><button type="button" rel="tooltip" data-placement="left" title="Remove product" class="btn btn-link btn-danger remove-btn">
   <i class="material-icons">close</i>
   </button></td>
 </tr>`;
    $('#tbl_body').prepend(row);
    update_total_product_price();
  }

  //search button
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

  //product row remove
  $(document).on('click', '.remove-btn', function () {
    swal({
      title: "Are you sure?",
      icon: "warning",
      buttons: true,
      dangerMode: true,
    }).then((value) => {
      if (value) {
        let productid = $(this).closest("product-id").val();
        $(this).closest('tr').remove();
        update_total_product_price();
      }
    });
  })

  //Check product name exist or not in purchase table
  function productNameExist(product_name) {
    var flag = false;
    $(document).find(".product-name").each(function () {
      var name = $(this).text().trim();
      if (name === product_name.trim()) {
        flag = true;
      }
    });
    return flag;
  }

  function findProductByName(productName) {
    var product;
    $.ajax({
      url: '/purchase/ajax/product/',
      async: false,
      data: {
        'name': productName
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
  }

  //purchase product price or quantity change
  $(document).on('change', '.product-quantity, .product-price', function () {
    let row = $(this).closest('tr');
    let unit_price = row.find('input.product-price').val();
    if (unit_price != "") {
      unit_price = parseFloat(unit_price);
      row.find('input.product-price').val(unit_price);
    } else if (unit_price == "") {
      unit_price = 1.0;
      row.find('input.product-price').val(unit_price);
    }
    let product_quantity = row.find('input.product-quantity').val().trim();
    if (product_quantity != "") {
      product_quantity = parseFloat(product_quantity);
      row.find('input.product-quantity').val(product_quantity);
    } else if (product_quantity == "") {
      product_quantity = 1.0;
      row.find('input.product-quantity').val(product_quantity);
    }
    if (unit_price < 1) {
      unit_price = 1.00;
      row.find('input.product-price').val(unit_price);
    } else if (product_quantity < 1) {
      product_quantity = 1;
      row.find('input.product-quantity').val(product_quantity);
    }
    let product_amount = parseFloat(unit_price * product_quantity).toFixed(2);
    row.find('.product-subtotal').text(product_amount);
    update_total_product_price();
  })


  //update total amount
  function update_total_product_price() {
    let total_amount = 0;
    $(document).find(".table-row").each(function () {
      total_amount += parseFloat($(this).find('.product-subtotal').text());
    });
    $("#table_total_amount").text(parseFloat(total_amount));
    grand_total();
  }

  //discount calculate
  function discountCalculate(type, amount, totalAmount) {
    var discount_control = $('#id_discount');
    var discountAmount = 0;
    if (type === 'none' || type === "") {
      discount_control.hide();
      discount_control.val("");
      return discountAmount = 0;
    }
    else if (amount == 0 || amount < 0 || amount === NaN) {
      discount_control.show();
      return discountAmount = 0;
    }
    discount_control.show();
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

  //calculate tax
  function calculateTax(amount, percentage) {
    var taxamount = 0;
    if (amount > 0 && percentage > 0) {
      taxamount = (percentage * amount) / 100;
    }
    return taxamount;
  }

  //change discount amount tax
  $("#id_discount_type, #id_discount, #id_tax, #id_shipping_charges, #id_paid_amount").change(function () {
    grand_total();
  });

  //update total tax , discount, grand total
  let product_total_amount = 0;
  let totalTax = 0;
  var taxArray = [];
  var taxArray1 = [];
  function grand_total() {
    product_total_amount = $("#table_total_amount").text().trim();
    if (product_total_amount != "") {
      product_total_amount = parseFloat(product_total_amount);
    }
    let discount_type = $("#id_discount_type").val();
    let discount_amount = $("#id_discount").val();
    if (discount_amount === "") {
      $('#id_discount').val(0);
      discount_amount = 0;
    }

    let total_discount_amount = discountCalculate(discount_type, discount_amount, product_total_amount);
    //console.log(total_discount_amount);
    $("#total_discount_amount").text(total_discount_amount);
    product_total_amount = product_total_amount - total_discount_amount;

    //tax
    $("#salesTaxDetails").empty();
    let taxText = $('select#id_tax option:selected').text().trim();
    totalTax = 0;
    if (taxText != "" && product_total_amount > 0) {
      let taxTemp = taxText.toLocaleLowerCase();
      let taxList = taxTemp.split("%");
      taxArray = [];
      taxArray1 = [];
      for (let i = 0; i < taxList.length - 1; i++) {
        let taxText = taxList[i].split(" ");
        let taxAmt = calculateTax(product_total_amount, parseFloat(taxText[1]));
        let taxObj = {

          name: taxText[0],
          percentage: parseFloat(taxText[1]),
          amount: taxAmt
        };
        taxArray.push(taxObj);
        taxArray1.push(`  ${taxText[0]}  ${parseFloat(taxText[1])}% of ${product_total_amount} = ${taxAmt}`);
      }
      taxArray.forEach(element => {
        totalTax = totalTax + element.amount;
        $("#salesTaxDetails").append(`<h6 class"tax-details">${element.name} ${element.percentage}% of ${product_total_amount} = ${element.amount}</h6>`);
      });
    }
    $('#salesTax').text(totalTax);
    if (product_total_amount > 0) {
      product_total_amount = product_total_amount + totalTax;
    }

    //shipping charge
    let shippingCharges = $('#id_shipping_charges').val().trim();
    if (shippingCharges !== "") {
      shippingCharges = parseFloat(shippingCharges);
    } else {
      shippingCharges = 0;
      $('#id_shipping_charges').val(0);
    }
    if (product_total_amount > 0 && shippingCharges > 0) {
      product_total_amount = product_total_amount + shippingCharges;
    }
    $("#grand_total_amount").text(product_total_amount.toFixed(2));
    //payment
    let paid_amount = parseFloat($("#id_paid_amount").val().trim());
    if (!Number.isNaN(paid_amount)) {
      if (paid_amount >= 0 && paid_amount <= product_total_amount) {
        let due_amount = product_total_amount;
        due_amount = product_total_amount - paid_amount;
        $("#due_amount").text(due_amount.toFixed(2));
      } else {
        swal("Alert", "Amount is greater.", "warning");
        $("#id_paid_amount").val(0);
      }
    }
  }

  function productFind() {
    let product_list = [];
    $(document).find(".table-row").each(function () {
      let row = $(this);
      let id = parseFloat(row.find(".product-id").val().trim());
      let name = row.find(".product-name").text().trim();
      let quantity = parseInt(row.find(".product-quantity").val());
      let price = parseFloat(row.find(".product-price").val().trim());
      let subtotal = parseFloat(row.find(".product-subtotal").text());
      let product = {
        product_id: id,
        product_name: name,
        product_quantity: quantity,
        price: price,
        subtotal: subtotal
      };
      product_list.push(product);
    });
    return product_list;
  }

  function salesObject(){
    taxArray1 = taxArray1.toString();
      let customer_id = $("#id_customer").val();
      let sale_status = $("#id_sale_status").val();
      let pay_num = parseInt($("#id_pay_num").val());
      let pay_term_option = $("#id_pay_term_option").val();
      let sale_date = $("#id_sale_date").val();
      let net_amount = parseFloat($("#table_total_amount").text());
      let discount_type = $("#id_discount_type").val();
      let discount = parseFloat($("#id_discount").val());
      let discount_amount = parseFloat($("#total_discount_amount").text());
      let tax_details = taxArray1;
      let tax_total = parseFloat($("#salesTax").text());
      let shipping_details = $("#id_shipping_details").val();
      let shipping_charges = parseFloat($("#id_shipping_charges").val());
      let sales_total = parseFloat($("#grand_total_amount").text());
      
      let sale = {
        customer_id : customer_id,
        sale_status : sale_status,
        pay_num : pay_num,
        pay_term_option : pay_term_option,
        sale_date : sale_date,
        net_amount: net_amount,
        discount_type : discount_type,
        discount : discount,
        discount_amount : discount_amount,
        tax_details : tax_details,
        tax_total : tax_total,
        shipping_details : shipping_details,
        shipping_charges : shipping_charges,
        sales_total : sales_total
      };
      return sale;
  }

  function salesPayment(){
    let paid_amount = parseFloat($("#id_paid_amount").val());
    let payemntMethod = $("#payemntMethod").val();
    let cheque = $("#id_cheque").val();
    let bank_account = $("#id_bank_account_no").val();
    let card_no = $("#id_card_no");
    let card_holder_name = $("#id_card_holder_name").val();
    let card_transaction_no = $("#id_card_transaction_no").val();
    let card_type = $("#id_card_type").val();
    let card_month = $("#id_card_month").val();
    let card_year = $("#id_card_year").val();
    let cvv = $("#id_card_security_code").val();
    let payment_note = $("#id_payment_note").val();
    let due_amount = $("#due_amount").text().trim();

    var p_status = "due";
    let sales_total = parseFloat($("#grand_total_amount").text());
    if (sales_total != 0) {
      if (paid_amount == sales_total) {
        p_status = "paid";
      } else if (paid_amount != 0) {
        p_status = "partial";
      } else {
        p_status = "due";
      }
    }

    let payment_obj = {
      paid_amount : paid_amount,
      total_paid: paid_amount,
      payemnt_method : payemntMethod,
      cheque_no : cheque,
      bank_account : bank_account,
      card_no : card_no,
      card_holder_name : card_holder_name,
      card_transaction_no : card_transaction_no,
      cad_type : card_type,
      card_month : card_month,
      card_year : card_year,
      cvv : cvv,
      payment_note : payment_note,
      due_amount: due_amount,
      payment_status: p_status,
    };
    return payment_obj;
  }
  function getTAX_ID(){
    let tax = $("#id_tax").val();
    return tax;
  }
  
  $("#id_btn_save").click(function () {
    const csrf_token = $("[name=csrfmiddlewaretoken]").val();
    let product_list = JSON.stringify(productFind());
    let sale_obj = JSON.stringify(salesObject());
    let sale_payment = JSON.stringify(salesPayment());
    let tax_id = JSON.stringify(getTAX_ID());
    console.log(product_list);
    console.log(sale_obj);
    console.log(sale_payment);
    console.log(tax_id)
    console.log(csrf_token);
    
    $.post(
      "/sale/",
      {
        sale_obj,
        sale_payment,
        product_list,
        tax_id,
        csrfmiddlewaretoken: csrf_token
      },
      function (data, status){
        console.log(window.location);
        console.log(window.location.hostname);
        if (data == "success") {
          swal("Good job!", `Your order is saved ${data}.`, "success", {
            button: "Ok",
          }).then((value) => {
            window.location = `${window.location.href}list`;
          });
        }
      });
  });

});