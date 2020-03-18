from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pictures", "0008_auto_20200316_0156"),
    ]

    migration = """
        CREATE TRIGGER tagsearchupdate BEFORE INSERT OR UPDATE
        ON pictures_picture FOR EACH ROW EXECUTE PROCEDURE
        tsvector_update_trigger(indexed_tags_search, 'pg_catalog.simple', tags);

        -- Force triggers to run and populate the text_search column.
        UPDATE pictures_picture set ID = ID;
    """

    reverse_migration = """
        DROP TRIGGER tagsearchupdate ON pictures_picture;
    """

    operations = [migrations.RunSQL(migration, reverse_migration)]
