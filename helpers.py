import json

def encodeAction(action, data = ''):
  return (json.dumps({
    'action': action,
    'data': data
  })).encode()

def decodeAction(obj):
  data = json.loads(obj)
  return data['action'], data['data']
