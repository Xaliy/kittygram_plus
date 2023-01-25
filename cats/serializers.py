
from rest_framework import serializers
from djoser.serializers import UserSerializer

import datetime as dt
import webcolors


from .models import Achievement, AchievementCat, Cat, Owner, CHOICES, User


# Для обработки добавленных эндпоинтов djoser
#  использует собственные вьюсеты и сериализаторы. 
class CustomUserSerializer(UserSerializer):

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class AchievementSerializer(serializers.ModelSerializer):
    # Определите новое поле achievement_name в сериализаторе,
    # в качестве параметра передайте аргумент
    # source=<'оригинальное имя поля в модели' Achievement>.
    achievement_name = serializers.CharField(source='name')

    class Meta:
        model = Achievement
        fields = ('id', 'achievement_name')


# Урок 10 создали новый класс для окраса котиков
# Для создания собственного типа поля сериализатора нужно описать
#  класс для нового типа, который будет унаследован от serializers.Field
#  и описать в нём два метода:
# 	* def to_representation(self, value) (для чтения)
#  	* и def to_internal_value(self, data) (для записи).
# Опишем новый тип поля Hex2NameColor :
class Hex2NameColor(serializers.Field):
    # При чтении данных ничего не меняем - просто возвращаем как есть
    def to_representation(self, value):
        return value

    # При записи код цвета конвертируется в его название
    def to_internal_value(self, data):
        # Доверяй, но проверяй
        try:
            # Если имя цвета существует, то конвертируем код в название
            data = webcolors.hex_to_name(data)
        except ValueError:
            # Иначе возвращаем ошибку
            raise serializers.ValidationError('Для этого цвета нет имени')
        # Возвращаем данные в новом формате
        return data


# Изменили
# И еще изменили  - добавили  color
class CatSerializer(serializers.ModelSerializer):
    # Убрали owner = serializers.StringRelatedField(read_only=True)
    # Переопределяем поле achievements
    # achievements = AchievementSerializer(read_only=True, many=True)
    # achievements = AchievementSerializer(many=True) тут не объявлено ,
    #  что поле не обязательное и по умолчнию считаю что , required=True
    # пропишем явно, что поле не обязательно - required=False
    achievements = AchievementSerializer(many=True, required=False)
    # добавляем расчет сколько лет котику
    # С помощью поля SerializerMethodField можно модифицировать
    # существующее поле или создать новое
    age = serializers.SerializerMethodField()
    # # Новый тип поля Hex2NameColor можно присвоить полю color
    # color = Hex2NameColor()  # Вот он - наш собственный тип поля
    # Теперь поле примет только значение, упомянутое в списке CHOICES
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner',
                  'achievements', 'age')

    # содержимое поля age  будет вычисляться «на лету» в методе get_age
    # Метод, который будет вызван для поля <имя_поля>,
    # по умолчанию должен называться get_<имя_поля>
    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

# переписали метод create
    def create(self, validated_data):
        # Если в исходном запросе не было поля achievements
        if 'achievements' not in self.initial_data:
            # То создаём запись о котике без его достижений
            cat = Cat.objects.create(**validated_data)
            return cat

        # Иначе делаем следующее:
        # Уберём список достижений из словаря validated_data и сохраним его
        achievements = validated_data.pop('achievements')
        # Сначала добавляем котика в БД
        cat = Cat.objects.create(**validated_data)
        # А потом добавляем его достижения в БД
        for achievement in achievements:
            current_achievement, status = Achievement.objects.get_or_create(
                **achievement)
            # И связываем каждое достижение с этим котиком
            AchievementCat.objects.create(
                achievement=current_achievement, cat=cat)
        return cat


class OwnerSerializer(serializers.ModelSerializer):
    cats = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Owner
        fields = ('first_name', 'last_name', 'cats')


# урок 12
# Опишем для этого ещё один сериализатор только для списка
# который назовём CatListSerializer:
# если запрашивается список котиков, то необходимы только id, имя и цвет.
# так же допишем вьюху
class CatListSerializer(serializers.ModelSerializer):
    color = serializers.ChoiceField(choices=CHOICES)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color')
