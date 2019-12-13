from django.db import models


class Pokemon(models.Model):
    """Покемон"""
    title_ru = models.CharField(max_length=200, verbose_name='название')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='название на английском')
    title_jp = models.CharField(max_length=200, blank=True, verbose_name='название на японском')
    description = models.CharField(max_length=2000, blank=True, verbose_name='описание')
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name="next_evolutions", verbose_name='эволюционирует из')
    image = models.ImageField(upload_to='pokemon_image', verbose_name='изображение')

    def __str__(self):
        return self.title_ru


class PokemonEntity(models.Model):
    """Экземляр покемона"""
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='название', related_name='pokemon_entities')
    latitude = models.FloatField(verbose_name='широта')
    longitude = models.FloatField(verbose_name='долгота')
    appeared_at = models.DateTimeField(verbose_name='появится в')
    disappeared_at = models.DateTimeField(verbose_name='пропадёт в')
    level = models.IntegerField(null=True, blank=True, verbose_name='уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='атака')
    defence = models.IntegerField(null=True, blank=True, verbose_name='защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='выносливость')
