"""demo Example model, this model is goging to create table at startup
"""
from anyblok import Declarations
from anyblok.column import Integer, String
from anyblok.relationship import Many2One, One2Many, Many2Many
from anyblok.declarations import hybrid_method

from sqlalchemy.ext.orderinglist import ordering_list
from operator import itemgetter


Model = Declarations.Model


# A todolist with a many2one on todoitem


@Declarations.register(Model)
class TodoList:
    id = Integer(primary_key=True)
    name = String(label="Name", unique=True, nullable=False)


@Declarations.register(Model)
class TodoItem:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)
    position = Integer(label="Position", nullable=False)
    todo_list = Many2One(
        label="Todo list",
        model=Model.TodoList,
        nullable=False,
        foreign_key_options={"ondelete": "cascade"},
        one2many=(
            "todo_items",
            dict(
                #  I understand it is sioux, it is the way to apply
                # the two argument on the One2Many, else the argument
                # is on the Many2One it is a non sens here
                order_by="ModelTodoItem.position",
                collection_class=ordering_list("position"),
            ),
        ),
    )

    def __str__(self):
        return ("{self.position} {self.name}").format(self=self)

    def __repr__(self):
        msg = "<TodoItem: position={self.position}, name={self.name}, id={self.id}>"
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
    position = Integer(label="Position of a track within a playlist")


@Declarations.register(Model)
class Track:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)


# I remove the table name is use less because
# when join_model is defined so the join_table argument
# is ignored and the primary join is automaticly filled
@Declarations.register(Model)
class Playlist:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)

    tracks = Many2Many(
        label="Tracks",
        model=Model.Track,
        join_model=Model.PlaylistTrack,
        local_columns="id",
        remote_columns="id",
        m2m_local_columns="playlist_id",
        m2m_remote_columns="track_id",
        order_by="ModelPlaylistTrack.position",
        collection_class=ordering_list("position"),
    )
