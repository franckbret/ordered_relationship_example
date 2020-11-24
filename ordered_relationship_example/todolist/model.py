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

    def _sort_items_by_position(self):
        self.todo_items.sort(key=lambda x: getattr(x, 'position'))

    @hybrid_method
    def get_ordered_items(self):
        if not self.todo_items:
            return
        self._sort_items_by_position()
        return self.todo_items

    def __str__(self):
        return ("{self.name}").format(self=self)

    def __repr__(self):
        msg = "<TodoList: {self.name}, {self.id}>"
        return msg.format(self=self)


@Declarations.register(Model)
class TodoItem:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)
    position = Integer(label="Position", nullable=False)
    todo_list = Many2One(
        label="Todo list",
        model=Model.TodoList,
        nullable=False,
        one2many=(
            "todo_items",
            dict(
                # I understand it is sioux, it is the way to apply
                # the two argument on the One2Many, else the argument
                # is on the Many2One it is a non sens here
                order_by="ModelTodoItem.position",
                collection_class=ordering_list('position'),
            )
        )
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
    position = Integer(label="Position", nullable=False)


@Declarations.register(Model)
class Survey:
    id = Integer(primary_key=True)
    name = String(label="Name", nullable=False)
    questions = One2Many(
        label="Survey questions",
        model=Model.Question,
        # The following 2 arguments have no impact on ordering
        # order_by="ModelQuestion.position",
        # collection_class=ordering_list('position'),
    )

    def _sort_questions_by_position(self):
        self.questions.sort(key=lambda x: getattr(x, 'position'))

    @hybrid_method
    def get_ordered_questions(self):
        if not self.questions:
            return
        self._sort_questions_by_position()
        return self.questions


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
        # The following 2 arguments have no impact on ordering
        order_by="ModelPlaylistTrack.position",
        collection_class=ordering_list('position'),
      )

    def _sort_tracks_by_position(self):
        cls = self.registry.PlaylistTrack
        ordered = cls.query('track_id').filter_by(playlist_id=self.id).order_by(cls.position).all()
        tracks = [self.registry.Track.query().get(x) for x in ordered]
        return tracks

    @hybrid_method
    def get_ordered_tracks(self):
        if not self.tracks:
            return
        return self._sort_tracks_by_position()
