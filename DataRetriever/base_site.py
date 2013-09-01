class BaseJobSite(object):

    def __init__(self, browser):
        self.browser = browser

    def pretty_dictionary_print(self, dictionary, *args):
        for item in dictionary.iteritems():
            print "========================="
            print item[0]
            print "\n%s" % item[1]