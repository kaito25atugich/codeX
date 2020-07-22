class DataBaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'help':
            return 'db_help'
        elif model._meta.app_label == 'kucg':
            return 'db_kucg'
        return None
 
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'help':
            return 'db_help'
        elif model._meta.app_label == 'kucg':
            return 'db_kucg'
        return None
 
    def allow_relation(self, obj1, obj2, **hints):
        return True
 
    def allow_migrate(self, db, app_label, model=None, **hints):
        if app_label == 'auth' or app_label == 'contenttypes' or app_label == 'sessions' or app_label == 'admin':
            return db == 'default'
        if app_label == 'codeX':
            return db == 'default'
        elif app_label == 'help':
            return db == 'db_help'
        elif app_label == 'kucg':
            return db == 'db_kucg'
        return None