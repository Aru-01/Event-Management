from django import forms
from events.models import Category, Event
from django.contrib.auth.models import User


class StyledFormMixin:
    default_classes = (
        "px-4 py-2 border border-gray-300 rounded-lg shadow-sm text-gray-700 "
        "bg-gradient-to-r from-white to-gray-50 hover:shadow-lg "
        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 "
        "transition duration-200 ease-in-out"
    )

    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            widget = field.widget

            if isinstance(widget, (forms.TextInput, forms.EmailInput)):
                widget.attrs.update(
                    {
                        "class": f"{self.default_classes} w-full",
                        "placeholder": f"Enter {field.label.lower()}...",
                    }
                )

            elif isinstance(widget, forms.Textarea):
                widget.attrs.update(
                    {
                        "class": f"{self.default_classes} w-full resize-none",
                        "placeholder": f"Enter {field.label.lower()}...",
                        "rows": 3,
                    }
                )

            elif isinstance(widget, forms.SelectDateWidget):
                widget.attrs.update(
                    {
                        "type": "date",
                        "class": f"{self.default_classes} bg-white",
                    }
                )

            elif isinstance(widget, forms.TimeInput):
                widget.attrs.update(
                    {
                        "type": "time",
                        "class": f"{self.default_classes} w-full bg-white",
                    }
                )

            elif isinstance(widget, forms.CheckboxSelectMultiple):
                widget.attrs.update(
                    {
                        "class": (
                            "space-y-2 p-2 bg-white border border-gray-200 rounded-md shadow-sm"
                        ),
                    }
                )


class EventModelForm(StyledFormMixin, forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Participants",
    )

    class Meta:
        model = Event
        fields = "__all__"
        widgets = {
            "date": forms.SelectDateWidget(
                empty_label=("Choose Year", "Choose Month", "Choose Day"),
            ),
            "time": forms.TimeInput(format="%H:%M", attrs={"type": "time"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].empty_label = "Select Category"
        self.apply_styled_widgets()


class CategoryForm(StyledFormMixin, forms.ModelForm):

    class Meta:
        model = Category
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
