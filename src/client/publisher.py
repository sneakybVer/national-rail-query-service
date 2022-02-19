import logging


class TrainServiceUpdatePublisher(object):
    def publishUpdates(self, updates):
        for update in updates:
            logging.info("TrainServiceUpdatePublisher]: %s", update.printInfo())
