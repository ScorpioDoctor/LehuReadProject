from captcha.fields import CaptchaField
from django import forms

from books.models import BookNotes
from .models import UserProfile


class LoginForm(forms.Form):
    username = forms.CharField(required=True, error_messages={"required": u"用户名不能为空"})
    password = forms.CharField(required=True, min_length=5, error_messages={
        "required": u"密码不能为空", "min_length": "密码长度至少5个字符"})


class RegistForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={"required": u"邮箱不能为空"})
    captcha = CaptchaField(error_messages={"invalid": u"验证码错误"})


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UpdatePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UpdateUserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nickname', 'mobile', 'address', 'birthday', 'gender']


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image', ]


class BookNotesForm(forms.ModelForm):
    class Meta:
        model = BookNotes
        fields = "__all__"
        exclude = ['user', 'addtime', 'clicknum', 'favornum', 'commtnum']
