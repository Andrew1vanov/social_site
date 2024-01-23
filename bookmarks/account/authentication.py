from django.contrib.auth.models import User

class EmailAuthBackend:
    '''Аутентификация посредством адреса электронной почты'''
    def authenticate(self, request, username = None, password = None):
        '''Извлекается пользователь с данным адресом электронной почты'''
        try:
            user = User.objects.get(email = username)
            if user.check_password(password):#проверка пароля
                return user 
            return None
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None
    
    def get_user(self, user_id):
        '''Пользователь извлекается по ID, указанному в параметре user_id'''
        try:
            return User.objects.get(pk = user_id)#pk - primary key
        except User.DoesNotExist:
            return None