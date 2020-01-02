class ModelSingleton:
  class __ModelSingleton:
    def __init__(self, arg):
      self.val = arg
    def __str__(self):
      return repr(self) + self.val
  instance = None
  def __init__(self, arg):
    if not ModelSingleton.instance:
      ModelSingleton.instance = ModelSingleton.__ModelSingleton(arg)
    else:
      ModelSingleton.instance.val = arg
  def __getattr__(self, name):
    return getattr(self.instance, name)