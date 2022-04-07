from typing import List, Type, Optional

from django.db import models


class Game(models.Model):
    name = models.CharField(max_length=255)


class GameUpdator(models.Model):
    subclasses: List[Type["GameUpdator"]] = []

    game = models.OneToOneField(Game, on_delete=models.CASCADE)

    def __init_subclass__(cls, **kwargs) -> None:
        cls.subclasses.append(cls)

    @classmethod
    def find_by_game(cls, game_id: int) -> Optional["GameUpdator"]:
        return cls.objects.filter(game_id=game_id).first()

    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.game}"

    def implementation(self) -> "GameUpdator":
        for impl_cls in self.subclasses:
            if impl := impl_cls.objects.filter(game_id=self.game_id).first():
                return impl
        raise Exception(f"Cannot find implementation for {self}")

    def run_update(self) -> None:
        raise NotImplementedError()


class SteamUpdator(GameUpdator):
    steam_path = models.CharField(max_length=512)

    def run_update(self) -> None:
        print(f"update steam game: {self.game}")


class FileUpdator(GameUpdator):
    path_to_file = models.CharField(max_length=512)
    run_params = models.CharField(max_length=512)

    def run_update(self) -> None:
        print(f"update game: {self.game} using file at {self.path_to_file}")
