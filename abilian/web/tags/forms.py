# coding=utf-8
"""
"""
from __future__ import absolute_import

from wtforms.fields import StringField
from flask import current_app

from abilian.core.models.tag import Tag
from abilian.web.forms import Field, ModelForm
from abilian.web.forms.widgets import Select2, ListWidget
from abilian.web.forms.validators import required
from abilian.web.forms.filters import strip


class TagsField(Field):
  """
  Handle tags selection on for a given :attr:`tags namespace<.Tag.ns>`.

  Usage::

      __tags__ = TagsField(ns='tags namespace')

  """
  multiple = True
  widget = Select2(js_init='tags-select', multiple=True)
  view_widget = ListWidget()

  def __init__(self, ns, *args, **kwargs):
    kwargs.setdefault('view_widget', self.view_widget)
    super(TagsField, self).__init__(*args, **kwargs)
    self.ns = ns.strip()
    assert self.ns

  def iter_choices(self):
    choices = []
    extension = current_app.extensions['tags']
    ns_tags = extension.get(ns=self.ns)

    for tag in ns_tags:
      choices.append((tag.label, tag.label, tag in self.data))

    # in case of error during form validation, don't forget new added tags
    for tag in self.data - set(ns_tags):
      choices.append((tag.label, tag.label, True))

    return sorted(choices)


  def default(self):
    return set()

  def process_formdata(self, valuelist):
    extension = current_app.extensions['tags']
    valuelist = set(valuelist[0].split(u';'))
    data = set()

    for label in valuelist:
      tag = extension.get(ns=self.ns, label=label)
      if tag is None:
        tag = Tag(ns=self.ns, label=label)
      data.add(tag)

    self.data = data

  def populate_obj(self, obj, name):
    extension = current_app.extensions['tags']
    all_tags = extension.entity_tags(obj)
    to_remove = all_tags - self.data

    for tag in to_remove:
      all_tags.remove(tag)

    for tag in self.data:
      all_tags.add(tag)


class TagForm(ModelForm):
  """
  Form for a single tag
  """
  ns = StringField(u'Namespace',
                   validators=[required()],
                   filters=(strip,),
  )

  label = StringField(u'Label', filters=(strip,), validators=[required(),])

  class Meta:
    model = Tag
    include_primary_keys = True
    assign_required = False # for 'id': allow None, for new records
