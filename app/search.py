#!/usr/bin/env python3
"""
This module contains a search script
that searches tickets based on particular attributes
of a ticket such as the subject, issue description
"""
from flask import current_app


def add_to_index(index, model):
    """
    Add entries to a full-text index
        :param index: the index name to use
        :param model: the SQLALchemy model to search in
    """
    if not current_app.elasticsearch:
        return

    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, id=model.id, body=payload)


def remove_from_index(index, model):
    """
    delete entries from index
        :param index: the index name to use
        :param model: the SQLAlchemy model to remove from
    """
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, id=model.id)


def query_index(index, query, page, per_page):
    """

    :param index: index name for example, tickets
    :param query: text to search for
    :param page: which page to search
    :param per_page: size / range of pages to search
    :return: list of result id elements for the search results, total number of results
    """
    if not current_app.elasticsearch:
        return [], 0
    search = current_app.elasticsearch.search(
        index=index, body={'query': {'multi_match': {'query': query, 'fields': ['*']}},
                           'from': (page - 1) * per_page, 'size': per_page})

    ids = [int(hit['_id']) for hit in search['hits']['hits']]
    return ids, search['hits']['total']
