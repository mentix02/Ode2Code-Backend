from author.models import Bookmark


def bookmark_exists(author_id, series_id, model_type='series'):
    try:
        if Bookmark.objects.filter(
                model_pk=series_id,
                author_id=author_id,
                model_type=model_type,
        ).exists():
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
