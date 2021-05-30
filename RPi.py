

class gpio:
  def __getattr__(self, name):
    def t(*args):
      return None
    return t

GPIO = gpio()
