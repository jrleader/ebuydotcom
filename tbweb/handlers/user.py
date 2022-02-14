from flask import Blueprint, request, current_app, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from ..forms import RegisterForm, LoginForm, ProfileForm, AvatarForm, PasswordForm, WalletForm

from ..services import EbUser, EbFile

from ..models import User

from ..config import BaseConfig

user = Blueprint('user', __name__, url_prefix='/user')

base_url_user = BaseConfig.SERVICE_TBUSER['addresses'][0]


@user.route('/register', methods=['GET','POST'])
def register():
    '''
    注册用户
    '''

    form = RegisterForm()

    # 通过表单验证
    if form.validate_on_submit():

        print(base_url_user)
        # 向用户服务发送注册信息并获得响应
        resp = EbUser(current_app).post_json('{}/users'.format(base_url_user), json= {
            'username': form.username.data,
            'password': form.password.data
        }, check_code=False)

        # 响应不成功
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('/user/register.html', form=form, current_user=None)

        flash('注册成功，请登录', 'success')

        return redirect(url_for('.login'))

    # 输入的注册信息未通过表单验证 (包括初次访问)
    return render_template('user/register.html', form=form, current_user=None)


@user.route('/login', methods=['GET','POST'])
def login():
    '''
    登录
    '''

    form = LoginForm()

    # 输入表单的信息验证成功
    if form.validate_on_submit:
        # 向后台服务发送验证密码请求，并获得响应
        resp = EbUser(current_app).get_json('{}/users/verify'.format(base_url_user), params= { # 把URL改成从配置文件里动态获取
            'username': form.username.data,
            'password': form.password.data
        }, check_code=False)

        # 响应不成功
        if resp['code'] != 0:
            flash(resp['message'], 'danger')
            return render_template('/user/login.html', form=form, current_user=None)

        # 密码/用户名错误
        if not resp['data']['isCorrect']:
            if(form.username.data != None or form.password.data != None):
                flash('用户名或密码错误')
            return render_template('/user/login.html', form=form, current_user=None)

        # 用户登录
        # 在用户会话中将用户标记为已登录，remember_me表示是否要向用户浏览器写入cookie保存会话信息，保存用户会话
        # cookie默认保存一年，通过修改REMEMBER_COOKIE_DURATION配置项可以更改这个值
        login_user(User(resp['data']['user']), form.remember_me.data)

        print('User {} has logged in'.format(resp['data']['user']['username']))

        # 成功登录，重定向到主页
        return redirect(url_for('common.index'))
        # return render_template('index.html', current_user=User(resp['data']['user'])) 
        # werkzeug.routing.BuildError: Could not build url for endpoint 'cart_product.index'. Did you mean 'common.index' instead?

    # 输入表单的信息验证失败
    return render_template('user/login.html', form=form, current_user=None)

@user.route('/logout')
@login_required         # 必须要先登录才能登出
def logout():
    '''
    登出
    '''

    # 退出登录
    logout_user()

    flash('用户已顺利登出', 'success')

    #重定向到主页
    return redirect(url_for('common.index'))

@user.route('/profile')
@login_required         # 必须要先登录才能编辑资料
def profile():
    '''
    编辑资料
    '''
    pass


@user.route('/avatar')
@login_required     
def avatar():
    '''
    设置头像
    '''
    pass

@user.route('/password')
@login_required
def password():
    '''
    修改密码
    '''
    pass

@user.route('/wallet')
@login_required
def wallet():
    '''
    充值钱包
    '''
    pass