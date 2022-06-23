import cm

with cm.ContextManager('My context') as f:
    print('my func')