#?shortcut=Mod1+Shift+T

import json
import os
import traceback
import urllib2
import webbrowser
from com.pnfsoftware.jeb.client.api import IScript
from com.pnfsoftware.jeb.util.net import Net
from com.pnfsoftware.jeb.core.units import IInteractiveUnit
"""
Localize strings to English. The translated string is also registered as a comment if the unit supports it.
Optionally use Google services to perform the translation.
"""
class TranslateString(IScript):
  def run(self, ctx):
    f = ctx.getFocusedFragment()
    if not f:
      return

    sel = f.getSelectedText() or f.getActiveItemAsText()
    if not sel:
      return

    print('Text: %s' % sel)
    text = sel.strip(' \'\"')

    # if you have set up a Google Cloud Engine API key, use the web Service and add the translated string as a comment
    # else, open up a browser and navigate to Google Translate

    key = os.environ.get('GCP_API_KEY')
    if not key:
      url = 'https://translate.google.com/#view=home&op=translate&sl=auto&tl=en&text=%s' % urllib2.quote(text.encode('utf8'))
      print('Query: %s' % url)
      webbrowser.open(url)
      return

    url = 'https://translation.googleapis.com/language/translate/v2?key=%s' % key
    try:
      r = Net().query(url, {'target': 'en', 'q': text})
      tt = json.loads(r)['data']['translations'][0]['translatedText']
    except Exception as e:
      traceback.print_exc(e)
      return

    print('Translation: %s' % tt)

    a = f.getActiveAddress()
    if a and isinstance(f.getUnit(), IInteractiveUnit):
      comment0 = f.getUnit().getComment(a)
      comment = tt + '\n' + comment0 if comment0 else tt
      f.getUnit().setComment(a, comment)