# forms/user.py
# 表单处理使用了 Flask-WTF ，各个表单类只需继承于 FlaskForm ，就可实现表单验证。
# 在大多数场景下都使用Flask-WTF自带的验证器完成表单验证，只有在少数情况下才要调用后台服务接口完成验证（例如验证用户名是否已存在）

from flask import current_app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import Required, Optional, Length, Email, EqualTo, DataRequired, ValidationError, NumberRange

from ..services import EbUser

from ..config import BaseConfig

base_url_user = BaseConfig.SERVICE_TBUSER['addresses'][0]


# 注册表单
class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(2, 20)])
    password = PasswordField('密码', validators=[Required(), Length(6, 20)]) ##### Todo：添加验证器，验证密码内是否包含一个以上特殊字符
    repeat_password = PasswordField(
        '重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

    # 验证用户名
    def validate_username(self, field):
        # 使用 GET 方式向后台的用户服务接口 /users 地址发送查询用户名的请求，获取返回数据
        resp = EbUser(current_app).get_json('{}/users'.format(base_url_user), params={
            'username': field.data,
        })
        # 如果存在用户数据就抛出异常
        if len(resp['data']['users']) > 0:
            raise ValidationError('用户名已经存在')

# 登录表单
class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[Required(), Length(2, 20)])
    password = PasswordField('密码', validators=[Required(), Length(6, 20)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('提交')

# 个人资料表单
class ProfileForm(FlaskForm):
    username = StringField('用户名', validators=[Length(2, 20)])
    gender = StringField('性别', validators=[Length(1, 1)])
    mobile = StringField('手机', validators=[Length(11, 11)])
    submit = SubmitField('提交')

# 头像表单
class AvatarForm(FlaskForm):
    avatar = FileField(
        validators=[FileRequired(), FileAllowed(['jpg', 'png'], '头像必须为图片')])
    submit = SubmitField('提交')

# 密码表单
class PasswordForm(FlaskForm):
    password = PasswordField('密码', validators=[Required(), Length(6, 20)])
    repeat_password = PasswordField(
        '重复密码', validators=[Required(), EqualTo('password')])
    submit = SubmitField('提交')

# 钱包表单
class WalletForm(FlaskForm):
    money = IntegerField('充值数量（元）', validators=[
                         Required(), NumberRange(1, 1000000)])
    submit = SubmitField('提交')