from celery import task

from rapidsms.router.blocking import BlockingRouter


@task()
def rapidsms_handle_message(msg, incoming=True):
    """Simple Celery task to process messages via BlockingRouter."""

    logger = rapidsms_handle_message.get_logger()
    if incoming:
        direction_name = 'incoming'
    else:
        direction_name = 'outgoing'
    logger.debug('New %s message: %s' % (direction_name, msg))
    router = BlockingRouter()
    try:
        router.start()
        if incoming:
            router.receive_incoming(msg)
        else:
            router.send_outgoing(msg)
        router.stop()
    except Exception, e:
        logger.exception(e)
    logger.debug('Complete')


@task()
def queue_to_send(backend_name, text, identities):
    logger = rapidsms_handle_message.get_logger()
    router = BlockingRouter()
    try:
        router.start()
        backend = router.backends[backend_name]
        backend.send(text=text, identities=identities)
        router.stop()
    except Exception, e:
        logger.exception(e)