import logging
import time


def retry(callback, tries=2):
    def retryDecorator(fn):
        def funcWrapper(*args, **kwargs):
            for i in range(tries):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    logging.error(e)
                    logging.info(
                        "calling callback {} after error".format(callback.__name__)
                    )
                    callback()
                    logging.info("retrying {} after error".format(fn.__name__))
            else:
                raise RuntimeError("Retries exceeded, see log for errors")

        return funcWrapper

    return retryDecorator
