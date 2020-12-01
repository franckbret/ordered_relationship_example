import pytest


class TestTodoList:
    """ Test python api on AnyBlok models"""

    def test_insert_without_position(self, rollback_registry):
        registry = rollback_registry

        personal = registry.TodoList.insert(name="personal")
        assert personal.todo_items.ordering_attr == "position"

        item1 = registry.TodoItem.insert(todo_list=personal, name="buy milk")
        assert item1.position == 0

        item2 = registry.TodoItem.insert(todo_list=personal, name="buy water")
        assert item2.position == 1

        assert len(personal.todo_items) == 2

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
        first = personal.todo_items.pop(0)
        personal.todo_items.append(first)

        assert personal.todo_items == [item2, item1]
        assert personal.todo_items[0] == item2
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

        registry.flush()
        personal.refresh()

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
        assert personal.todo_items[0].position == 1
        personal.todo_items.reorder()
        assert personal.todo_items[0].position == 0
        assert personal.todo_items[0] == item2


class TestSurvey:
    """ Test python api on AnyBlok models"""

    def test_insert(self, rollback_registry):
        registry = rollback_registry
        survey = registry.Survey.insert(name="first")

        assert survey.questions.ordering_attr == "position"

        q1 = registry.Question.insert(
            name="one", survey_id=survey.id, position=0
        )

        q2 = registry.Question.insert(name="two")
        survey.questions.append(q2)
        registry.flush()

        q3 = registry.Question.insert(name="three", survey_id=survey.id)

        expected = [q1, q2, q3]

        survey.refresh()
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
        t2 = registry.Track.insert(name="two")
        registry.PlaylistTrack.insert(playlist_id=playlist.id, track_id=t1.id)
        registry.flush()
        playlist.refresh()

        # insert = call __init__ + add in session + flush of the object
        # (only if insert is not overwrite)
        playlist.tracks.append(registry.PlaylistTrack(track_id=t2.id))
        # flush after append because playlist_id is filled by one2many and
        # added in the session. flush is also call before commit
        registry.flush()

        assert len(playlist.tracks) == 2
        assert playlist.tracks.track_id == [t1.id, t2.id]


class TestEvent:
    """ Test python api on AnyBlok models"""

    def test_insert(self, rollback_registry):
        registry = rollback_registry
        event = registry.Event.insert(name="first")

        assert event.guests.ordering_attr == "position"

        guest1 = registry.Guest.insert(name="guest1")
        guest2 = registry.Guest.insert(name="guest2")
        guest3 = registry.Guest.insert(name="guest3")
        event.guests.append(guest1)
        event.guests.append(guest2)
        event.guests.append(guest3)

        registry.flush()
        event.refresh()
        assert len(event.guests) == 3


class TestPersonAddresses:
    """ Test python api on AnyBlok models"""

    def test_insert_without_position(self, rollback_registry):
        registry = rollback_registry

        address3 = registry.Address.insert(city="Paris 3")
        address1 = registry.Address.insert(city="Paris 1")
        address4 = registry.Address.insert(city="Paris 4")
        address2 = registry.Address.insert(city="Paris 2")

        person3 = registry.Person.insert(name="test 3")
        person1 = registry.Person.insert(name="test 1")
        person4 = registry.Person.insert(name="test 4")
        person2 = registry.Person.insert(name="test 2")

        person3.addresses.append(address3)
        person1.addresses.append(address1)
        person4.addresses.append(address4)
        person2.addresses.append(address2)

        person1.addresses.append(address4)
        person1.addresses.append(address2)

        address1.persons.append(person4)

        registry.flush()

        assert address1.persons.ordering_attr == "name"
        assert person1.addresses.ordering_attr == "city"

        assert address1.persons == [person1, person4]
        assert address2.persons == [person1, person2]
        assert address3.persons == [person3]
        assert address4.persons == [person1, person4]

        person1.refresh()
        assert person1.addresses == [address1, address2, address4]
        assert person2.addresses == [address2]
        assert person3.addresses == [address3]
        person4.refresh()
        assert person4.addresses == [address1, address4]
