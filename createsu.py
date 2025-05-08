from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='superadmin').exists():
    User.objects.create_superuser('superadmin', 'superadmin@gmail.com', 'chernoyarka14forever')
    print("Суперюзер создан!")
else:
    print("Суперюзер уже существует.")
