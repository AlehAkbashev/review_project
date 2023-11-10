from django.db import models
from django.shortcuts import get_object_or_404


def get_model_obj(self, model: models.Model, key: str) -> models.Model or None:
    id = self.kwargs.get(key)
    return get_object_or_404(model, pk=id)
