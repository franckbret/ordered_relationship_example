"""demo Example model, this model is going to create table at startup
"""
from anyblok import Declarations
from anyblok.column import Integer, String
from anyblok.relationship import Many2One, One2Many, Many2Many, ordering_list


Model = Declarations.Model

# Basic mann2many between two tables


@Declarations.register(Model)
class Address:

    id = Integer(primary_key=True)
    street = String()
    zip = String()
    city = String()


@Declarations.register(Model)
class Person:

    name = String(primary_key=True)
    addresses = Many2Many(
        model=Model.Address,
        many2many=(
            "persons",
            dict(
                order_by="ModelPerson.name",
                collection_class=ordering_list("name"),
            ),
        ),
        order_by="ModelAddress.city",
        collection_class=ordering_list("city"),
    )


# A todolist with a many2one on todoitem


@Declarations.register(Model)
class TodoList:
    id = Integer(primary_key=True)
    name = String(label="Name", unique=True, nullable=False)


@Declarations.register(Model)
class TodoItem:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)
    position = Integer(label="Position")
    todo_list = Many2One(
        label="Todo list",
        model=Model.TodoList,
        nullable=False,
        foreign_key_options={"ondelete": "cascade"},
        one2many=(
            "todo_items",
            dict(
                order_by="ModelTodoItem.position",
                collection_class=ordering_list("position"),
            ),
        ),
    )

    def __str__(self):
        return ("{self.position} {self.name}").format(self=self)

    def __repr__(self):
        msg = (
            "<TodoItem: position={self.position}, name={self.name}, "
            "id={self.id}>"
        )
        return msg.format(self=self)


# One2many on a survey model
# A survey have questions and question have only one survey
@Declarations.register(Model)
class Question:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)
    survey_id = Integer(foreign_key="Model.Survey=>id")
    position = Integer(label="Position", nullable=True)


@Declarations.register(Model)
class Survey:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)
    questions = One2Many(
        label="Survey questions",
        model=Model.Question,
        order_by="ModelQuestion.position",
        collection_class=ordering_list("position"),
    )


# Playlist with tracks


@Declarations.register(Model)
class PlaylistTrack:

    track_id = Integer(
        primary_key=True,
        autoincrement=False,
        foreign_key="Model.Track=>id",
    )
    playlist_id = Integer(
        primary_key=True,
        autoincrement=False,
        foreign_key="Model.Playlist=>id",
    )
    position = Integer(
        label="Position of a track within a playlist", primary_key=True
    )


@Declarations.register(Model)
class Track:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)


@Declarations.register(Model)
class Playlist:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)

    tracks = One2Many(
        model=Model.PlaylistTrack,
        order_by="ModelPlaylistTrack.position",
        collection_class=ordering_list("position"),
    )
    # tracks = Many2Many(
    #     model=Model.Track,
    #     join_model=Model.PlaylistTrack,
    #     order_by="ModelPlaylistTrack.position",
    #     collection_class=ordering_list("position"),
    #     #        many2many=(
    #     #            "playlists",
    #     #            dict(
    #     #                order_by="ModelPlaylistTrack.position",
    #     #                collection_class=ordering_list('position'),
    #     #            )
    #     #        ),
    # )


@Declarations.register(Declarations.Model)
class Guest:
    id = Integer(primary_key=True)
    name = String(nullable=False)

    def __repr__(self):
        return "<Guest(name={self.name!r})>".format(self=self)


@Declarations.register(Declarations.Model)
class EventGuest:
    guest = Many2One(
        model=Declarations.Model.Guest,
        primary_key=True,
        column_names="guest_id",
    )
    event = Many2One(
        model="Model.Event",
        primary_key=True,
        column_names="event_id",
    )
    position = Integer(label="Position of guest at an event")


@Declarations.register(Declarations.Model)
class Event:
    id = Integer(primary_key=True)
    name = String(nullable=False)

    guests = Many2Many(
        model=Model.Guest,
        join_model=Model.EventGuest,
        order_by="ModelEventGuest.position",
        collection_class=ordering_list("position"),
    )

    def __repr__(self):
        return "<Event(name={self.name!r}, guests={self.guests!r})>".format(
            self=self
        )
