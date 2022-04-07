from django.contrib import admin
from django.db.models import QuerySet
from django.http import HttpRequest

from bridge.models import Game, GameUpdator


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [
        type(f"Updator{cls.__name__}", (admin.StackedInline,), dict(model=cls))
        for cls in GameUpdator.subclasses
    ]
    actions = ["run_update"]

    @admin.action(description="Run update")
    def run_update(self, request: HttpRequest, queryset: "QuerySet[Game]") -> None:
        for game in queryset:
            updator = GameUpdator.find_by_game(game.pk)
            updator.implementation().run_update()
