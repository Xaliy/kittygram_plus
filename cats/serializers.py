from rest_framework import serializers

from .models import Achievement, AchievementCat, Cat, Owner


class AchievementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Achievement
        fields = ('id', 'name')


# Изменили
class CatSerializer(serializers.ModelSerializer):
    # Убрали owner = serializers.StringRelatedField(read_only=True)
    # Переопределяем поле achievements
    # achievements = AchievementSerializer(read_only=True, many=True)
    # achievements = AchievementSerializer(many=True) тут не объявлено ,
    #  что поле не обязательное и по умолчнию считаю что , required=True
    # пропишем явно, что поле не обязательно - required=False
    achievements = AchievementSerializer(many=True, required=False)

    class Meta:
        model = Cat
        fields = ('id', 'name', 'color', 'birth_year', 'owner', 'achievements')

# пррепишем метод create с учетом того что поле achievements не обязательно 
# используем словарь initial_data
#     def create(self, validated_data):
#         # Уберем список достижений из словаря validated_data и сохраним его
#         achievements = validated_data.pop('achievements')

#         # Создадим нового котика пока без достижений, данных нам достаточно
#         cat = Cat.objects.create(**validated_data)

#         # Для каждого достижения из списка достижений
#         for achievement in achievements:
#             # Создадим новую запись или получим существующий экземпляр из БД
#             current_achievement, status = Achievement.objects.get_or_create(
#                 **achievement)
#             # Поместим ссылку на каждое достижение во вспомогательную таблицу
#             # Не забыв указать к какому котику оно относится
#             AchievementCat.objects.create(
#                 achievement=current_achievement, cat=cat)
#         return cat

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
