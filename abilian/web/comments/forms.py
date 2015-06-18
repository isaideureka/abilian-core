# coding=utf-8
"""
"""
from __future__ import absolute_import

from wtforms.fields import TextAreaField

from abilian.core.models.comment import Comment
from abilian.web.forms import Form
from abilian.web.forms.widgets import TextArea
from abilian.web.forms.validators import required
from abilian.web.forms.filters import strip


class CommentForm(Form):

  body = TextAreaField(
    validators=[required()],
    filters=(strip,),
    widget=TextArea(rows=5, resizeable='vertical'),    
  )
  
  class Meta:
    model = Comment
    include_primary_keys = True
    assign_required = False # for 'id': allow None, for new records
    
