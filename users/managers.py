from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    
    def email_validator(self, email):
        try:
          validate_email(email)
        except ValidationError:
            raise ValueError('有効なメールアドレスを入力してください')

    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('ユーザー名を入力してください')
        
        if not password:
            raise ValueError('パスワードを入力してください')
        
        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError('メールアドレスを入力してください')
        
        # モデルインスタンスの作成
        user = self.model(
            username=username,
            email = email,
            **extra_fields
        )
        # パスワードをハッシュ化
        user.set_password(password)
        # デフォルトで管理者権限を付与しない
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        # ユーザーを保存
        user.save()
        # user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        
        if not password:
            raise ValueError(_('Admin User: and email address is required'))

        if email:
            email = self.normalize_email(email)
            self.email_validator(email)
        else:
            raise ValueError('メールアドレスを入力してください')
        
        user = self.create_user(username,email,password,**extra_fields)

        user.save()

        return user
