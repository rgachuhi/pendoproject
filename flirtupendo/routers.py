'''
Created on Apr 22, 2015

@author: Raphael
'''
class WorldRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to auth_db.
        """
        app_list = ('world')
        if model._meta.app_label in app_list:
            return 'default'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        app_list = ('world')
        if model._meta.app_label in app_list:
            return 'default'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        app_list = ('world')
        if obj1._meta.app_label in app_list or \
           obj2._meta.app_label in app_list:
                return True
        return None

    def allow_migrate(self, db, app_label, model=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        
        app_list = ('world')
        if app_label in app_list:
            return db == 'default'
        return None
    
class PrimaryRouter(object):
    def db_for_read(self, model, **hints):
        app_list = ('world')
        if model._meta.app_label in app_list:
            return None
        return 'primary'

    def db_for_write(self, model, **hints):
        app_list = ('world')
        if model._meta.app_label in app_list:
            return None
        return 'primary'

    def allow_relation(self, obj1, obj2, **hints):
        app_list = ('world')
        if obj1._meta.app_label in app_list or \
           obj2._meta.app_label in app_list:
                return False
        return True

    def allow_migrate(self, db, app_label, model=None, **hints):
        db_list = ('world_db')
        if db in db_list:
            return False
        return True
