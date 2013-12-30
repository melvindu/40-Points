class ModelMixin(object):
  @classmethod
  def get(cls, **kwargs):
    results = cls.query.filter(**kwargs).all()
    if len(results) > 1:
      raise ValueError('get() returned more than one result')
    elif len(results) == 1:
      return results[0]
    else:
      return None

  @classmethod
  def get_all(cls, **kwargs):
    return cls.query.filter(**kwargs).all()
  
