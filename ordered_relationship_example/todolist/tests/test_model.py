import pytest
from pprint import pprint as pp


class TestTodoList:
    """ Test python api on AnyBlok models"""

    def test_create_todolist(self, rollback_registry):
        registry = rollback_registry
        personal = registry.TodoList.insert(name="personal")

        assert registry.TodoList.query().count() == 1
        assert personal.name == "personal"

        item1 = registry.TodoItem.insert(todo_list=personal, name="buy milk", position=0)
        item2 = registry.TodoItem.insert(todo_list=personal, name="buy cheese", position=1)
        item3 = registry.TodoItem.insert(todo_list=personal, name="buy eggs", position=2)

        assert len(personal.todo_items) == 3

        # This one works because position value is the same as insert order
        for i, item in enumerate(personal.todo_items):
            assert item.position == i


    def test_create_todolist_unordered_positions(self, rollback_registry):
        registry = rollback_registry
        personal = registry.TodoList.insert(name="personal")

        assert registry.TodoList.query().count() == 1
        assert personal.name == "personal"

        item1 = registry.TodoItem.insert(todo_list=personal, name="buy milk", position=1)
        item2 = registry.TodoItem.insert(todo_list=personal, name="buy cheese", position=0)
        item3 = registry.TodoItem.insert(todo_list=personal, name="buy eggs", position=2)

        assert len(personal.todo_items) == 3

        # This one obviously fail because position value is the not the same as insert order
        expected = [item2, item1, item3]

        with pytest.raises(AssertionError):
            assert personal.todo_items == expected

        # but should be ok using a dedicated sort function on todolist
        ordered = personal.get_ordered_items()

        assert expected == ordered

        for i, item in enumerate(ordered):
            assert item.position == i


class TestSurvey:
    """ Test python api on AnyBlok models"""

    def test_create_survey(self, rollback_registry):
        registry = rollback_registry
        survey = registry.Survey.insert(name="first")

        assert registry.Survey.query().count() == 1
        assert survey.name == "first"

        q1 = registry.Question.insert(name="one", position=0)
        q2 = registry.Question.insert(name="two", position=1)
        q3 = registry.Question.insert(name="three", position=2)

        # here we add children (questions) through parent object (survey)
        survey.questions.clear()
        survey.questions.extend([q2, q3, q1])

        assert len(survey.questions) == 3

        expected = [q1, q2, q3]
        with pytest.raises(AssertionError):
            assert survey.questions == expected

        ordered = survey.get_ordered_questions()

        assert expected == ordered

        for i, item in enumerate(ordered):
            assert item.position == i


class TestPlaylist:
    """ Test python api on AnyBlok models"""

    def test_playlist_insert_unordered_track_without_position(self, rollback_registry):
        registry = rollback_registry
        playlist = registry.Playlist.insert(name="first")

        t2 = registry.Track.insert(name="two")
        t3 = registry.Track.insert(name="three")
        t1 = registry.Track.insert(name="one")

        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t3.id)
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t1.id)
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t2.id)

        expected = [t1, t2, t3]
        # seems logic that those one fail
        with pytest.raises(AssertionError):
            assert playlist.tracks == expected

        with pytest.raises(AssertionError):
            assert playlist.get_ordered_tracks() == expected

    def test_playlist_insert_unordered_track_with_position(self, rollback_registry):
        registry = rollback_registry
        playlist = registry.Playlist.insert(name="first")

        t2 = registry.Track.insert(name="two")
        t3 = registry.Track.insert(name="three")
        t1 = registry.Track.insert(name="one")

        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t3.id, position=2)
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t1.id, position=0)
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t2.id, position=1)

        expected = [t1, t2, t3]
        
        # this one should fail ??? Does it maeans adding order_by clause on many2many definition
        # works ?
        assert playlist.tracks == expected
        # this one should pass
        assert playlist.get_ordered_tracks() == expected

    def test_playlist_insert_unordered_track_with_position(self, rollback_registry):
        registry = rollback_registry
        playlist = registry.Playlist.insert(name="first")

        t2 = registry.Track.insert(name="two")
        t3 = registry.Track.insert(name="three")
        t1 = registry.Track.insert(name="one")

        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t3.id, position=2)
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t1.id, position=0)
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t2.id, position=1)

        expected = [t1, t2, t3]
        
        # this one should fail ??? Does it maeans adding order_by clause on many2many definition
        # works ?
        assert playlist.tracks == expected
        # this one should pass
        assert playlist.get_ordered_tracks() == expected
