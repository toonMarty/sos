#!/usr/bin/env python3
from app import db
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)

        if total == 0:
            return cls.query.filter_by(id=0), 0

        when = {}

        for i in range(len(ids)):
            when[ids[i]] = i
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        """
        Respond to an event which will be
        triggered before a commit takes place.
        This handler is for a session that hasn't been
        committed yet, to enable taking a look and figuring out
        what objects are going to be added, modified, and deleted
        :param session: a sqlalchemy session
        :return:
        """
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        """
        Respond to an event which will be
        triggered after a commit takes place.
        when this handler is invoked, the
        session has been successfully committed, so
        changes can be made on the Elasticsearch end

        :param session: a sqlalchemy session
        :return:
        """
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)

        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)

        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        """
        refreshes an index with all the data from the relational side
        :return:
        """
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


# setting up event handlers
db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
