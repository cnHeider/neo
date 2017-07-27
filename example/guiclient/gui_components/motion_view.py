from kivy.adapters.dictadapter import DictAdapter
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.listview import ListItemButton, ListItemLabel, \
  CompositeListItem, ListView

integers_dict = {str(i): {'text': str(i), 'is_selected': False} for i in range(100)}


class MotionView(GridLayout):
  def __init__(self, **kwargs):
    kwargs['cols'] = 2
    super(MotionView, self).__init__(**kwargs)

    args_converter = lambda row_index, row_data: {
      'text': row_data['text'],
      'size_hint_y': None,
      'height': 25,
      'cls_dicts': [
        {'cls': ListItemButton,
         'kwargs': {'text': row_data['text']}
         },
        {'cls': ListItemLabel,
         'kwargs': {'text': row_data['text'],
                    'is_representing_cls': True
          }
        },
        {'cls': ListItemLabel,
         'kwargs': {
            'text': "Middle-{0}".format(row_data['text']),
            'is_representing_cls': True
         }
        },
        {'cls': ListItemLabel,
         'kwargs': {
           'text': "End-{0}".format(row_data['text']),
           'is_representing_cls': True
         }
         },
      ]
    }

    item_strings = ["{0}".format(index) for index in range(100)]

    dict_adapter = DictAdapter(sorted_keys=item_strings,
                               data=integers_dict,
                               args_converter=args_converter,
                               selection_mode='single',
                               allow_empty_selection=False,
                               cls=CompositeListItem)

    list_view = ListView(adapter=dict_adapter)

    self.add_widget(list_view)

  def build(self):
    self.step_button = Button(text='Step')
    self.reset_button = Button(text='Reset')
    self.spacer = Label()
    self.step_button.bind(on_release=self.on_step_button)
    self.reset_button.bind(on_release=self.on_reset_button)

    self.add_widget(self.step_button)
    self.add_widget(self.reset_button)
    self.add_widget(self.spacer)
    return self

  def on_step_button(self):
    pass

  def on_reset_button(self):
    pass

if __name__ == '__main__':
  from kivy.base import runTouchApp

  runTouchApp(MotionView(width=800))
