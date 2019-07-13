from django import forms
from product.models import Product
from product_type.models import ProductType
from brand.models import Brand
from category.models import Category

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ProductForm(forms.ModelForm):

    # name = forms.CharField(widget=forms.TextInput())

    # type = forms.ModelChoiceField(
    #     queryset=Type.objects.all(),
    #     widget=forms.Select(attrs={
    #         'class': 'custom-select',
    #     }))

    # code = forms.CharField(widget=forms.TextInput(), required=False)

    # brand = forms.ModelChoiceField(
    #     queryset=Brand.objects.all(),
    #     widget=forms.Select(attrs={'class': 'custom-select'})
    # )

    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(),
    #     widget=forms.Select(attrs={'class': 'custom-select', }),
    #     required=True)

    # cost = forms.DecimalField(widget=forms.NumberInput(
    #     attrs={'min': 0}), required=False)

    # price = forms.DecimalField(widget=forms.NumberInput(
    #     attrs={'min': 0}), required=False)

    # TAX_METHOD_CHOICE = [('Exclusive', 'Exclusive'),
    #                      ('Inclusive', 'Inclusive'),
    #                      ]
    # tax_method = forms.ChoiceField(
    #     choices=TAX_METHOD_CHOICE, widget=forms.Select(), required=False)

    # quantity = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'min': 1}), required=False)
    # alert_quantity = forms.IntegerField(
    #     widget=forms.NumberInput(attrs={'min': 1}), required=False)
    # description = forms.Textarea()
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)
    #     self.helper.form_tag = False
    #     self.helper.layout = Layout(
    #         Row(
    #             Column('name', css_class='form-group col-md-4 mb-0'),
    #             Column('code', css_class='form-group col-md-4 mb-0'),
    #             Column('cost', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('type', css_class='form-group col-md-4 mb-0'),
    #             Column('brand', css_class='form-group col-md-4 mb-0'),
    #             Column('category', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(
    #             Column('price', css_class='form-group col-md-4 mb-0'),
    #             Column('quantity', css_class='form-group col-md-4 mb-0'),
    #             Column('alert_quantity', css_class='form-group col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #         Row(

    #             Column('tax_method', css_class='form-group col-md-4 mb-0'),
    #             Column('description', css_class='form-group col-md-8 mb-0'),
    #             Column('image', css_class='custom-file col-md-4 mb-0'),
    #             css_class='form-row'
    #         ),
    #     )

    class Meta:
        model = Product
        fields = '__all__'
        
        # widgets = {
        #     'description': forms.Textarea(attrs={'class':'mt-2', 'rows': 3, 'cols': 10}),
        #     'image': forms.FileInput(attrs={'class': 'custom-file-input', "accept": "image"}),
        # }
