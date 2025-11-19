from django import forms

from global_model.model import Category, Brand, Product


class SliderForm(forms.Form):
    title = forms.CharField(
        label="Slider Title",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter Slider Title',
            }
        )
    )

    image = forms.ImageField(
        label="Slider Image",
        required=False,
        widget=forms.FileInput(
            attrs={
                'class': 'form-control mt-2',
                'accept': '.png, .jpg, .jpeg, .webp',
            }
        )
    )

    link = forms.CharField(
        label="Slider Link",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter Slider Link',
            }
        )
    )

    status = forms.ChoiceField(
        label="Slider Status",
        widget=forms.Select(
            attrs={
                'class': 'form-control mt-2',
            }
        ),
        initial='1',
        choices=[("0", "Inactive"),("1", "Active")]
    )

    description = forms.CharField(
        label="Slider Description",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': '(Optional)',
                'rows': 8,
            }
        ),
        required=False,
    )


class ProductForm(forms.Form):
    name = forms.CharField(
        label="Product Name",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter Product Name',
            }
        )
    )

    quantity = forms.IntegerField(
        label="Quantity",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter Product Quantity',
            }
        )
    )

    price = forms.IntegerField(
        label="Price",
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter Product Price',
                'step':'0.02'
            }
        )
    )

    image = forms.ImageField(
        label="Slider Image",
        widget=forms.FileInput(
            attrs={
                'class': 'form-control mt-2',
                'accept': '.png, .jpg, .jpeg, .webp',
            }
        )
    )

    brand = forms.ChoiceField(
        label="Brand",
        widget=forms.Select(
            attrs={
                'class': 'form-control mt-2',
            }
        )
    )

    category = forms.ChoiceField(
        label="Category",
        widget=forms.Select(
            attrs={
                'class': 'form-control mt-2',
            }
        )
    )

    status = forms.ChoiceField(
        label="Status",
        widget=forms.Select(
            attrs={
                'class': 'form-control mt-2',
            }
        ),
        initial='1',
        choices=[("0", "Inactive"),("1", "Active")]
    )

    description = forms.CharField(
        label="Product Description",
        widget=forms.Textarea(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': '(Optional)',
                'rows': 8,
            }
        ),
        required=False,
    )

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.strip() != "":
            is_exist= Product.objects.filter(name__iexact=name).first()
            if is_exist:
                self
                raise forms.ValidationError("Product with this name already exists.")
        return name


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # category
        categories = Category.objects.all()
        self.fields['category'].choices = [(str(c.id), c.name) for c in categories]

        # brand
        brands = Brand.objects.all()
        self.fields['brand'].choices = [(str(b.id), b.name) for b in brands]