from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Game(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='Games', verbose_name='Категория')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class UserProfile(models.Model):
    telegramID = models.BigIntegerField(verbose_name='Телеграмм ID')
    telegramUsername = models.CharField(max_length=80, verbose_name='Никнейм в Телеграмм')
    mainGame = models.ForeignKey(Game, on_delete=models.CASCADE, 
                                 related_name='UserProfiles', verbose_name='Основная игра')
    nicknameSteam = models.CharField(max_length=80, verbose_name='Никнейм в стиме')
    aboutMe = models.TextField(verbose_name='О себе')
    isActive = models.BooleanField(default=True, verbose_name='Активен')

    def __str__(self):
        return f'{self.telegramUsername} | {self.mainGame}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'