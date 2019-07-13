$(document).ready(function () {

  $(".needs-validation").validate({

    highlight: function (element) {
      $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
      $(element).closest('.form-group').removeClass('has-success').addClass('has-danger');
      $(element).closest('.form-check').removeClass('has-success').addClass('has-danger');
    },
    success: function (element) {
      $(element).closest('.form-group').removeClass('has-danger').addClass('has-success');
      $(element).closest('.form-check').removeClass('has-danger').addClass('has-success');
    },
    errorPlacement: function (error, element) {
      $(element).closest('.form-group').append(error);
    },
    rules: {
      first_name: {
        required: true,
        minlength: 2,
        maxlength: 15,
      },
      last_name: {
        required: true,
        minlength: 2,
        maxlength: 15,
      },
      phone: {
        number: true,
        required: true,
        minlength: 10,
        maxlength: 10,
      },
      email: {
        email: true,
        maxlength: 50,
      },
      country: {
        required: true
      },
      gst_number: {
        minlength: 15,
        maxlength: 15,
      }
    },
    opening_balance: {
      number: true,
      maxlength: 10,
      minlength: 1,
    },
   



    messages: {
      first_name: {
        required: "Please enter first name.",
        minlength: "Please enter atleast two characters.",
        maxlength: "Only 15 charaters are allowed."
      },
      last_name: {
        required: "Please enter first name.",
        minlength: "Please enter atleast two characters.",
        maxlength: "Only 15 charaters are allowed.",
      },
      phone: {
        number: "Only number is allowed",
        required: "Please enter phone number.",
        minlength: "Your mobile number is missing",
      },
      email: {
        email: "Please enter valid email address.",
        maxlength: "Only 50 charaters are allowed.",
      },
      country: {
        required: "Please select country."
      },
      gst_number: {
        minlength: "Please enter atleast 15 characters.",
        maxlength: "Only 15 charaters are allowed.",
      },
      opening_balance: {
        number: "Only number is allowed",
        maxlength: "Only 15 charaters are allowed.",
        minlength: "Please enter atleast 1 characters.",
      },
     
    }

  });
});