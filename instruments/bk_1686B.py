class bk_1686B:

    def write(self, parent, *args, **kwargs):
        print('This is the bk_1686B')
        return parent.write(*args, **kwargs)
