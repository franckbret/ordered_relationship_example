import pytest
from pprint import pprint as pp


class TestTodoList:
    """ Test python api on AnyBlok models"""

    def test_insert_without_position(self, rollback_registry):
        registry = rollback_registry

        personal = registry.TodoList.insert(name="personal")
        item1 = registry.TodoItem.insert(todo_list=personal, name="buy milk")

    def test_orderinglist(self, rollback_registry):
        registry = rollback_registry

        personal = registry.TodoList.insert(name="personal")

        assert personal.todo_items == []
        assert personal.todo_items.ordering_attr == "position"

        item1 = registry.TodoItem.insert(todo_list=personal, name="buy milk")

        assert len(personal.todo_items) == 1
        assert personal.todo_items[0] == item1
        assert personal.todo_items[0].position == 0

        item2 = registry.TodoItem.insert(todo_list=personal, name="buy cheese")

        assert len(personal.todo_items) == 2
        assert personal.todo_items[1] == item2
        assert personal.todo_items[1].position == 1

        assert personal.todo_items == [item1, item2]

        # reorder through relationship
        personal.todo_items = [item2, item1]

        assert personal.todo_items == [item2, item1]
        assert personal.todo_items[0] == item2

        with pytest.raises(AssertionError):
            assert personal.todo_items[0].position == 0

        # explicitely reorder and refresh records
        personal.todo_items.reorder()
        assert personal.todo_items[0].position == 0
        assert personal.todo_items == [item2, item1]

        # reorder through record
        item1.position = 0
        item2.position = 1
        assert item1.position == 0
        assert item2.position == 1

        with pytest.raises(AssertionError):
            assert personal.todo_items[0] == item1
            assert personal.todo_items[0].position == 0
            assert personal.todo_items[1] == item2
            assert personal.todo_items[1].position == 1

        personal.refresh()
        item1.refresh()
        item2.refresh()
        personal.todo_items.reorder()

        assert personal.todo_items[0] == item1
        assert personal.todo_items[0].position == 0
        assert personal.todo_items[1] == item2
        assert personal.todo_items[1].position == 1

        assert personal.todo_items == [item1, item2]

        # insert with position
        item3 = registry.TodoItem.insert(
            todo_list=personal, name="buy eggs", position=2
        )
        assert personal.todo_items == [item1, item2, item3]

        # delete related record
        item1.delete()
        assert registry.TodoItem.query().count() == 2
        assert personal.todo_items == [item2, item3]
        personal.todo_items.reorder()
        assert personal.todo_items[0] == item2
        assert personal.todo_items[0].position == 0

        # remove reference from related list
        personal.todo_items.remove(item3)
        assert personal.todo_items == [item2]
        assert personal.todo_items[0] == item2
        assert personal.todo_items[0].position == 0
        assert registry.TodoItem.query().count() == 1


class TestSurvey:
    """ Test python api on AnyBlok models"""

    def test_insert(self, rollback_registry):
        registry = rollback_registry
        survey = registry.Survey.insert(name="first")

        assert survey.questions.ordering_attr == "position"

        q1 = registry.Question.insert(name="one", survey_id=survey.id)
        q2 = registry.Question.insert(name="two")
        survey.questions.append(q2)
        q3 = registry.Question.insert(
            name="three", survey_id=survey.id, position=2
        )
        expected = [q1, q2, q3]

        survey.questions.reorder()

        assert len(survey.questions) == 3
        assert survey.questions == expected
        for i, question in enumerate(survey.questions):
            assert question.position == i


class TestPlaylist:
    """ Test python api on AnyBlok models"""

    def test_playlist_insert(self, rollback_registry):
        registry = rollback_registry
        playlist = registry.Playlist.insert(name="first")

        assert playlist.tracks.ordering_attr == "position"

        t1 = registry.Track.insert(name="one")
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t1.id)

        t2 = registry.Track.insert(name="two")
        playlist.tracks.append(t2)

        assert len(playlist.tracks) == 2
